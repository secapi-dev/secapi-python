"""``client.institutions`` - 13F institutional investors and their holdings."""

from __future__ import annotations

from typing import Optional

from ._resource import BaseResource
from .models.institution import (
    Institution,
    InstitutionChangesResponse,
    InstitutionFiling,
    InstitutionFilingPeriodsResponse,
    InstitutionFilingsResponse,
    InstitutionPortfolioCompositionResponse,
    InstitutionProfileResponse,
    InstitutionsActivityResponse,
    InstitutionsHoldingsHistoryResponse,
    InstitutionsHoldingsResponse,
    InstitutionsListResponse,
    InstitutionTradingActivityResponse,
)


class Institutions(BaseResource):
    """Form 13F managers: portfolios, holdings, flows and market activity."""

    def list(
        self, *, q: Optional[str] = None, limit: Optional[int] = None, page: Optional[int] = None
    ) -> InstitutionsListResponse:
        """List institutional managers that file Form 13F."""
        params = {"q": q, "limit": limit, "page": page}
        return self._client._get_model("/v1/institutions", params, InstitutionsListResponse)

    def get(self, cik: str) -> Institution:
        """Fetch a single institution by CIK."""
        return self._client._get_model(f"/v1/institutions/{cik}", None, Institution)

    def profile(self, cik: str, *, quarter: Optional[str] = None) -> InstitutionProfileResponse:
        """Profile for a manager (portfolio value, position counts, etc.)."""
        params = {"quarter": quarter}
        return self._client._get_model(f"/v1/institutions/{cik}/profile", params, InstitutionProfileResponse)

    def activity(
        self, *, year: Optional[int] = None, quarter: Optional[str] = None, limit: Optional[int] = None
    ) -> InstitutionsActivityResponse:
        """Market-wide smart-money activity (most bought/sold, new/closed)."""
        params = {"year": year, "quarter": quarter, "limit": limit}
        return self._client._get_model("/v1/institutions/activity", params, InstitutionsActivityResponse)

    # -- filings -----------------------------------------------------------

    def filings(
        self,
        cik: str,
        *,
        quarter: Optional[str] = None,
        form_type: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> InstitutionFilingsResponse:
        """Form 13F filings for a manager."""
        params = {"quarter": quarter, "formType": form_type, "limit": limit, "page": page}
        return self._client._get_model(f"/v1/institutions/{cik}/filings", params, InstitutionFilingsResponse)

    def filing(self, cik: str, accession_number: str) -> InstitutionFiling:
        """A single Form 13F filing by accession number."""
        return self._client._get_model(
            f"/v1/institutions/{cik}/filings/{accession_number}", None, InstitutionFiling
        )

    def filing_periods(self, cik: str, *, year: Optional[int] = None) -> InstitutionFilingPeriodsResponse:
        """Quarterly Form 13F filing coverage for a manager."""
        params = {"year": year}
        return self._client._get_model(
            f"/v1/institutions/{cik}/filing-periods", params, InstitutionFilingPeriodsResponse
        )

    # -- holdings ----------------------------------------------------------

    def holdings(
        self,
        cik: str,
        *,
        quarter: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> InstitutionsHoldingsResponse:
        """Portfolio positions for a manager. ``sort`` is value/shares/weight."""
        params = {"quarter": quarter, "limit": limit, "sort": sort}
        return self._client._get_model(f"/v1/institutions/{cik}/holdings", params, InstitutionsHoldingsResponse)

    def holdings_history(
        self,
        cik: str,
        *,
        year: Optional[int] = None,
        quarter: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> InstitutionsHoldingsHistoryResponse:
        """Holdings across filing periods (quarterly snapshots)."""
        params = {"year": year, "quarter": quarter, "limit": limit, "sort": sort}
        return self._client._get_model(
            f"/v1/institutions/{cik}/holdings/history", params, InstitutionsHoldingsHistoryResponse
        )

    # -- flows & composition ----------------------------------------------

    def changes(self, cik: str, *, quarter: Optional[str] = None) -> InstitutionChangesResponse:
        """Quarter-over-quarter portfolio change metrics for a manager."""
        params = {"quarter": quarter}
        return self._client._get_model(f"/v1/institutions/{cik}/changes", params, InstitutionChangesResponse)

    def buys(
        self,
        cik: str,
        *,
        quarter: Optional[str] = None,
        new_only: Optional[bool] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> InstitutionTradingActivityResponse:
        """Securities a manager increased vs the prior quarter."""
        params = {"quarter": quarter, "newOnly": new_only, "limit": limit, "page": page}
        return self._client._get_model(f"/v1/institutions/{cik}/buys", params, InstitutionTradingActivityResponse)

    def sells(
        self,
        cik: str,
        *,
        quarter: Optional[str] = None,
        sold_out_only: Optional[bool] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> InstitutionTradingActivityResponse:
        """Securities a manager decreased vs the prior quarter."""
        params = {"quarter": quarter, "soldOutOnly": sold_out_only, "limit": limit, "page": page}
        return self._client._get_model(f"/v1/institutions/{cik}/sells", params, InstitutionTradingActivityResponse)

    def sectors(self, cik: str, *, quarter: Optional[str] = None) -> InstitutionPortfolioCompositionResponse:
        """Portfolio breakdown by sector."""
        params = {"quarter": quarter}
        return self._client._get_model(
            f"/v1/institutions/{cik}/sectors", params, InstitutionPortfolioCompositionResponse
        )

    def industries(self, cik: str, *, quarter: Optional[str] = None) -> InstitutionPortfolioCompositionResponse:
        """Portfolio breakdown by industry / SIC."""
        params = {"quarter": quarter}
        return self._client._get_model(
            f"/v1/institutions/{cik}/industries", params, InstitutionPortfolioCompositionResponse
        )
