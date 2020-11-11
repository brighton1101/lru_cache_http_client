class HttpClient:
    """
    Template interface for valid HttpClients used by the application
    """

    def get(self, url, params=None, **kwargs):
        pass

    def make_args_hashable(self, params=None, **kwargs):
        """
        Given keyword args, make them all hashable
        """
        return params, kwargs
