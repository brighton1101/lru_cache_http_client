import time
from lru_cache_http_client.hash.hasher import Hasher
from typing import Optional


class TtlHasher(Hasher):
    """
    Hashing class for computing TTL hashes for application
    By default, the time to live is 3600 seconds
    """

    seconds: int = 3600

    def __init__(self, seconds: Optional[int] = None):
        """
        :constructor
        :param seconds - # of seconds that object should live for
        """
        self.seconds = self.seconds if seconds is None else seconds

    def get_hash(self, *args, **kwargs):
        """
        Gets hash value based on current time
        """
        return round(time.time() / self.seconds)
