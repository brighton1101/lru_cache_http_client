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
    _, kwargs1 = hasher.setup()
    _, kwargs2 = hasher.setup()
    hash1 = kwargs1[hasher.TTL_PARAM_NAME]
    hash2 = kwargs2[hasher.TTL_PARAM_NAME]
    assert hash1 == hash2


def test_get_hash_outside_window():
    """
    Given: - user creates an instance of `TtlHasher` with 1
           second policy
           - user gets hash, waits a second, gets another hash
    Assert: Hash is different
    """
    hasher = TtlHasher(seconds=1)
    _, kwargs1 = hasher.setup()
    time.sleep(1)
    _, kwargs2 = hasher.setup()
    hash1 = kwargs1[hasher.TTL_PARAM_NAME]
    hash2 = kwargs2[hasher.TTL_PARAM_NAME]
    assert hash1 != hash2
