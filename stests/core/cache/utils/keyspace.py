from stests.core.utils.workflow import WorkflowContext



def get_key(ctx: WorkflowContext, item_type: str, item_key: str) -> str:
    """Returns fully qualified cache key.
    
    :param ctx: Contextual information passed along the flow of execution.
    :param item_type: Type of item being cached.
    :param item_key: Key of item to be cached.

    :returns: A fully qualified cache key.

    """
    namespace = _get_namespace(ctx, item_type)

    return f"{namespace}:{item_key}"


def _get_namespace(ctx: WorkflowContext, item_type: str = None) -> str:
    """Returns namespace to be prefixed to a key.

    :param ctx: Contextual information passed along the flow of execution.
    :param item_type: Type of item being cached.

    :returns: Namespace to be prefixed to an item key.

    """
    ns = f"{ctx.network_id}.{ctx.workflow_type}.{ctx.workflow_id}"
    if item_type is not None:
        ns = f"{ns}.{item_type}"

    return ns