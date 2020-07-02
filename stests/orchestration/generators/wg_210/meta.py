# Reuse wg_100 phase 1 & 3.
from stests.orchestration.generators.wg_100 import meta as wg_100

# Reuse wg_200 args + types.
from stests.orchestration.generators.wg_200 import meta as wg_200

from stests.orchestration.generators.wg_210 import phase_1
from stests.orchestration.generators.wg_210 import phase_2



# Workload custom args.
Arguments = wg_200.Arguments

# Workload command line args.
ARGS = wg_200.ARGS

# Workload description.
DESCRIPTION = "Counter (stored contract)"

# Set of workflow phases.
PHASES = (
    wg_100.phase_1,
    phase_1,
    phase_2,
    wg_100.phase_2,
)

# Workload type.
TYPE = "WG-210"

# Workload typeset - registered with encoder.
TYPE_SET = wg_200.TYPE_SET