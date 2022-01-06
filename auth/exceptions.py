from config.errors import ApplicationException


class InvalidHeaderError(ApplicationException):
    """
    An error raised when the expected header format does not match what was received
    """
    def __init__(self, payload=None):
        super().__init__(message="Missing/Invalid request headers",
                         status_code=400,
                         payload=payload,
                         name="InvalidHeaderError")


class NoAuthorizationError(ApplicationException):
    """
    An error raised when no JWT was found when a protected endpoint was accessed
    """
    def __init__(self, payload=None):
        super().__init__(message="Unauthorised request",
                         status_code=401,
                         payload=payload,
                         name="NoAuthorizationError")
