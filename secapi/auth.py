"""API key resolution and request authentication.

The SEC API authenticates with an API key sent in the ``x-api-key`` header.
Keys look like ``fs_live_...`` (production) or ``fs_test_...`` (test mode).
"""

from __future__ import annotations

import os
from typing import Dict, Optional

#: Header the SEC API expects the key in.
API_KEY_HEADER = "x-api-key"

#: Environment variables checked, in order, when no key is passed explicitly.
ENV_VARS = ("SECAPI_API_KEY", "SEC_API_KEY")


class MissingAPIKeyError(ValueError):
    """Raised when no API key can be resolved from arguments or the environment."""

    def __init__(self) -> None:
        super().__init__(
            "No API key provided. Pass api_key=... to SECClient(), or set the "
            "SECAPI_API_KEY environment variable. Get a key at https://secapi.dev."
        )


def resolve_api_key(explicit: Optional[str] = None) -> str:
    """Return the API key from the explicit argument or the environment.

    Raises :class:`MissingAPIKeyError` if none is found.
    """
    if explicit and explicit.strip():
        return explicit.strip()
    for var in ENV_VARS:
        value = os.environ.get(var)
        if value and value.strip():
            return value.strip()
    raise MissingAPIKeyError()


def auth_headers(api_key: str) -> Dict[str, str]:
    """Build the authentication header(s) for a request."""
    return {API_KEY_HEADER: api_key}
