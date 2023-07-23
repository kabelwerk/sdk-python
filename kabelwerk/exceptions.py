class KabelwerkException(Exception):
    """
    The base class for all Kabelwerk exceptions.
    """
    pass


class ConnectionError(KabelwerkException):
    """
    Raised when there is an issue with the connection to the Kabelwerk backend.


    Attributes
    ----------

    request
        The failed request.

    cause
        The underlying error.

    """

    def __init__(self, error):
        self.request = error.request
        self.cause = error


class AuthenticationError(KabelwerkException):
    """
    Raised when the authentication token is rejected by the Kabelwerk backend.


    Attributes
    ----------

    request
        The failed request.

    response
        The Kabelwerk backend's response.

    """

    def __init__(self, response):
        self.request = response.request
        self.response = response


class ValidationError(KabelwerkException):
    """
    Raised when the input data is rejected by the Kabelwerk backend as invalid.


    Attributes
    ----------

    request
        The failed request.

    response
        The Kabelwerk backend's response.

    field
        The argument which failed the validation.

    error_message
        Description of the error.

    """

    def __init__(self, response, field, error_message):
        self.request = response.request
        self.response = response

        self.field = field
        self.error_message = error_message


class ServerError(KabelwerkException):
    """
    Raised when the Kabelwerk backend fails to handle the request or behaves in
    an unexpected way.


    Attributes
    ----------

    request
        The failed request.

    response
        The Kabelwerk backend's response.

    """

    def __init__(self, response):
        self.request = response.request
        self.response = response
