from jsonrpcclient import request

from stests.core.types.infra import Network
from stests.core.types.infra import Node


# Method upon client to be invoked.
_RPC_METHOD = "info_get_deploy"


def execute(
    network: Network,
    node: Node,
    deploy_hash: str,
    ) -> str:
    """Queries a node for a deploy.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param deploy_hash: Hash of deploy being pulled.

    :returns: Representation of a deploy within a node's state.

    """
    response = request(node.url_rpc, _RPC_METHOD, deploy_hash=deploy_hash)

    return response.data.result
