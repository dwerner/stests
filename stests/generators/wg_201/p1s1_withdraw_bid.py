from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.generators.utils import verification
from stests.generators.utils.infra import get_network_node


# Step label.
LABEL = "auction-bid-withdraw"

# Account index of user dispatching bid withdrawal.
_USER_ACCOUNT_INDEX = 1


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set target network / node.
    network, node = get_network_node(ctx)

    # Set validator account.
    validator = factory.create_account_for_run(ctx, _USER_ACCOUNT_INDEX, "WG-200")

    # Submit deploy.
    dispatch_info = chain.DeployDispatchInfo(validator, network, node)
    deploy_hash, dispatch_duration, dispatch_attempts = \
        chain.set_auction_bid_withdraw(
            dispatch_info,
            ctx.args.amount
            )

    # Update cache: deploy.
    cache.state.set_deploy(factory.create_deploy_for_run(
        ctx=ctx, 
        account=validator,
        node=node, 
        deploy_hash=deploy_hash, 
        dispatch_attempts=dispatch_attempts,
        dispatch_duration=dispatch_duration,
        typeof=DeployType.AUCTION_BID_WITHDRAW
        ))


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, 1) 
