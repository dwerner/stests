import inspect
import typing
from datetime import datetime as dt

import dramatiq

from stests.core import cache
from stests.core.utils import logger
from stests.core.domain import RunContext
from stests.core.domain import RunStepStatus
from stests.generators.wg_100 import correlator as wg_100_correlator


# Queue to which messages will be dispatched.
_QUEUE = "correlator"

# Map: run type --> run correlator.
CORRELATORS = {
    "WG-100": wg_100_correlator,
}


@dramatiq.actor(queue_name=_QUEUE)
def correlate_finalized_deploy(ctx: RunContext, dhash: str):   
    """Correlates a finalzied deploy with a workload generator correlation handler.
    
    :param ctx: Generator run contextual information.
    :param dhash: Hash of a finalized deploy.

    """
    # Escape if no correlator.
    try:
        correlator = CORRELATORS[ctx.run_type]
    except KeyError:
        logger.log_warning(f"Workload generator {ctx.run_type} has no registered correlator")
        return
    
    # Escape if current step to actor mapping failed.
    actor = _get_actor(ctx, correlator)
    if actor is None:
        logger.log_warning(f"Workload generator {ctx.run_type} {ctx.run_step} has no registered actor")
        return

    # Verify current step.
    if not _verify(ctx, correlator, actor, dhash):
        return

    # Complete curent step.
    _complete_step(ctx)

    # Increment step.
    _increment(ctx, correlator, actor)


def _complete_step(ctx):
    """Returns step information for downstream correlation.
    
    """
    step = cache.get_run_step(ctx)
    step.status = RunStepStatus.COMPLETE
    step.timestamp_end = dt.now().timestamp()
    cache.set_run_step(step)


def _verify(ctx: RunContext, correlator, actor: dramatiq.Actor, dhash: str) -> bool:
    """Verifies that a step has completed prior to incrementation.
    
    """
    try:
        verifier = correlator.VERIFIERS[actor]
    except KeyError:
        logger.log_warning(f"{ctx.run_type} has no verifier for step {ctx.run_step}")
        return True
    else:
        return verifier(ctx, dhash)


def _increment(ctx: RunContext, correlator, actor: dramatiq.Actor):
    """Increments a run step.
    
    """
    next_actor = _get_next_actor(ctx, correlator, actor)
    if next_actor:
        next_actor.send(ctx)
    else:
        "TODO: mark end of workload generator"
        pass


def _get_actor(ctx: RunContext, correlator) -> dramatiq.Actor:
    """Returns an actor from a pipeline bymatching it's name against a run step.
    
    """
    for actor in correlator.PIPELINE:
        if ctx.run_step == _get_step_from_actor(actor):
            return actor


def _get_next_actor(ctx: RunContext, correlator, actor: dramatiq.Actor) -> dramatiq.Actor:
    """Derives next actor in pipeline.
    
    """
    for idx, actor in enumerate(correlator.PIPELINE):
        if ctx.run_step == _get_step_from_actor(actor):
            try:
                return correlator.PIPELINE[idx + 1]
            except IndexError:
                return None


def _get_step_from_actor(actor: dramatiq.Actor) -> str:
    """Gets name of actor so that it can be mapped to a step.
    
    """
    fn = actor.fn
    m = inspect.getmodule(fn)

    return f"{m.__name__.split('.')[-1]}.{fn.__name__}"