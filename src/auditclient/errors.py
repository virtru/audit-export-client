DEFAULT_ERROR_MESSAGE = 'Something went wrong in the auditClient'
INVALID_CREDENTIALS_MESSAGE = 'The provided credentials are Invalid'
NETWORK_ERROR_MESSAGE = 'An error occured while retrieving data'


class AuditClientError(Exception):
    """Base exception for errors raised by AuditClient"""

    def __init__(self, msg):
        msg = DEFAULT_ERROR_MESSAGE if msg is None else msg
        super().__init__(msg)


class InvalidCredentialsError(AuditClientError):
    """The provided credentials are invalid"""

    def __init__(self):
        msg = INVALID_CREDENTIALS_MESSAGE
        super().__init__(msg)


class ClientConnectionError(AuditClientError):
    """An error occured while trying to connect to api"""

    def __init__(self):
        msg = NETWORK_ERROR_MESSAGE
        super().__init__(msg)
