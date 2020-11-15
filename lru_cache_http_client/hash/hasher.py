class Hasher:
    """
    Interface for creating hashes for application
    """

    def setup(self, *args, **kwargs):
        return args, kwargs

    def teardown(self, *args, **kwargs):
        return args, kwargs
