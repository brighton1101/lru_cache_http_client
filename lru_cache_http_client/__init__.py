from lru_cache_http_client.hash.hasher import Hasher
from lru_cache_http_client.hash.ttl_hasher import TtlHasher
from lru_cache_http_client.http.lru_http_client import LruHttpClient


def get_caching_client(capacity=128, ttl_seconds=None):
    """
    Returns a caching HTTP client for making GET requets. LruHttpClient by
    default uses the `requests` package to issue HTTP requests, so any params
    that work for `requests.get` also work for `LruHttpClient.get`
    :param capacity    - by default, 128. most performant if number supplied
                         is a power of 2
    :param ttl_seconds - by default, None. if provided, items in the cache
                         will have a ttl policy with this value
    :return an instance of `LruHttpClient`
    """
    hasher = Hasher() if ttl_seconds is None else TtlHasher(seconds=ttl_seconds)
    return LruHttpClient(capacity, hasher=hasher)
