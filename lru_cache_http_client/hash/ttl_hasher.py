import time
from lru_cache_http_client.hash.hasher import Hasher
from typing import Optional


class TtlHasher(Hasher):
    """
    Hashing class for computing TTL hashes for application
    By default, the time to live is 3600 seconds
    """

    seconds: int = 3600

    # Should be treated as a Final val and not modified at runtime
    TTL_PARAM_NAME: str = "TTL_INDEX"

    def __init__(self, seconds: Optional[int] = None):
        """
        :constructor
        :param seconds - # of seconds that object should live for
        """
        self.seconds = self.seconds if seconds is None else seconds

    def setup(self, *args, **kwargs):
        kwargs[self.TTL_PARAM_NAME] = self.get_hash(args, kwargs)
        return args, kwargs

    def teardown(self, *args, **kwargs):
        del kwargs[self.TTL_PARAM_NAME]
        return args, kwargs

    def get_hash(self, *args, **kwargs):
        """
        Gets hash value based on current time
        """
        return round(time.time() / self.seconds)
