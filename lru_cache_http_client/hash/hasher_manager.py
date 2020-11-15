from lru_cache_http_client.hash.hasher import Hasher


class HasherManager(Hasher):
    """
    An aggreagate Hasher, for applying multiple transformations
    to hash args
    """

    hashers: tuple = ()

    def __init__(self, hashers: tuple = ()):
        self.hashers = hashers

    def setup(self, *args, **kwargs):
        for hasher in self.hashers:
            args, kwargs = hasher.setup(*args, **kwargs)
        return args, kwargs

    def teardown(self, *args, **kwargs):
        for hasher in self.hashers:
            args, kwargs = hasher.teardown(*args, **kwargs)
        return args, kwargs

    @staticmethod
    def get_builder():
        return _HasherManagerBuilder()


class _HasherManagerBuilder:
    _hashers = []

    def add_hasher(self, hasher):
        self._hashers.append(hasher)
        return self

    def build(self):
        return HasherManager(tuple(self._hashers))
