"""Typed exceptions raised by the SEC API SDK.

Instead of leaking raw HTTP errors, the client raises a small, predictable
hierarchy so you can handle problems precisely::

    from secapi import SECClient
    from secapi.exceptions import AuthenticationError, RateLimitError, NotFoundError

    client = SECClient(api_key="...")
    try:
        client.filings.search(ticker="AAPL")
    except RateLimitError as exc:
        ...  # back off and retry
    except AuthenticationError:
        ...  # bad / missing key
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Type


class SecApiError(Exception):
    """Base class for every error raised by this SDK."""


class APIConnectionError(SecApiError):
    """The request never produced a response (DNS, TCP, TLS, etc.)."""

    def __init__(self, message: str = "Could not connect to the SEC API.", *, cause: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.__cause__ = cause


class APITimeoutError(APIConnectionError):
    """The request timed out before a response was received."""

    def __init__(self, message: str = "Request to the SEC API timed out.", *, cause: Optional[BaseException] = None) -> None:
        super().__init__(message, cause=cause)


class APIStatusError(SecApiError):
    """The API returned a non-success HTTP status code."""

    #: Default message used when the response body has none.
    _default_message = "The SEC API returned an error."

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        status_code: int,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        body: Any = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        self.request_id = request_id
        self.body = body
        message = message or self._default_message
        if request_id:
            super().__init__(f"{message} (status={status_code}, request_id={request_id})")
        else:
            super().__init__(f"{message} (status={status_code})")
        self.message = message


class BadRequestError(APIStatusError):
    """400 - the request was malformed or failed validation."""

    _default_message = "The request was invalid. Check your parameters and try again."


#: Alias: a 400 from this API is a request-validation failure.
ValidationError = BadRequestError


class AuthenticationError(APIStatusError):
    """401 - the API key is missing or invalid."""

    _default_message = "Invalid or missing API key."


class PermissionDeniedError(APIStatusError):
    """403 - the key is valid but not allowed (expired, revoked, plan gate)."""

    _default_message = "Your API key does not have access to this resource."


class NotFoundError(APIStatusError):
    """404 - the requested resource does not exist."""

    _default_message = "The requested resource was not found."


class RateLimitError(APIStatusError):
    """429 - you exceeded your plan's request limit."""

    _default_message = "API rate limit exceeded for your plan."


class ServerError(APIStatusError):
    """5xx - something went wrong on the SEC API side."""

    _default_message = "The SEC API had an internal error. Please retry shortly."


_STATUS_TO_EXCEPTION = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    429: RateLimitError,
}


def _parse_error_body(body: Any) -> Dict[str, Optional[Any]]:
    """Pull ``code``/``message``/``details``/``request_id`` out of the body.

    The API wraps errors as ``{"error": {code, message, details, request_id}}``.
    """
    info: Dict[str, Optional[Any]] = {"code": None, "message": None, "details": None, "request_id": None}
    if isinstance(body, dict):
        error = body.get("error") if isinstance(body.get("error"), dict) else body
        if isinstance(error, dict):
            info["code"] = error.get("code")
            info["message"] = error.get("message")
            info["details"] = error.get("details")
            info["request_id"] = error.get("request_id") or error.get("requestId")
    return info


def make_status_error(status_code: int, *, body: Any = None, request_id: Optional[str] = None) -> APIStatusError:
    """Build the most specific exception for an HTTP status code."""
    info = _parse_error_body(body)
    exc_cls: Type[APIStatusError]
    if status_code >= 500:
        exc_cls = ServerError
    else:
        exc_cls = _STATUS_TO_EXCEPTION.get(status_code, APIStatusError)
    return exc_cls(
        info["message"],
        status_code=status_code,
        code=info["code"],
        details=info["details"],
        request_id=info["request_id"] or request_id,
        body=body,
    )
