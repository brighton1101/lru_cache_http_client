from functools import lru_cache
from lru_cache_http_client.http.requests_http_client import (
    RequestsHttpClient,
)
from lru_cache_http_client.http.http_client import HttpClient
from lru_cache_http_client.hash.hasher import Hasher

from typing import Optional


class LruHttpClient(HttpClient):
    """
    Decorator HTTP Client with a `Least Recently Used Cache` (LRU Cache) to
    cache 'identical' requests sent. By identical, that means the same
    args passed to the `get` method.

    Optionally, a user can specify a hashing function that can be used
    for a TTL policy for items added to the cache. See
    lru_cache_http_client.hash.ttl_hasher for an example implementation.

    By default, the client uses an http client that wraps around the
    `Requests` library: https://requests.readthedocs.io/en/master/ - However,
    this is extensible and can be injected by the user.
    """

    http_client = None

    hasher = None

    capacity = None

    def __init__(
        self,
        capacity: int = 128,
        http_client: Optional[HttpClient] = None,
        hasher: Optional[Hasher] = None,
    ):
        """
        :constructor
        :param capacity     - capacity for cache (should be powers of 2
                              for best performance)
        :param http_client  - optionally inject your own HttpClient impl
                              to decorate. by default, uses RequestsHttpClient
        :param hasher       - optionally inject your own Hasher implementation
                              useful for ttl indexing
        """
        _validate_http_client(http_client)
        _validate_hasher(hasher)
        self.http_client = RequestsHttpClient() if http_client is None else http_client
        self.hasher = Hasher() if hasher is None else hasher
        self.capacity = capacity
        self._setup_cahcing_func()

    def get(self, url: str, params: Optional[dict] = None, **kwargs):
        """
        Checks cache for existence of similar request (by method params). If
        similar request exists, the Response is returned from the cache. If
        not, issue a request from injected HttpClient
        :param url       - url to issue request to
        :param params    - url parameters to add onto url
        :param **kwargs  - additional args to pass to injected HttpClient
        :return          - return value of injected HttpClient's `get` method
        """

        ttl = (
            None if self.hasher is None else self.hasher.get_hash(url, params, **kwargs)
        )

        params, kwargs = self.http_client.make_args_hashable(params=params, **kwargs)

        return self.caching_func(url, params=params, ttl=ttl, **kwargs)

    caching_func = None

    def _get_caching(self, url, params=None, ttl=None, **kwargs):
        """
        Wrapper method for issuing get requests from http client. DO NOT
        call directly, but rather call through the caching_func property
        that is set at runtime
        """
        return self.http_client.get(url, params=params, **kwargs)

    def _setup_cahcing_func(self):
        """
        Setup LRU cache
        """
        self.caching_func = lru_cache(maxsize=self.capacity)(self._get_caching)


def _validate_http_client(http_client):
    if http_client is not None and not isinstance(http_client, HttpClient):
        raise TypeError("Invalid HttpClient provided for `http_client` arg")


def _validate_hasher(hasher):
    if hasher is not None and not isinstance(hasher, Hasher):
        raise TypeError("Invalid Hashing class provided for `hasher` arg.")
