from lru_cache_http_client.hash.hasher import Hasher
from lru_cache_http_client.http.http_client import HttpClient
from lru_cache_http_client.http.lru_http_client import LruHttpClient

import pytest
import time
from collections.abc import Hashable


class TestHttpClient(HttpClient):
    """
    Mock HttpClient to be injected into LruHttpClient for testing
    Unique calls to `get` will return unique vals.
    This is useful as we're trying to test the caching abilities
    of LruHttpClient.
    """

    count = 1

    def get(self, url, params=None, **kwargs):
        assert url != ""
        self.count += 1
        return self.count


def test_invalid_http_client():
    """
    Given: user tries to create LruHttpClient with
           invalid HttpClient
    Assert: TypeError raised
    """

    class Dummy:
        pass

    with pytest.raises(AssertionError):
        LruHttpClient(http_client=Dummy())


def test_invalid_hasher():
    """
    Given: user tries to create LruHttpClient with
           invalid Hasher
    Assert: TypeError raised
    """

    class Dummy:
        pass

    with pytest.raises(AssertionError):
        LruHttpClient(hasher=Dummy())


def test_same_req():
    """
    Given: User hits caching client with same url twice in a row.
           Successive (uncached) requests to HttpClient will return
           different results
    Assert: Both responses are the same due to caching
    """

    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    url = "example.com"
    res1 = caching_client.get(url)
    res2 = caching_client.get(url)
    assert res1 == res2


def test_diff_req():
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


def test_req_url_params_list():
    """
    Given: User hits caching client with same url twice, with
           url params supplied as unhashable type `list`
    Assert: LruHttpClient is able to make the list hashable
            and caches the request
    """
    client = TestHttpClient()
    caching_client = LruHttpClient(http_client=client)
    url = "test.com"
    res1 = caching_client.get(url)
    res2 = caching_client.get(url)
    assert res1 == res2


def test_setup_called():
    """
    Given: User hits caching client with the same url twice.
           The hashing function returns different values for the
           current parameters passed in
    Assert: The injected HttpClient's get method is called twice
    """

    class TestHasher(Hasher):
        counter = 0

        def setup(self, *args, **kwargs):
            self.counter += 1
            kwargs["test_ttl"] = self.counter
            return args, kwargs

        def teardown(self, *args, **kwargs):
            del kwargs["test_ttl"]
            return args, kwargs

    client = TestHttpClient()
    hasher = TestHasher()
    caching_client = LruHttpClient(http_client=client, hasher=hasher)
    res1 = caching_client.get("abc")
    res2 = caching_client.get("abc")
    assert res1 == 2
    assert res2 == 3


def test_teardown_called():
    """
    Given: User hits caching client injected with hasher that's
           teardown method turns url into `None` val. Injected
           HttpClient will raise Exception if `None` is passed in
    Assert: AssertionError raised
    """

    class TestHasher(Hasher):
        def teardown(self, *args, **kwargs):
            return ("",), kwargs

    client = TestHttpClient()
    hasher = TestHasher()
    caching_client = LruHttpClient(http_client=client, hasher=hasher)
    with pytest.raises(AssertionError):
        caching_client.get("hello world")
