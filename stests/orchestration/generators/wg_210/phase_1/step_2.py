import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.types.chain import ContractType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils import verification
from stests.orchestration.generators.utils.contracts import do_install_contract



# Step label.
LABEL = "set-named-keys"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    # Set named keys.
    account = cache.state.get_account_by_index(ctx, constants.ACC_RUN_CONTRACT)
    contract = clx.contracts.get_contract(ContractType.COUNTER_DEFINE_STORED)
    keys = clx.contracts.get_named_keys(ctx, account, None, contract.NKEYS)

    # Persist named keys.
    for key_name, key_hash in keys:
        cache.state.set_named_key(ctx, factory.create_named_key(
            account,
            contract.TYPE,
            key_name,
            key_hash,
        ))


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    # TODO: pull keys and assert
    pass
