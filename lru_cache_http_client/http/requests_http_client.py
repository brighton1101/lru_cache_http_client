from lru_cache_http_client.http.http_client import HttpClient

import requests
from collections.abc import Hashable
from typing import Optional


class RequestsHttpClient(HttpClient):
    """
    Wrapper class for `requests` http client
    """

    def get(self, url: str, params: Optional[dict] = None, **kwargs):
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
