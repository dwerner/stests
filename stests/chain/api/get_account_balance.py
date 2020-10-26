from jsonrpcclient import request

from stests.chain.api.get_state_root_hash import execute as get_state_root_hash
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.infra import Network



# Method upon client to be invoked.
_RPC_METHOD = "state_get_balance"


def execute(
    network: Network,
    node: Node,
    purse_uref: str,
    state_root_hash: str = None,
    ) -> int:
    """Queries account balance at a certain block height | hash.

    :param network: Target network being tested.
    :param node: Target node being tested.
    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.

    :returns: Account balance.

    """
    state_root_hash = state_root_hash or get_state_root_hash(network, node)
    response = request(node.url_rpc, _RPC_METHOD, 
        state_root_hash=state_root_hash,
        purse_uref=purse_uref,
        path=[]
        )

    return response.data.result['balance_value']
