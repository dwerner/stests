from stests.core import cache
from stests.core import clx
from stests.core.domain import DeployStatus
from stests.core.domain import RunContext
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus
from stests.core.mq.actor import actorify
from stests.generators.wg_100 import constants



@actorify(is_substep=True)
def do_refund(ctx: RunContext, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Generator run contextual information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
    """
    # Pull accounts.
    cp1 = cache.get_account_by_run(ctx, cp1_index)
    if cp2_index == constants.ACC_NETWORK_FAUCET:
        network = cache.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.get_account_by_run(ctx, cp2_index)

    # Refund CLX from cp1 -> cp2.
    (deploy, refund) = clx.do_refund(ctx, cp1, cp2)

    # Update cache.
    cache.set_run_deploy(deploy)
    cache.set_run_transfer(refund)


def verify_deploy(ctx: RunContext, dhash: str):
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.get_run_deploy(dhash)
    assert deploy
    assert deploy.status == DeployStatus.FINALIZED


def verify_deploy_count(ctx: RunContext, expected: int):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    assert cache.get_step_deploy_count(ctx) == expected


def verify_refund(ctx: RunContext, dhash: str) -> Transfer:
    """Verifies that a refund between counter-parties completed.
    
    """
    refund = cache.get_run_transfer(dhash)
    assert refund
    assert refund.status == TransferStatus.COMPLETE