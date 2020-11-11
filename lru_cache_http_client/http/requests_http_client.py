from lru_cache_http_client.http.http_client import HttpClient

import requests
from collections.abc import Hashable


class RequestsHttpClient(HttpClient):
    """
    Wrapper class for `requests` http client
    """

    def get(self, url, params=None, **kwargs):
        r"""Sends a GET request via 'requests' package
        https://requests.readthedocs.io/en/latest/_modules/requests/api/#get
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.get(url, params, **kwargs)

    def make_args_hashable(self, params=None, **kwargs):
        """
        Make args to `get` method hashable
        """

        # params needs to be hashable
        if params is not None:
            if isinstance(params, dict):
                params = _RequestsArg_hashabledict(params)
            elif isinstance(params, list):
                params = tuple(params)

        # certain kwargs need to be converted to hashable
        # type, notably `dict` kwargs
        dict_kwargs = ["headers", "cookies", "proxies"]
        for key, value in kwargs.items():
            if key not in dict_kwargs:
                continue
            elif isinstance(value, dict):
                kwargs[key] = _RequestsArg_hashabledict(value)

        return params, kwargs


class _RequestsArg_hashabledict(dict):
    """
    Helper wrapper around dict class to make it hashable.
    Note that all items in dict must be of type str for this
    to work
    """

    def __init__(self, unhashable_dict=None):
        """
        Given a dict, or missing val, instantiate a dict
        that can be hashed. Useful for caching method above
        """
        if unhashable_dict is None:
            unhashable_dict = {}
        dict_items = unhashable_dict.items()
        for key, val in dict_items:
            if not isinstance(key, Hashable) or not isinstance(val, Hashable):
                raise TypeError("Unhashable params passed into function")
        super().__init__(dict_items)

    def __hash__(self):
        return hash(frozenset(sorted(self.items())))
