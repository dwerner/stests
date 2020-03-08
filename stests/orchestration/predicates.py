import typing

from stests.core import cache
from stests.core.cache.locks import RunLock
from stests.core.cache.locks import RunPhaseLock
from stests.core.cache.locks import RunStepLock
from stests.core.domain import RunContext
from stests.core.utils import logger
from stests.orchestration.model import Workflow



def can_start_run(ctx: RunContext) -> bool:
    """Returns flag indicating whether a run increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a run increment is valid.

    """
    # False if workflow invalid.
    _, wflow_is_valid = _validate_wflow(ctx)
    if not wflow_is_valid:
        return False

    # False if phase/step are not initialised.
    if ctx.phase_index != 0 or ctx.step_index != 0:
        logger.log_warning(f"invalid context - phase & step must be set to zero: {ctx.run_type} :: run={ctx.run_index}")
        return False

    # False if locked.
    lock = RunLock(
        ctx.network,
        ctx.run_index,
        ctx.run_type
    )
    _, acquired = cache.control.lock_run(lock)
    if not acquired:
        logger.log_warning(f"unacquired run lock: {ctx.run_type} :: run={ctx.run_index}")
        return False

    # All tests passed, therefore return true.    
    return True


def can_start_phase(ctx: RunContext) -> bool:
    """Returns flag indicating whether a phase increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a phase increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = _validate_wflow(ctx)
    if not wflow_is_valid:
        return False

    # Set indexes.
    phase_index = ctx.phase_index + 1

    # False if phase index is invalid.
    if phase_index > len(wflow.phases):
        logger.log_warning(f"invalid phase index: {ctx.run_type} :: run={ctx.run_index} :: phase={phase_index}")
        return False
    
    # False if locked.
    lock = RunPhaseLock(
        ctx.network,
        ctx.run_index,
        ctx.run_type,
        phase_index
    )
    _, acquired = cache.control.lock_phase(lock)
    if not acquired:
        logger.log_warning(f"unacquired phase lock: {ctx.run_type} :: run={ctx.run_index} :: phase={phase_index}")
        return False
    
    # All tests passed, therefore return true.    
    return True


def can_start_step(ctx: RunContext) -> bool:
    """Returns flag indicating whether a step increment is valid.
    
    :param ctx: Execution context information.

    :returns: Flag indicating whether a step increment is valid.

    """
    # False if workflow invalid.
    wflow, wflow_is_valid = _validate_wflow(ctx)
    if not wflow_is_valid:
        return False

    # Set indexes.
    phase_index = ctx.phase_index
    step_index = ctx.step_index + 1

    # False if phase index is invalid.
    if phase_index > len(wflow.phases):
        logger.log_warning(f"invalid phase index: {ctx.run_type} :: {ctx.run_index_label} :: phase={phase_index}")
        return False
    
    # False if step index is invalid.
    phase = wflow.phases[phase_index - 1]
    if step_index > len(phase.steps):
        logger.log_warning(f"invalid step index: {ctx.run_type} :: {ctx.run_index_label} :: phase={phase_index} :: step={step_index}")
        return False

    # False if locked.
    lock = RunStepLock(
        ctx.network,
        ctx.run_index,
        ctx.run_type,
        phase_index,
        step_index
    )
    _, acquired = cache.control.lock_step(lock)
    if not acquired:
        logger.log_warning(f"unacquired step lock: {ctx.run_type} :: run={ctx.run_index} :: phase={phase_index} :: step={step_index}")
        return False
    
    # All tests passed, therefore return true.    
    return True


def _validate_wflow(ctx: RunContext) -> typing.Tuple[typing.Optional[Workflow], bool]:
    """Predicate determining whether the workflow to be executed is valid or not.
    
    """
    # False if workflow unregistered.
    try:
        wflow = Workflow.create(ctx)
    except ValueError:
        logger.log_warning(f"unregistered workflow: {ctx.run_type}")
        return None, False

    # False if workflow has no phases.
    if not wflow.phases:
        logger.log_warning(f"invalid workflow - has no associated phases: {ctx.run_type}")
        return None, False

    # False if a phase has no steps.
    for phase in wflow.phases:
        if not phase.steps:
            logger.log_warning(f"invalid workflow - a phase has no associated steps: {ctx.run_type}")
            return None, False

    # All tests passed, therefore return true.   
    return wflow, True
