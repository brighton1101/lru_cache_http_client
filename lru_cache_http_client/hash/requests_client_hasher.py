from lru_cache_http_client.hash.hasher import Hasher
from collections.abc import Hashable


class RequestsClientHasher(Hasher):
    """
    Hashing class for making args passed to
    `lru_cache_http_client.http.requests_http_client.RequestsHttpClient`
    hashable.
    """

    def setup(self, *args, **kwargs):
        """
        Make args passed to `RequestsHttpClient.get` method hashable
        """

        # certain kwargs need to be converted to hashable
        # type, notably `dict` kwargs that don't have the
        # __hash__ method defined
        dict_kwargs = ["headers", "cookies", "proxies", "params"]
        for key, value in kwargs.items():
            if key not in dict_kwargs:
                continue
            elif key == "params" and isinstance(value, list):
                kwargs[key] = tuple(value)
            elif isinstance(value, dict) and not self._is_hashable(value):
                kwargs[key] = _RequestsArg_hashabledict(value)

        return args, kwargs

    def _is_hashable(self, in_dict):
        return in_dict.__hash__ is not None


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
