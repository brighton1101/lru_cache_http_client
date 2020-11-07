class Hasher:
    """
    Interface for creating hashes for application
    """

    def get_hash(self, *args, **kwargs):
        """
        By default, return 0. This allows us to inject a dummy hasher
        for objects that we want to have the 'same' hash
        """
        return 0
