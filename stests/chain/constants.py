import os



# Default time after which transaction processing should be aborted.
DEFAULT_TX_TIME_TO_LIVE = 3600000

# Default transaction gas price to apply.
DEFAULT_TX_GAS_PRICE = 10

# Default transaction fee to apply.
DEFAULT_TX_FEE = int(2e6)

# Path to client binary.
PATH_TO_BINARY = os.getenv("CLX_CLIENT")