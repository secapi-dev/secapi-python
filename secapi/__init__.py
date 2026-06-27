"""secapi - the official Python SDK for the SEC API (https://secapi.dev).

Quickstart::

    from secapi import SECClient

    client = SECClient(api_key="YOUR_API_KEY")
    results = client.filings.search(ticker="AAPL", form="10-K")
    print(results)
"""

from __future__ import annotations

from . import models
from ._version import __version__
from .client import SECClient
from .exceptions import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    SecApiError,
    ServerError,
    ValidationError,
)

__all__ = [
    "SECClient",
    "__version__",
    "models",
    # exceptions
    "SecApiError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "ValidationError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]
