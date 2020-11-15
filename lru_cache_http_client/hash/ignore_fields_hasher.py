from typing import Union, List


class IgnoreFieldsHasher:
    """
    Hasher implementation for ignoring arguments
    """

    ignored_fields: List[Union[int, str]] = []

    def __init__(self, fields: List[Union[int, str]]):
        self.ignored_fields = fields

    def setup(self, *args, **kwargs):
        args = list(args)
        for field in self.ignored_fields:
            if isinstance(field, int):
                if field >= len(args):
                    raise IndexError("Arg at that position does not exist")
                args[field] = _IgnoredField(args[field])
            elif isinstance(field, str):
                kwargs[field] = _IgnoredField(kwargs[field])
            else:
                raise IndexError("Invalid ignored field")
        return tuple(args), kwargs

    def teardown(self, *args, **kwargs):
        args = list(args)
        for field in self.ignored_fields:
            if isinstance(field, int):
                args[field] = args[field].ignored_val
            else:
                kwargs[field] = kwargs[field].ignored_val
        return tuple(args), kwargs


class _IgnoredField:

    ignored_val = None

    def __init__(self, ignored_val):
        self.ignored_val = ignored_val

    def __hash__(self):
        return 0
