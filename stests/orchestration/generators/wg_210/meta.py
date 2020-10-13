from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.wg_210 import args
from stests.orchestration.generators.wg_210 import phase_1



# Workload custom args.
Arguments = args.Arguments

# Workload command line args.
ARGS = args.ARGS

# Workload description.
DESCRIPTION = "Submits a deploy delegating an amount of tokens (in motes) to a validator for staking purposes."

# Set of workflow phases.
PHASES = (
    phase_1,
)

# Workload type.
TYPE = "WG-210"

# Workload typeset - registered with encoder.
TYPE_SET = {
    Arguments,
}
