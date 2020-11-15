from lru_cache_http_client.hash.ignore_fields_hasher import (
    IgnoreFieldsHasher,
    _IgnoredField,
)

import pytest


def test_ignore_field_setup_positional_invalid():
    """
    Given: IgnoreFieldsHasher is told to ignore a
           positional arg that is out of bounds when
           setup is called
    Assert: IndexError is raised
    """
    ignored_fields = [0, 1]
    hasher = IgnoreFieldsHasher(ignored_fields)
    with pytest.raises(IndexError):
        hasher.setup("a")


def test_ignore_field_setup_positional():
    """
    Given: IgnoreFieldsHasher is passed an ignored field
           in the setup method for a positional arg twice
    Assert: The hash values for each call on the ignored
            field are the same
    """
    ignored_fields = [0, 1]
    hasher = IgnoreFieldsHasher(ignored_fields)
    args1, _ = hasher.setup("a", "b")
    args2, _ = hasher.setup("d", "e")
    assert args1[0].__hash__() == args2[0].__hash__()
    assert args1[1].__hash__() == args2[1].__hash__()


def test_ignore_field_setup_keyword():
    """
    Given: IgnoreFieldsHasher is passed an ignored field
           in the setup method for a keyword arg twice
    Assert: The hash values for each call on the ignored
            field are the same
    """
    ignored_fields = ["hello"]
    hasher = IgnoreFieldsHasher(ignored_fields)
    _, kwargs1 = hasher.setup(hello="world")
    _, kwargs2 = hasher.setup(hello="world2")
    assert kwargs1["hello"].__hash__() == kwargs2["hello"].__hash__()


def test_ignore_field_teardown_positional():
    """
    Given: IgnoreFieldsHasher is passed an ignored field
           in the teardown method for a positional arg
    Assert: The keyword arg's value is converted back to
            original value
    """
    field = _IgnoredField(1)
    ignored_fields = [0]
    hasher = IgnoreFieldsHasher(ignored_fields)
    args, _ = hasher.teardown(field)
    assert args[0] == 1


def test_ignore_field_teardown_keyword():
    """
    Given: IgnoreFieldsHasher is passed an ignored field
           in the teardown method for a keyword arg
    Assert: The keyword arg's value is converted back to
            original value
    """
    field = _IgnoredField("hello world")
    ignored_fields = ["hello"]
    hasher = IgnoreFieldsHasher(ignored_fields)
    _, kwargs = hasher.teardown(hello=field)
    assert kwargs["hello"] == "hello world"
