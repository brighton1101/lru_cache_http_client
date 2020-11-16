from typing import Optional


class HttpClient:
    """
    Template interface for valid HttpClients used by the application
    """

    def get(self, url: str, params: Optional[dict] = None, **kwargs):
        pass

    @staticmethod
    def validate_http_client(http_client):
        assert isinstance(http_client, HttpClient), "Invalid instance of HttpClient"
