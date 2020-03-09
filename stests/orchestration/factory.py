from stests.core.orchestration import *



def create_info(ctx: ExecutionContext, aspect: ExecutionAspect) -> ExecutionInfo:
    """Returns a domain object instance: ExecutionInfo.

    """
    if aspect == ExecutionAspect.RUN:
        return ExecutionInfo(
            network=ctx.network,
            phase_index=None,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=ExecutionStatus.IN_PROGRESS,
            step_index=None,
            step_label=None,
            tp_duration=None,
            ts_start=datetime.now(),
            ts_end=None,
            _type_key=None
        )

    elif aspect == ExecutionAspect.PHASE:
        return ExecutionInfo(
            network=ctx.network,
            phase_index=ctx.phase_index,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=ExecutionStatus.IN_PROGRESS,
            step_index=None,
            step_label=None,
            tp_duration=None,
            ts_start=datetime.now(),
            ts_end=None,
            _type_key=None
        )

    elif aspect == ExecutionAspect.STEP:
        return ExecutionInfo(
            network=ctx.network,
            phase_index=ctx.phase_index,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=ExecutionStatus.IN_PROGRESS,
            step_index=ctx.step_index,
            step_label=ctx.step_label,
            tp_duration=None,
            ts_start=datetime.now(),
            ts_end=None,
            _type_key=None
        )


def create_state(ctx: ExecutionContext, aspect: ExecutionAspect, status: ExecutionStatus = None) -> ExecutionInfo:
    """Returns a domain object instance: ExecutionInfo.

    """
    if aspect == ExecutionAspect.RUN:
        return RunState(
            network=ctx.network,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=ctx.status,
            _type_key=None
        )

    elif aspect == ExecutionAspect.PHASE:
        return PhaseState(
            network=ctx.network,
            phase_index=ctx.phase_index,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=status,
            _type_key=None
        )

    elif aspect == ExecutionAspect.STEP:
        return StepState(
            network=ctx.network,
            phase_index=ctx.phase_index,
            run_index=ctx.run_index,
            run_type=ctx.run_type,
            status=status,
            step_index=ctx.step_index,
            step_label=ctx.step_label,
            _type_key=None
        )

def create_run_lock(ctx: ExecutionContext) -> RunLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.

    :returns: An execution lock.

    """
    return RunLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
    )


def create_phase_lock(ctx: ExecutionContext, phase_index: int) -> PhaseLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.
    :param phase_index: Index of next execution phase.

    :returns: An execution lock.

    """
    return PhaseLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=phase_index,
    )


def create_step_lock(ctx: ExecutionContext, step_index: int, step_label: str) -> StepLock:
    """Factory: Returns an execution lock.
    
    :param ctx: Execution context information.
    :param step_index: Index of next execution step.

    :returns: An execution lock.

    """
    return StepLock(
        network=ctx.network,
        run_index=ctx.run_index,
        run_type=ctx.run_type,
        phase_index=ctx.phase_index,
        step_index=step_index,
        step_label=step_label,
    )
