from lru_cache_http_client.hash.ttl_hasher import TtlHasher
import time


def test_get_hash_within_window():
    """
    Given: - user creates an instance of `TtlHasher` with 1
           second policy.
           - user gets hash twice instantaneously
    Assert: Hash is the same within one second interval
    """
    hasher = TtlHasher(seconds=1)
    hash1 = hasher.get_hash()
    hash2 = hasher.get_hash()
    assert hash1 == hash2


def test_get_hash_outside_window():
    """
    Given: - user creates an instance of `TtlHasher` with 1
           second policy
           - user gets hash, waits a second, gets another hash
    Assert: Hash is different
    """
    hasher = TtlHasher(seconds=1)
    hash1 = hasher.get_hash()
    time.sleep(1)
    hash2 = hasher.get_hash()
    assert hash1 != hash2
