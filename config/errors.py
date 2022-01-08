class ApplicationException(Exception):
    """
    Base class for all application exceptions
    """

    def __init__(self, message=None, status_code=None, payload=None, name=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.name = name


class UserNotFoundException(ApplicationException):
    """
    Thrown if user doesn't exist
    """

    def __init__(self, payload=None):
        super().__init__(message="User does not exists",
                         status_code=404,
                         payload=payload,
                         name="UserNotFoundException")


class UserAlreadyExistsException(ApplicationException):
    """
    Thrown if user already exist while creating new
    """

    def __init__(self, payload=None):
        super().__init__(message="User already exists with provided username",
                         status_code=409,
                         payload=payload,
                         name="UserAlreadyExistsException")


class InvalidUserCredentialsException(ApplicationException):
    """
    Thrown if Invalid credentials are supplied
    """

    def __init__(self, payload=None):
        super().__init__(message="Invalid username/password combination",
                         status_code=401,
                         payload=payload,
                         name="InvalidUserCredentialsException")


class InvalidPlayerIdException(ApplicationException):
    """
    Thrown when player not found
    """

    def __init__(self, payload=None):
        super().__init__(message="No player with given player ID exists on your team",
                         status_code=404,
                         payload=payload,
                         name="InvalidPlayerIdException")


class InvalidTransferException(ApplicationException):
    """
    Thrown if user tries to transfer a player already on team
    """

    def __init__(self, payload=None):
        super().__init__(message="Invalid transfer request. Requested player already on team",
                         status_code=400,
                         payload=payload,
                         name="InvalidTransferException")


class InsufficientFundsException(ApplicationException):
    """
    Thrown if ask price is more than available cash
    """

    def __init__(self):
        super().__init__(message="Insufficient funds",
                         status_code=400,
                         name="InsufficientFundsException")


class InvalidCountryNameException(ApplicationException):
    """
    Thrown if ask price is more than available cash
    """

    def __init__(self, payload=None):
        super().__init__(message="Invalid country name specified",
                         status_code=422,
                         name="InvalidCountryNameException",
                         payload=payload)
