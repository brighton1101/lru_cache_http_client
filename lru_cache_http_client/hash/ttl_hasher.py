import time
from lru_cache_http_client.hash.hasher import Hasher


class TtlHasher(Hasher):
    """
    Hashing class for computing TTL hashes for application
    By default, the time to live is 3600 seconds
    """

    seconds = None

    def __init__(self, seconds=3600):
        """
        :constructor
        :param seconds - # of seconds that object should live for
        """
        self.seconds = seconds

    def get_hash(self, *args, **kwargs):
        """
        Gets hash value based on current time
        """
        return round(time.time() / self.seconds)
