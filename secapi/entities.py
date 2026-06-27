"""``client.entities`` - SEC registrants (CIK, ticker, entity class)."""

from __future__ import annotations

from typing import Optional

from ._resource import BaseResource, DateParam, FormParam
from .models.entity import EntitiesListResponse, Entity, EntitySicListResponse
from .models.filing import FilingsListResponse


class Entities(BaseResource):
    """Look up SEC entities and the filings that belong to them."""

    def list(
        self,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        entity_type: Optional[str] = None,
        q: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> EntitiesListResponse:
        """List entities, optionally filtered by ticker, CIK, class or name.

        ``entity_type`` is one of ``company``, ``individual``, ``institution``.
        ``q`` does a case-insensitive substring match on the entity name.
        """
        params = {
            "ticker": ticker,
            "cik": cik,
            "entityType": entity_type,
            "q": q,
            "page": page,
            "limit": limit,
        }
        return self._client._get_model("/v1/entities", params, EntitiesListResponse)

    def get(self, identifier: str) -> Entity:
        """Fetch one entity by CIK (digits) or ticker symbol.

        Example::

            client.entities.get("AAPL")
            client.entities.get("0000320193")
        """
        return self._client._get_model(f"/v1/entities/{identifier}", None, Entity)

    def filings(
        self,
        identifier: str,
        *,
        form: Optional[FormParam] = None,
        start_date: Optional[DateParam] = None,
        end_date: Optional[DateParam] = None,
        page: int = 1,
        limit: int = 20,
    ) -> FilingsListResponse:
        """List filings for an entity resolved by CIK or ticker."""
        params = {
            "formTypes": form,
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "limit": limit,
        }
        return self._client._get_model(f"/v1/entities/{identifier}/filings", params, FilingsListResponse)

    def sic_codes(self, *, page: int = 1, limit: int = 20) -> EntitySicListResponse:
        """List SEC Standard Industrial Classification (SIC) codes."""
        params = {"page": page, "limit": limit}
        return self._client._get_model("/v1/entities/sic-codes", params, EntitySicListResponse)
