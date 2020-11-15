from lru_cache_http_client.hash.hasher_manager import HasherManager
from lru_cache_http_client.hash.hasher import Hasher


def test_builder():
    """
    Given: User uses HasherManager's builder and passes in
           three valid Hasher instances
    Assert: The manager contains those instances
    """
    hasher1 = Hasher()
    hasher2 = Hasher()
    hasher_manager_builder = HasherManager.get_builder()
    hasher_manager_builder.add_hasher(hasher1)
    hasher_manager_builder.add_hasher(hasher2)
    hasher_manager = hasher_manager_builder.build()
    assert hasher1 in hasher_manager.hashers
    assert hasher2 in hasher_manager.hashers


def test_setup():
    """
    Given: User has a valid HasherManager instance with a
           Hasher that adds an argument to kwargs in setup
    Assert: HasherManager.setup will add that to kwargs
    """

    class TestHasher(Hasher):
        def __init__(self, key):
            self.key = key

        def setup(self, *args, **kwargs):
            kwargs[self.key] = 123
            return args, kwargs

    hasher1 = TestHasher("key1")
    hasher2 = TestHasher("key2")
    hasher_manager = HasherManager((hasher1, hasher2))
    _, kwargs = hasher_manager.setup()
    assert kwargs["key1"] == 123
    assert kwargs["key2"] == 123


def test_teardown():
    """
    Given: User has a valid HasherManager instance with a
           Hasher that deletes an arg in teardown
    Assert: HasherManager.teardown will destroy that
    """

    class TestHasher(Hasher):
        def __init__(self, key):
            self.key = key

        def teardown(self, *args, **kwargs):
            del kwargs[self.key]
            return args, kwargs

    hasher1 = TestHasher("a")
    hasher2 = TestHasher("b")
    hasher_manager = HasherManager((hasher1, hasher2))
    _, kwargs = hasher_manager.teardown(a=1, b=2)
    assert len(kwargs) == 0
    assert "a" not in kwargs
    assert "b" not in kwargs
