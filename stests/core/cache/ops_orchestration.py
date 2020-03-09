import random
import typing

import stests.core.cache.ops_infra as infra
from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.domain import *
from stests.core.orchestration import *
from stests.core.utils import factory



@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_by_network(network_id: NetworkIdentifier) -> typing.Generator:
    """Flushes network specific monitoring information.

    :param network_id: A network identifier.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield ["context", network_id.name, "*"]
    yield ["lock", network_id.name, "*"]
    yield ["phase", network_id.name, "*"]
    yield ["step", network_id.name, "*"]
    yield ["step-deploy-count", network_id.name, "*"]
        

@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_by_run(ctx: ExecutionContext) -> typing.Generator:
    """Flushes previous run information.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    for collection in [
        "context",
        "phase",
        "step",
        "step-deploy-count",
    ]:
        yield [
            collection,
            ctx.network,
            ctx.run_type,
            ctx.run_index_label,
            "*"
        ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.FLUSH)
def flush_locks(ctx: ExecutionContext) -> typing.Generator:
    """Flushes previous run locks.

    :param ctx: Execution context information.

    :returns: A generator of keypaths to be flushed.
    
    """
    yield [
        "lock",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_context(network: str, run_index: int, run_type: str) -> ExecutionContext:
    """Decaches domain object: ExecutionContext.
    
    :param network: Name of network being tested.
    :param run_index: Generator run index.
    :param run_type: Generator run type, e.g. wg-100.

    :returns: Cached run context information.

    """
    run_index_label = f"R-{str(run_index).zfill(3)}"

    return [
        "context",
        network,
        run_type,
        run_index_label
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_contexts(network: str, run_type: str) -> ExecutionContext:
    """Decaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Cached run context information.

    """
    return [
        "context",
        network,
        run_type,
        "*"
    ]

def get_run_network(ctx: ExecutionContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Execution context information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return infra.get_network(network_id)


def get_step(ctx: ExecutionContext) -> ExecutionInfo:
    """Decaches domain object: ExecutionInfo.
    
    :param ctx: Execution context information.

    :returns: Cached run step information.

    """
    steps = get_steps(ctx)
    steps = sorted(steps, key=lambda i: i.ts_start)

    return steps[-1] if steps else None


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_steps(ctx: ExecutionContext) -> typing.List[ExecutionInfo]:
    """Decaches collection of domain objects: ExecutionInfo.

    :param ctx: Execution context information.

    :returns: List of run steps.
    
    """
    return [
        "step",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        "*"
        ]
        

@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET_COUNT)
def get_step_deploy_count(ctx: ExecutionContext) -> int:
    """Reurns current count of run step deploys.

    :param ctx: Execution context information.

    """
    keypath = [
        "step-deploy-count",
        ctx.network,
        ctx.run_type,
    ]
    if ctx.phase_index and ctx.step_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}.{ctx.step_index_label}")
    elif ctx.phase_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}")
    else:
        keypath.append(ctx.run_index_label)

    return keypath


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.INCR)
def increment_step_deploy_count(ctx: ExecutionContext):
    """Increments (atomically) count of run step deploys.

    :param ctx: Execution context information.

    """
    keypath = [
        "step-deploy-count",
        ctx.network,
        ctx.run_type,
    ]
    if ctx.phase_index and ctx.step_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}.{ctx.step_index_label}")
    elif ctx.phase_index:
        keypath.append(f"{ctx.run_index_label}.{ctx.phase_index_label}")
    else:
        keypath.append(ctx.run_index_label)

    return keypath


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def lock_run(lock: RunLock) -> typing.Tuple[typing.List[str], RunLock]:
    """Encaches a lock: RunLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        lock.run_index_label
    ], lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def lock_phase(lock: PhaseLock) -> typing.Tuple[typing.List[str], PhaseLock]:
    """Encaches a lock: PhaseLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        f"{lock.run_index_label}.{lock.phase_index_label}",
    ], lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.LOCK)
def lock_step(lock: StepLock) -> typing.Tuple[typing.List[str], StepLock]:
    """Encaches a lock: StepLock.

    :param lock: Information to be locked.

    """
    return [
        "lock",
        lock.network,
        lock.run_type,
        f"{lock.run_index_label}.{lock.phase_index_label}.{lock.step_index_label}",
    ], lock


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_run_context(ctx: ExecutionContext) -> typing.Tuple[typing.List[str], ExecutionContext]:
    """Encaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    return [
        "context",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label
    ], ctx



@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_run_state(state: RunState) -> typing.Tuple[typing.List[str], RunState]:
    """Encaches domain object: RunState.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    return [
        "state",
        state.network,
        state.run_type,
        state.run_index_label,
        "-"
    ], state 


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_run_info(ctx: ExecutionContext) -> ExecutionContext:
    """Decaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath to domain object instance.

    """
    return [
        "info",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        "-"
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_list_run_info(network_id: NetworkIdentifier, run_type: str) -> typing.List[ExecutionInfo]:
    """Decaches domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath to domain object instance.

    """
    return [
        "info",
        network_id.name,
        run_type,
        "*"
    ]


def update_run_info(ctx: ExecutionContext) -> ExecutionInfo:
    """Updates domain object: ExecutionContext.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    # Pull.
    info = get_run_info(ctx)

    # Update.
    # TODO: set error from context.
    info.end(ctx.status, None)

    # Recache.
    set_info(info)

    return info


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_phase_info(ctx: ExecutionContext) -> ExecutionInfo:
    """Decaches domain object: ExecutionInfo.
    
    :param ctx: Execution context information.

    :returns: Keypath to domain object instance.

    """
    return [
        "info",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        ctx.phase_index_label,
    ]


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_phase_state(state: PhaseState) -> typing.Tuple[typing.List[str], PhaseState]:
    """Encaches domain object: PhaseState.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    return [
        "state",
        state.network,
        state.run_type,
        state.run_index_label,
        state.phase_index_label,
    ], state 


def update_phase_info(ctx: ExecutionContext, status: ExecutionStatus) -> ExecutionInfo:
    """Updates domain object: ExecutionInfo.
    
    :param ctx: Execution context information.
    :param status: New execution state.

    :returns: Keypath + domain object instance.

    """
    # Pull & update.
    info = get_phase_info(ctx)
    info.end(status, None)

    # Recache.
    set_info(info)

    return info


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_step_info(info: ExecutionInfo) -> typing.Tuple[typing.List[str], ExecutionInfo]:
    """Encaches domain object: ExecutionInfo.
    
    :param evt: ExecutionInfo domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        "info",
        info.network,
        info.run_type,
        info.run_index_label,
        f"{info.phase_index_label}.{info.step_index_label}"
    ], info


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_step_state(state: StepState) -> typing.Tuple[typing.List[str], StepState]:
    """Encaches domain object: RunState.
    
    :param ctx: Execution context information.

    :returns: Keypath + domain object instance.

    """
    return [
        "state",
        state.network,
        state.run_type,
        state.run_index_label,
        f"{state.phase_index_label}.{state.step_index_label}"
    ], state


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.GET)
def get_step_info(ctx: ExecutionContext) -> ExecutionInfo:
    """Decaches domain object: ExecutionInfo.
    
    :param ctx: Execution context information.

    :returns: Keypath to domain object instance.

    """
    return [
        "info",
        ctx.network,
        ctx.run_type,
        ctx.run_index_label,
        f"{ctx.phase_index_label}.{ctx.step_index_label}"
    ]


def update_step_info(ctx: ExecutionContext, status: ExecutionStatus) -> ExecutionInfo:
    """Updates domain object: ExecutionInfo.
    
    :param ctx: Execution context information.
    :param status: New execution state.

    :returns: Keypath + domain object instance.

    """
    # Pull & update.
    info = get_step_info(ctx)
    info.end(status, None)

    # Recache.
    set_info(info)

    return info


@cache_op(StorePartition.ORCHESTRATION, StoreOperation.SET)
def set_info(info: ExecutionInfo) -> typing.Tuple[typing.List[str], ExecutionInfo]:
    """Encaches domain object: ExecutionInfo.
    
    :param evt: ExecutionInfo domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    if info.phase_index and info.step_index:
        return [
            "info",
            info.network,
            info.run_type,
            info.run_index_label,
            f"{info.phase_index_label}.{info.step_index_label}"
        ], info
    elif info.phase_index:
        return [
            "info",
            info.network,
            info.run_type,
            info.run_index_label,
            info.phase_index_label,
            ], info
    else:
        return [
            "info",
            info.network,
            info.run_type,
            info.run_index_label,
            "-",
        ], info