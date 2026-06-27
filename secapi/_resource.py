"""Shared base + type aliases for resource namespaces."""

from __future__ import annotations

import datetime
from typing import Sequence, Union

from ._base_client import BaseSECClient

#: A date accepted as either an ISO string ("2025-01-31") or a ``date``.
DateParam = Union[str, datetime.date]

#: A form-type filter: one form ("10-K") or several (["10-K", "8-K"]).
FormParam = Union[str, Sequence[str]]

#: A symbol/ratio filter: one value or several (joined with commas).
ListParam = Union[str, Sequence[str]]


class BaseResource:
    """Base class for every resource namespace (``client.filings`` etc.)."""

    def __init__(self, client: BaseSECClient) -> None:
        self._client = client
