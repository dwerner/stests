from stests.core.orchestration import ExecutionContext
from stests.generators.wg_100 import constants
from stests.generators.wg_100.phase_3 import utils



# Step description.
DESCRIPTION = "Refunds funds previously transferred from network faucet."

# Step label.
LABEL = "refund-network-faucet"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """     
    utils.do_refund.send(
        ctx,
        constants.ACC_RUN_FAUCET,
        constants.ACC_NETWORK_FAUCET
    )


def verify_deploy(ctx: ExecutionContext, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, dhash)
    utils.verify_refund(ctx, dhash)
    utils.verify_deploy_count(ctx, 1)
