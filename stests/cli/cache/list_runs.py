import argparse

from stests.core import cache
from stests.core.utils import args_validator
from stests.core.utils import factory
from stests.core.utils import logger


from stests.generators.wg_100 import args



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays informations regarding a generators run.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# CLI argument: generator.
ARGS.add_argument(
    "run_type",
    help="Generator type - e.g. wg-100.",
    type=args_validator.validate_run_type
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Unpack.
    network_id = factory.create_network_id(args.network)

    # Pull run contexts.
    runs = cache.get_contexts(
        network_id.name, 
        args.run_type
        )
    if not runs:
        logger.log_warning(f"No runs found within cache for {network_id.name} : {args.run_type}.")

    runs = list(map(lambda r: (r, cache.get_step(r)), runs))

    # Display.
    print("-----------------------------------------------------------------------------------------------")
    print(f"{network_id.name} : {args.run_type}")
    print("-----------------------------------------------------------------------------------------------")
    for run, step in runs:
        print(f"R-{str(run.run_index).zfill(4)} :: {step.action.ljust(22)} :: {step.status.name.ljust(11)} :: {step.ts_start} :: {step.step_elapsed_label.rjust(11)} ")
    print("-----------------------------------------------------------------------------------------------")



# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())