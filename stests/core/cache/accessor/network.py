from stests.core.types import Network
from stests.core.cache.utils.commands import do_set
from stests.core.cache.utils.keyspace import get_key
from stests.core.utils.workflow import WorkflowContext



def append_network(ctx: WorkflowContext, network: Network) -> str:
    """Appends network information to cache store.

    :param ctx: Contextual information passed along the flow of execution.
    :param network: Network information being cached.

    :returns: Network's cache key.

    """
    # Set key.
    key = network.name

    # Push to cache store.
    do_set(ctx, key, network)

    return key