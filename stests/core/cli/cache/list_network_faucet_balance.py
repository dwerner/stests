import argparse

from stests.core import cache
from stests.core import clx
from stests.core.utils import args_validator
from stests.core import factory
from stests.core.utils import logger


# CLI argument parser.
ARGS = argparse.ArgumentParser("Lists a network's faucet balance.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    network_id=factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        logger.log_warning(f"Network {args.network} is unregistered.")
        return

    balance = clx.get_account_balance(network_id, network.faucet)

    logger.log(f"""NETWORK: {network.name} -> faucet balance = {balance}""")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
