import redis

from stests.core.cache.stores.redis import evars



def get_store(network_id: str) -> redis.Redis:
    """Returns instance of a redis cache store accessor.

    :param network_id: Identifier of network being tested, e.g. DEV-LOC-01
    :returns: An instance of a redis cache store accessor.

    """
    # TODO: 1. map network id to a redis db so as to partition when
    #          running tests across multiple networks.
    db = 1
    # TODO: 2. cluster connections

    return redis.Redis(db=db, host=evars.HOST, port=evars.PORT)
