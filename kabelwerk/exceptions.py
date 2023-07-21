class KabelwerkException(Exception):
    """
    The base class for all Kabelwerk exceptions.
    """
    pass


class ConnectionError(KabelwerkException):
    """
    Raised when there is an issue with the connection to the Kabelwerk backend.
    """
    pass


class AuthenticationError(KabelwerkException):
    """
    Raised when the authentication token is rejected by the Kabelwerk backend.
    """
    pass


class ValidationError(KabelwerkException):
    """
    Raised when the input data is rejected by the Kabelwerk backend as invalid.
    """
    pass


class ServerError(KabelwerkException):
    """
    Raised when the Kabelwerk backend fails to handle the request or behaves in
    an unexpected way.
    """
    pass
