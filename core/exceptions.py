from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseError(Exception, ABC):
    """
    Base class for custom exceptions.

    This class provides a template for other exceptions with
    a standard structure for logging and error handling.
    """

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize the error.

        Parameters
        ----------
        message : str
            Descriptive error message.
        context : Optional[Dict[str, Any]]
            Additional context related to the error, if any.
        """
        super().__init__(message)
        self.message = message
        self.context = context

    @property
    @abstractmethod
    def code(self) -> str:
        """Error code representing this specific error."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the error."""
        ...


class HTTPError(BaseError):
    """
    Base class for HTTP-related exceptions.
    """

    @property
    @abstractmethod
    def status_code(self) -> int:
        """HTTP status code associated with this error."""
        ...


class DuplicatedError(HTTPError):
    """
    Exception for resource duplication errors.
    """

    @property
    def code(self) -> str:
        return "DUPLICATED_ERROR"

    @property
    def description(self) -> str:
        return "The resource already exists."

    @property
    def status_code(self) -> int:
        return 409


class AuthError(HTTPError):
    """
    Exception for authentication errors.
    """

    @property
    def code(self) -> str:
        return "AUTH_ERROR"

    @property
    def description(self) -> str:
        return "Authentication failed or unauthorized access."

    @property
    def status_code(self) -> int:
        return 401


class NotFoundError(HTTPError):
    """
    Exception for resource not found errors.
    """

    @property
    def code(self) -> str:
        return "NOT_FOUND_ERROR"

    @property
    def description(self) -> str:
        return "The requested resource was not found."

    @property
    def status_code(self) -> int:
        return 404
