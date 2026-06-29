"""The public SEC API client."""

from __future__ import annotations

from typing import Mapping, Optional, Union

import httpx

from ._base_client import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, BaseSECClient
from .entities import Entities
from .filings import Filings
from .financials import Financials
from .insiders import Insiders
from .institutions import Institutions


class SECClient(BaseSECClient):
    """Entry point to the SEC API (https://secapi.dev).

    Example::

        from secapi import SECClient

        client = SECClient(api_key="YOUR_API_KEY")
        filings = client.filings.search(ticker="AAPL", form="10-K")
        for filing in filings.data:
            print(filing.filing_date, filing.form_type, filing.accession_number)

    The API key is read from ``api_key=`` or, if omitted, the ``SECAPI_API_KEY``
    environment variable. The client is safe to reuse across many requests; it
    keeps a pooled HTTP/2 connection open until you ``close()`` it (or use it as
    a context manager).

    Attributes:
        api_key: The resolved API key sent on every request.
        base_url: The API base URL.
        session: The underlying :class:`httpx.Client`.
    """

    #: SEC registrants (CIK, ticker, entity class).
    entities: Entities
    #: SEC filings and filing documents.
    filings: Filings
    #: Company financials, statements, metrics, ratios and segments.
    financials: Financials
    #: Insider transactions, ownership and activity.
    insiders: Insiders
    #: 13F institutional investors and holdings.
    institutions: Institutions

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Union[float, httpx.Timeout, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http2: bool = True,
        default_headers: Optional[Mapping[str, str]] = None,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        super().__init__(
            api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http2=http2,
            default_headers=default_headers,
            transport=transport,
        )
        self.entities = Entities(self)
        self.filings = Filings(self)
        self.financials = Financials(self)
        self.insiders = Insiders(self)
        self.institutions = Institutions(self)

    def __enter__(self) -> "SECClient":
        return self
