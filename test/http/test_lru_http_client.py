from lru_cache_http_client.hash.hasher import Hasher
from lru_cache_http_client.http.requests_http_client import HttpClient
from lru_cache_http_client.http.lru_http_client import LruHttpClient

import pytest
import time


def test_invalid_http_client():
    """
    Given: user tries to create LruHttpClient with
           invalid HttpClient
    Assert: TypeError raised
    """

    class Dummy:
        pass

    with pytest.raises(TypeError):
        LruHttpClient(http_client=Dummy())


def test_invalid_hasher():
    """
    Given: user tries to create LruHttpClient with
           invalid Hasher
    Assert: TypeError raised
    """

    class Dummy:
        pass

    with pytest.raises(TypeError):
        LruHttpClient(hasher=Dummy())


def test_no_ttl_same_req():
    """
    Given: User hits caching client with same url twice in a row.
           Successive (uncached) requests to HttpClient will return
           different results
    Assert: Both responses are the same due to caching
    """

    class TestHttpClient(HttpClient):
        count = 1

        def get(self, url, params=None, **kwargs):
            self.count += 1
            return self.count

    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    url = "example.com"
    res1 = caching_client.get(url)
    res2 = caching_client.get(url)
    assert res1 == res2


def test_no_ttl_same_req_url_params():
    """
    Given: User hits caching client with same url and url params dict
           twice in a row. Successive (uncached) requests to HttpClient
           will return different results
    Assert: Both responses are the same due to caching
    """

    class TestHttpClient(HttpClient):
        count = 1

        def get(self, url, params=None, **kwargs):
            self.count += 1
            return self.count

    url = "test.com"
    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    url_params = {"hello": "world"}
    res1 = caching_client.get(url, params=url_params)
    res2 = caching_client.get(url, params=url_params)
    assert res1 == res2


def test_get_diff_req():
    """
    Given: User hits caching client with two different urls three
           times. Successive requests to HttpClient injected into
           LruHttpClient will return different results
    Assert: Unique requests give different reponsonses and duplicate
            requests return cached responses
    """

    class TestHttpClient(HttpClient):
        count = 1

        def get(self, url, params=None, **kwargs):
            self.count += 1
            return self.count

    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    res1 = caching_client.get("different")
    res2 = caching_client.get("urls")
    res3 = caching_client.get("different")
    assert res1 == res3
    assert res2 != res3


def test_get_same_url_diff_url_params():
    """
    Given: User hits caching client with same URL twice, but
           different URL params. Successive requests to injected
           HttpClient will return different results
    Assert: They are treated as unique requests and get unique
            responses.
    """

    class TestHttpClient(HttpClient):
        count = 1

        def get(self, url, params=None, **kwargs):
            self.count += 1
            return self.count

    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    url = "test.come"
    res1 = caching_client.get(url, params={"a": "b"})
    res2 = caching_client.get(url, params={"a": "c"})
    assert res1 != res2


def test_ttl_expired():
    """
    Given: User hits caching client with the same url twice.
           The hashing function returns different values for the
           current hash (to simulate ttl behavior).
    Assert: The injected HttpClient's get method is called twice
    """

    class TestHttpClient(HttpClient):
        counter = 0

        def get(self, url, params=None, **kwargs):
            self.counter += 1
            return self.counter

    class TestHasher(Hasher):
        counter = 0

        def get_hash(self, *args, **kwargs):
            self.counter += 1
            return self.counter

    client = TestHttpClient()
    hasher = TestHasher()
    caching_client = LruHttpClient(http_client=client, hasher=hasher)
    res1 = caching_client.get("abc")
    res2 = caching_client.get("abc")
    assert res1 == 1
    assert res2 == 2
