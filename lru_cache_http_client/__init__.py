from lru_cache_http_client.hash.hasher import Hasher
from lru_cache_http_client.hash.ttl_hasher import TtlHasher
from lru_cache_http_client.http.lru_http_client import LruHttpClient


def get_caching_client(capacity=128, ttl_seconds=None):
    hasher = Hasher() if ttl_seconds == None else TtlHasher(seconds=ttl_seconds)
    return LruHttpClient(capacity, hasher=hasher)
