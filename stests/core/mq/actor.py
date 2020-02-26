import inspect
import functools
import typing
from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import factory
from stests.core.domain import RunStepStatus
from stests.core.cache import RunStepLock



# Queue to which message will be dispatched.
_QUEUE = f"generators.wg-100"


def actorify(on_success=None, is_substep=False):
    """Decorator to orthoganally convert a function into an actor.

    :param on_success: Continuation function upon execution success.
    :param is_substep: Flag indicating whether decorated function is a sub-step or not.

    :returns: Decorated function.
    
    """
    def decorator_actorify(actor):

        @dramatiq.actor(queue_name=_get_queue_name(actor))
        @functools.wraps(actor)
        def wrapper_actorify(*args, **kwargs):
            # Set context.
            ctx = args[0]

            # All steps must be locked prior to execution.
            if not is_substep:
                if not _can_step(ctx, actor):
                    return
                _set_step(ctx, actor)
            
            # Invoke actor.
            result = actor(*args, **kwargs)

            # If actor returned a message factory then wrap in a dramatiq.group.
            if inspect.isfunction(result):
                result = dramatiq.group(result())

            # Auto complete step when continuation actor is defined.
            if not is_substep and on_success:
                _complete_step(ctx)

            # Groups.
            if isinstance(result, dramatiq.group):
                if on_success:
                    result.add_completion_callback(on_success().message(ctx))
                result.run()

            # Continuation.
            elif on_success:
                on_success().send(ctx)

        return wrapper_actorify

    return decorator_actorify


def _can_step(ctx, actor):
    """Predicate to determine if next step within a workflow can be executed or not.
    
    """
    step = _get_step(actor)
    lock = RunStepLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        step=step
    )
    _, acquired = cache.lock_run_step(lock)

    print(f"222 :: {ctx.run_type} :: {step} :: {acquired}")

    return acquired


def _set_step(ctx, actor):
    """Returns step information for downstream correlation.
    
    """
    step = _get_step(actor)
    cache.set_run_step(
        factory.create_run_step(ctx, step)
    )
    ctx.run_step = step
    cache.set_run_context(ctx)


def _get_step(actor):
    """Returns a queue name derived from module in which actor is declared.
    
    """
    m = inspect.getmodule(actor)

    return f"{m.__name__.split('.')[-1]}.{actor.__name__}"


def _get_queue_name(actor):
    """Returns a queue name derived from module in which actor is declared.
    
    """
    m = inspect.getmodule(actor)

    return f"{m.__name__.split('.')[-2]}".replace('_', "-")


def _complete_step(ctx):
    """Returns step information for downstream correlation.
    
    """
    step = cache.get_run_step(ctx)
    step.status = RunStepStatus.COMPLETE
    step.timestamp_end = dt.now().timestamp()
    cache.set_run_step(step)
