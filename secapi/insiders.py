"""``client.insiders`` - insider transactions, ownership and activity."""

from __future__ import annotations

from typing import Optional

from ._resource import BaseResource, DateParam
from .models.insider import (
    InsiderBuySellRatioResponse,
    InsiderCompaniesResponse,
    InsiderDailyActivityResponse,
    InsiderHoldingsResponse,
    InsiderHoldingsSummaryResponse,
    InsiderNetSharesResponse,
    InsiderNetValueResponse,
    InsiderOwnersResponse,
    InsiderPerson,
    InsiderPersonsResponse,
    InsiderStatisticsResponse,
    InsiderTransactionsResponse,
)


class Insiders(BaseResource):
    """Form 4 insider transactions, owners, people and activity feeds."""

    def transactions(
        self,
        *,
        ticker: Optional[str] = None,
        person_cik: Optional[str] = None,
        acquired_disposed: Optional[str] = None,
        transaction_code: Optional[str] = None,
        derivative: Optional[bool] = None,
        insider_role: Optional[str] = None,
        min_value: Optional[int] = None,
        limit: Optional[int] = None,
        accepted_from: Optional[DateParam] = None,
        transaction_from: Optional[DateParam] = None,
    ) -> InsiderTransactionsResponse:
        """Insider transactions, globally or scoped to a company / person.

        - default: the cross-company feed
        - ``ticker="AAPL"``: transactions for one company
        - ``person_cik="0001214123"``: transactions for one insider

        ``acquired_disposed`` is ``"A"`` or ``"D"``.
        """
        params = {
            "acquiredDisposed": acquired_disposed,
            "transactionCode": transaction_code,
            "limit": limit,
            "acceptedFrom": accepted_from,
            "transactionFrom": transaction_from,
        }
        if person_cik is not None:
            return self._client._get_model(
                f"/v1/insiders/person/{person_cik}/transactions", params, InsiderTransactionsResponse
            )
        params["derivative"] = derivative
        params["insiderRole"] = insider_role
        params["minValue"] = min_value
        if ticker is not None:
            return self._client._get_model(
                f"/v1/insiders/{ticker}/transactions", params, InsiderTransactionsResponse
            )
        return self._client._get_model("/v1/insiders/transactions", params, InsiderTransactionsResponse)

    #: ``client.insiders.search(...)`` reads naturally; same as ``transactions``.
    search = transactions

    def latest(self, *, ticker: Optional[str] = None, limit: Optional[int] = None) -> InsiderTransactionsResponse:
        """The most recent insider transactions (optionally for one ``ticker``)."""
        return self.transactions(ticker=ticker, limit=limit)

    def buying(
        self,
        *,
        limit: Optional[int] = None,
        start: Optional[DateParam] = None,
        end: Optional[DateParam] = None,
    ) -> InsiderTransactionsResponse:
        """Recent insider buying (acquisition) activity across all companies."""
        params = {"limit": limit, "from": start, "end": end}
        return self._client._get_model("/v1/insiders/activity/buying", params, InsiderTransactionsResponse)

    def selling(
        self,
        *,
        limit: Optional[int] = None,
        start: Optional[DateParam] = None,
        end: Optional[DateParam] = None,
    ) -> InsiderTransactionsResponse:
        """Recent insider selling (disposal) activity across all companies."""
        params = {"limit": limit, "from": start, "end": end}
        return self._client._get_model("/v1/insiders/activity/selling", params, InsiderTransactionsResponse)

    def top_buyers(
        self, *, date: Optional[DateParam] = None, limit: Optional[int] = None
    ) -> InsiderDailyActivityResponse:
        """Issuers ranked by insider buy value on a single date."""
        params = {"date": date, "limit": limit}
        return self._client._get_model(
            "/v1/insiders/activity/daily/top-buyers", params, InsiderDailyActivityResponse
        )

    def top_sellers(
        self, *, date: Optional[DateParam] = None, limit: Optional[int] = None
    ) -> InsiderDailyActivityResponse:
        """Issuers ranked by insider sell value on a single date."""
        params = {"date": date, "limit": limit}
        return self._client._get_model(
            "/v1/insiders/activity/daily/top-sellers", params, InsiderDailyActivityResponse
        )

    def statistics(self) -> InsiderStatisticsResponse:
        """Aggregate insider statistics across all covered issuers."""
        return self._client._get_model("/v1/insiders/statistics", None, InsiderStatisticsResponse)

    def companies(
        self, *, q: Optional[str] = None, limit: Optional[int] = None, page: Optional[int] = None
    ) -> InsiderCompaniesResponse:
        """Directory of companies that have insider (Form 4) filings."""
        params = {"q": q, "limit": limit, "page": page}
        return self._client._get_model("/v1/insiders/companies", params, InsiderCompaniesResponse)

    def persons(
        self, *, q: Optional[str] = None, limit: Optional[int] = None, page: Optional[int] = None
    ) -> InsiderPersonsResponse:
        """Directory or search over insider persons."""
        params = {"q": q, "limit": limit, "page": page}
        return self._client._get_model("/v1/insiders/persons", params, InsiderPersonsResponse)

    # -- by company (ticker) ----------------------------------------------

    def owners(
        self,
        ticker: str,
        *,
        include_derivative: bool = False,
        include_non_derivative: bool = True,
        active_since: Optional[DateParam] = None,
        limit: Optional[int] = None,
    ) -> InsiderOwnersResponse:
        """Reporting owners and beneficial holders at a company."""
        params = {
            "includeDerivative": include_derivative,
            "includeNonDerivative": include_non_derivative,
            "activeSince": active_since,
            "limit": limit,
        }
        return self._client._get_model(f"/v1/insiders/{ticker}/owners", params, InsiderOwnersResponse)

    def buy_sell_ratio(self, ticker: str) -> InsiderBuySellRatioResponse:
        """Lifetime insider buy vs sell transaction counts for a company."""
        return self._client._get_model(
            f"/v1/insiders/{ticker}/buy-sell-ratio", None, InsiderBuySellRatioResponse
        )

    def net_shares(self, ticker: str) -> InsiderNetSharesResponse:
        """Lifetime net insider shares (acquired vs disposed) for a company."""
        return self._client._get_model(f"/v1/insiders/{ticker}/net-shares", None, InsiderNetSharesResponse)

    def net_value(self, ticker: str) -> InsiderNetValueResponse:
        """Lifetime net insider transaction value for a company."""
        return self._client._get_model(f"/v1/insiders/{ticker}/net-value", None, InsiderNetValueResponse)

    # -- by person (CIK) ---------------------------------------------------

    def person(self, cik: str) -> InsiderPerson:
        """Profile for an insider identified by reporting-owner CIK."""
        return self._client._get_model(f"/v1/insiders/person/{cik}", None, InsiderPerson)

    def person_transactions(
        self,
        cik: str,
        *,
        acquired_disposed: Optional[str] = None,
        transaction_code: Optional[str] = None,
        limit: Optional[int] = None,
        accepted_from: Optional[DateParam] = None,
        transaction_from: Optional[DateParam] = None,
    ) -> InsiderTransactionsResponse:
        """Transactions for one insider across companies."""
        return self.transactions(
            person_cik=cik,
            acquired_disposed=acquired_disposed,
            transaction_code=transaction_code,
            limit=limit,
            accepted_from=accepted_from,
            transaction_from=transaction_from,
        )

    def person_holdings(self, cik: str) -> InsiderHoldingsResponse:
        """Current holdings for an insider across issuers."""
        return self._client._get_model(f"/v1/insiders/person/{cik}/holdings", None, InsiderHoldingsResponse)

    def person_holdings_summary(
        self,
        cik: str,
        *,
        include_derivative: bool = True,
        include_non_derivative: bool = True,
    ) -> InsiderHoldingsSummaryResponse:
        """Holdings for an insider, aggregated by issuer."""
        params = {"includeDerivative": include_derivative, "includeNonDerivative": include_non_derivative}
        return self._client._get_model(
            f"/v1/insiders/person/{cik}/holdings/summary", params, InsiderHoldingsSummaryResponse
        )

    def person_ownership(self, cik: str) -> InsiderHoldingsResponse:
        """Current beneficial ownership snapshot for an insider."""
        return self._client._get_model(f"/v1/insiders/person/{cik}/ownership", None, InsiderHoldingsResponse)
