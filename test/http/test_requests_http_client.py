from lru_cache_http_client.http.requests_http_client import RequestsHttpClient

from collections.abc import Hashable
import pytest


def test_dict_with_unhashable_key():
    """
    Given: User passes in url params as dict with value
           of key that is not hashable
    Assert: TypeError raised
    """
    reqs_client = RequestsHttpClient()
    url_params = {"1": {"1": "234"}}
    with pytest.raises(TypeError):
        reqs_client.make_args_hashable(params=url_params)


def test_url_params_list():
    """
    Given: User passes in url params as unhashable list
    Assert: params are returned that are hashable
    """
    reqs_client = RequestsHttpClient()
    url_params = [("a", "b"), ("c", "d")]
    params, kwargs = reqs_client.make_args_hashable(params=url_params)
    assert isinstance(params, Hashable)


def test_url_params_dict():
    """
    Given: User passes in url params as unhashable dict
    Assert: params are returned that are hashable
    """
    reqs_client = RequestsHttpClient()
    url_params = {"a": "b"}
    params, kwargs = reqs_client.make_args_hashable(params=url_params)
    assert isinstance(params, Hashable)
    assert len(params) == 1
    assert params["a"] == "b"


def test_hashing_kwargs():
    """
    Given: User passes in headers, cookies, proxies that are of type dict
    Assert: They are returned as being hashable
    """
    reqs_client = RequestsHttpClient()
    url_params = None
    headers = {"a": "b"}
    cookies = {"c": "d"}
    proxies = {"e": 123}
    params, kwargs = reqs_client.make_args_hashable(
        params=url_params, cookies=cookies, headers=headers, proxies=proxies
    )
    assert isinstance(kwargs["headers"], Hashable)
    assert len(kwargs["headers"]) == 1
    assert kwargs["headers"]["a"] == "b"
    assert isinstance(kwargs["cookies"], Hashable)
    assert len(kwargs["cookies"]) == 1
    assert kwargs["cookies"]["c"] == "d"
    assert isinstance(kwargs["proxies"], Hashable)
    assert len(kwargs["proxies"]) == 1
    assert kwargs["proxies"]["e"] == 123
