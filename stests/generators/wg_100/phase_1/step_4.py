import random
import typing

from stests.core.orchestration import ExecutionContext
from stests.generators import utils
from stests.generators.wg_100 import constants



# Step description.
DESCRIPTION = "Fund's a set of run user accounts."

# Step label.
LABEL = "fund-users"


def execute(ctx: ExecutionContext) -> typing.Callable:
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    # Set dispatch window.
    deploy_count = ctx.args.user_accounts
    deploy_dispatch_window = ctx.get_dispatch_window_ms(deploy_count)

    # Transfer: run faucet -> user.
    for acc_index in range(constants.ACC_RUN_USERS, ctx.args.user_accounts + constants.ACC_RUN_USERS):
        utils.do_fund_account.send_with_options(
            args = (
                ctx,
                constants.ACC_RUN_FAUCET,
                acc_index,
                ctx.args.user_initial_clx_balance,
                False
            ),
            delay=random.randint(0, deploy_dispatch_window)
        )


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    utils.verify_deploy_count(ctx, ctx.args.user_accounts)    


def verify_deploy(ctx: ExecutionContext, bhash: str, dhash: str):
    """Step deploy verifier.
    
    :param ctx: Execution context information.
    :param dhash: A deploy hash.

    """
    utils.verify_deploy(ctx, bhash, dhash)
    transfer = utils.verify_transfer(ctx, dhash)
    utils.verify_account_balance(ctx, transfer.cp2_index, ctx.args.user_initial_clx_balance)
