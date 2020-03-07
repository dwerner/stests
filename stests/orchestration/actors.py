import inspect

import dramatiq

from stests.core import cache
from stests.core.cache.locks import RunLock
from stests.core.cache.locks import RunPhaseLock
from stests.core.cache.locks import RunStepLock
from stests.core.domain import ExecutionStatus
from stests.core.domain import RunContext
from stests.core.utils import logger

from stests.orchestration.model import Workflow
from stests.orchestration.model import WorkflowStep
from stests.orchestration import factory
from stests.orchestration import predicates



# Queue to which messages will be dispatched.
_QUEUE = "orchestration"


@dramatiq.actor(queue_name=_QUEUE)
def do_run(ctx: RunContext):
    """Runs a workflow.
    
    :param ctx: Execution context information.
    
    """
    # Temporary - will be done on run completion.
    cache.flush_locks(ctx)

    # Update ctx.
    ctx.phase_index = 0
    ctx.step_index = 0

    # Escape if unexecutable - acquires a lock otherwise.
    if not predicates.can_start_run(ctx):
        return

    # Update cache.
    cache.flush_by_run(ctx)
    cache.control.set_run_context(ctx)
    cache.control.set_state(factory.create_state(ctx))

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> starts")

    # Start phase 1.
    do_phase.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_run_end(ctx: RunContext):
    """Ends a workflow.
    
    :param ctx: Execution context information.
    
    """
    # Update status.
    cache.control.set_state(factory.create_state(ctx, status=ExecutionStatus.COMPLETE))

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} -> ends")


@dramatiq.actor(queue_name=_QUEUE)
def on_run_error(ctx: RunContext, err: str):
    """Ends a workflow phase in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # TODO.
    print(999)


@dramatiq.actor(queue_name=_QUEUE)
def do_phase(ctx: RunContext):
    """Runs a workflow phase.
    
    :param ctx: Execution context information.
    
    """
    # Update ctx.
    ctx.phase_index += 1
    ctx.step_index = 0

    # Escape if unexecutable - acquires a lock otherwise.
    if not predicates.can_start_phase(ctx, ctx.phase_index):
        return

    # Update cache.
    cache.control.set_run_context(ctx)
    cache.control.set_state(factory.create_state(ctx, ctx.phase_index))

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> starts")

    # Start step 1.
    do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_phase_end(ctx: RunContext):
    """Ends a workflow phase.
    
    :param ctx: Execution context information.
    
    """
    # Set phase.
    phase = Workflow.get_phase_(ctx, ctx.phase_index)

    # Update status.
    cache.control.set_state(factory.create_state(ctx, ctx.phase_index, status=ExecutionStatus.COMPLETE))

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} -> ends")

    # Enqueue either end of workflow or next phase. 
    if phase.is_last:
        on_run_end.send(ctx)
    else:
        do_phase.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def on_phase_error(ctx: RunContext, err: str):
    """Ends a workflow phase in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # TODO.
    print(999)


@dramatiq.actor(queue_name=_QUEUE)
def do_step(ctx: RunContext):
    """Runs a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Update ctx.
    ctx.step_index += 1

    # Escape if unexecutable - acquires a lock otherwise.
    if not predicates.can_start_step(ctx, ctx.phase_index, ctx.step_index):
        return

    # Update cache.
    cache.control.set_run_context(ctx)
    cache.control.set_state(factory.create_state(ctx, ctx.phase_index, ctx.step_index))

    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)    

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> starts")

    # Execute.
    do_step_execute(ctx, step)


def do_step_execute(ctx: RunContext, step: WorkflowStep):
    """Performs step execution.
    
    :param ctx: Execution context information.
    :param step: Step related execution information.
    
    """
    # Execute step.
    step.execute()

    # Process errors.
    if step.error:
        do_step_error.send(ctx, str(step.error))

    # Async steps are processed by deploy listeners.
    elif step.is_async:
        if step.result is not None:
            if inspect.isfunction(step.result):
                message_factory = step.result()
                group = dramatiq.group(message_factory)
                group.run()
            else:
                raise TypeError("Expecting either none or a message factory from a step function.")
        logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> listening for chain events")

    # Sync steps are processed inline.
    else:
        if step.result is None:
            do_step_end.send(ctx)

        elif inspect.isfunction(step.result):
            message_factory = step.result()
            group = dramatiq.group(message_factory)
            group.add_completion_callback(do_step_end.message(ctx))
            group.run()

        else:
            raise TypeError("Expecting either none or a message factory from a step function.")


@dramatiq.actor(queue_name=_QUEUE)
def do_step_end(ctx: RunContext):
    """Ends a workflow step.
    
    :param ctx: Execution context information.
    
    """
    # Set step.
    step = Workflow.get_phase_step(ctx, ctx.phase_index, ctx.step_index)

    # Update status.
    cache.control.set_state(factory.create_state(ctx, ctx.phase_index, ctx.step_index, ExecutionStatus.COMPLETE))

    # Inform.
    logger.log(f"WFLOW :: {ctx.run_type} :: {ctx.run_index_label} :: {ctx.phase_index_label} :: {ctx.step_index_label} :: {step.label} -> end")

    # Enqueue either end of phase or next step. 
    if step.is_last:
        on_phase_end.send(ctx)
    else:
        do_step.send(ctx)


@dramatiq.actor(queue_name=_QUEUE)
def do_step_error(ctx: RunContext, err: str):
    """Ends a workflow step in error.
    
    :param ctx: Execution context information.
    :param err: Execution error information.
    
    """
    # TODO.
    print(999)
