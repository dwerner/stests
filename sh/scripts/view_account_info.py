import argparse
import json
import typing

from stests.core import clx
from stests.core import factory
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays an on-chain account information.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: network name.
ARGS.add_argument(
    "account_id",
    help="Network account identifier (hex format), e.g. 78d38ce2ffab138bfa972f1d69e3aad7327fc0b1bcf89a5b0ca89475c2f49f43.",
    type=str
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    _render(clx.get_account_info(
        factory.create_network_id(args.network),
        args.account_id
        ))


def _render(info: typing.Dict[str, typing.Union[str, int]]):
    """Renders on-chain deploy information.
    
    """
    print("--------------------------------------------------------------------------------------------")
    if info:
        print(json.dumps(info, indent=4))
    else:
        print("Chain query returned null - is the address correct ?")
    print("--------------------------------------------------------------------------------------------")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())