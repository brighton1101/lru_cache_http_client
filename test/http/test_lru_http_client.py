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


def test_get_no_ttl_same_params():
    """
    Given: User hits caching client with same url twice in a row.
           Normal requests without caching take two seconds each
    Assert: To get both responses, it takes roughly two seconds
    """

    class TestHttpClient(HttpClient):
        def get(self, url, params=None, **kwargs):
            time.sleep(2)
            return "hello world" if url == "example.com" else "different"

    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    t1 = time.time()
    url = "example.com"
    res1 = caching_client.get(url)
    res2 = caching_client.get(url)
    assert (time.time() - t1) < 2.1
    assert res1 == res2


def test_get_no_ttl_diff_params():
    """
    Given: User hits caching client with two different urls three
           times. Normal requests without caching take two seconds
           each.
    Assert: The three requests take approximately 4 seconds to run
            (2 seconds for each unique request), and that the results
            are matching what is expected
    """

    class TestHttpClient(HttpClient):
        def get(self, url, params=None, **kwargs):
            time.sleep(2)
            return "hello world" if url == "different" else "hello"

    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    t2 = time.time()
    res1 = caching_client.get("different")
    res2 = caching_client.get("urls")
    res3 = caching_client.get("different")
    finished = time.time()
    assert (finished - t2) > 3.9
    assert (finished - t2) < 4.1
    assert res1 == res3
    assert res2 != res3


def test_get_ttl_expired():
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
