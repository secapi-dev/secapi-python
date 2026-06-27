"""``client.filings`` - query and retrieve SEC filings and documents."""

from __future__ import annotations

from typing import List, Optional

from ._resource import BaseResource, DateParam, FormParam
from .models.filing import (
    Filing,
    FilingDocument,
    FilingFormTypesListResponse,
    FilingsListResponse,
)


class Filings(BaseResource):
    """Search SEC filings and drill into a single filing's documents."""

    def search(
        self,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[FormParam] = None,
        start_date: Optional[DateParam] = None,
        end_date: Optional[DateParam] = None,
        page: int = 1,
        limit: int = 20,
    ) -> FilingsListResponse:
        """Search filings with pagination.

        ``form`` accepts a single form type or a list, e.g. ``form="10-K"`` or
        ``form=["10-K", "8-K", "4"]``.

        Example::

            client.filings.search(ticker="AAPL", form="10-K")
        """
        params = {
            "ticker": ticker,
            "cik": cik,
            "formTypes": form,
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "limit": limit,
        }
        return self._client._get_model("/v1/filings", params, FilingsListResponse)

    def get(self, accession_number: str) -> List[Filing]:
        """Return every filing matching an SEC accession number."""
        return self._client._get_list(f"/v1/filings/{accession_number}", None, Filing)

    def retrieve(self, cik: str, accession_number: str) -> Filing:
        """Return a single filing identified by CIK + accession number."""
        return self._client._get_model(f"/v1/filings/{cik}/{accession_number}", None, Filing)

    def documents(self, cik: str, accession_number: str) -> List[FilingDocument]:
        """List the documents that belong to a filing."""
        return self._client._get_list(
            f"/v1/filings/{cik}/{accession_number}/documents", None, FilingDocument
        )

    def form_types(self, *, page: int = 1, limit: int = 20) -> FilingFormTypesListResponse:
        """List the active SEC form types available for filtering."""
        params = {"page": page, "limit": limit}
        return self._client._get_model("/v1/filings/form-types", params, FilingFormTypesListResponse)
