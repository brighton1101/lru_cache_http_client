from lru_cache_http_client.hash.ignore_fields_hasher import IgnoreFieldsHasher

import pytest


def test_ignore_field_setup_positional_invalid():
    ignored_fields = [0, 1]
    hasher = IgnoreFieldsHasher(ignored_fields)
    with pytest.raises(IndexError):
        hasher.setup("a")


def test_ignore_field_setup_positional():
    ignored_fields = [0, 1]
    hasher = IgnoreFieldsHasher(ignored_fields)
    args1, _ = hasher.setup("a", "b")
    args2, _ = hasher.setup("d", "e")
    assert args1[0].__hash__() == args2[0].__hash__()
    assert args1[1].__hash__() == args2[1].__hash__()


def test_ignore_field_setup_keyword():
    ignored_fields = ["hello"]
    hasher = IgnoreFieldsHasher(ignored_fields)
    _, kwargs1 = hasher.setup(hello="world")
    _, kwargs2 = hasher.setup(hello="world2")
    assert kwargs1["hello"].__hash__() == kwargs2["hello"].__hash__()
