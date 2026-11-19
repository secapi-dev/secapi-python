"""``client.financials`` - company financials derived from SEC XBRL data."""

from __future__ import annotations

import datetime
from typing import Optional

from ._resource import BaseResource, DateParam, ListParam
from .models.financial import (
    CanonicalBalanceSheet,
    CanonicalCashFlow,
    CanonicalIncomeStatement,
    CompaniesSearchResponse,
    CompanyFinancialStatement,
    CompanyLatestFinancialsResponse,
    CompanySharesOutstandingResponse,
    CompanyStandardizedStatementsResponse,
    ConceptsListResponse,
    FinancialMetricRankingResponse,
    FinancialMetricSeriesResponse,
    FinancialRatioRankingResponse,
    FinancialRatioSeriesResponse,
    FinancialSegmentResponse,
    FinancialXbrl,
)

_STATEMENTS_BASE = "/v1/financials/filings/{accession}/statements"

#: Marks a ``form`` the by-company statement endpoint cannot filter on.
_OTHER_FORM = "other"


def _period_for_form(form: Optional[str]) -> Optional[str]:
    """``None`` for no form filter, annual / quarterly for 10-K / 10-Q, else ``_OTHER_FORM``."""
    if not form:
        return None
    upper = form.strip().upper()
    if upper == "10-K":
        return "annual"
    if upper == "10-Q":
        return "quarterly"
    return _OTHER_FORM


class Financials(BaseResource):
    """Financial statements, standardized metrics, ratios and segments."""

    # -- reference / lookup ------------------------------------------------

    def companies(
        self,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        limit: int = 25,
        page: int = 1,
    ) -> CompaniesSearchResponse:
        """Resolve a company and list its filings by ticker or CIK."""
        params = {"ticker": ticker, "cik": cik, "limit": limit, "page": page}
        return self._client._get_model("/v1/financials/companies/search", params, CompaniesSearchResponse)

    def concepts(
        self,
        q: str,
        *,
        version: Optional[str] = None,
        custom: Optional[bool] = None,
        limit: int = 50,
        page: int = 1,
    ) -> ConceptsListResponse:
        """Search XBRL concepts (line-item names) by label, code or taxonomy."""
        params = {"q": q, "version": version, "custom": custom, "limit": limit, "page": page}
        return self._client._get_model("/v1/financials/concepts/search", params, ConceptsListResponse)

    # -- by company (ticker or CIK, no accession number needed) ------------

    def latest(self, issuer: str, *, period: Optional[str] = None) -> CompanyLatestFinancialsResponse:
        """The company's most recent 10-K or 10-Q, standardized, in one response.

        Returns the filing with its income statement, balance sheet and cash
        flow. ``issuer`` is a ticker or a CIK. ``period`` is ``"annual"`` (10-K)
        or ``"quarterly"`` (10-Q); omit it for whichever is most recent. A
        statement is ``None`` when it could not be standardized for that filing.

        Example::

            latest = client.financials.latest("AAPL")
            latest.income_statement.metrics["revenue"]
        """
        return self._client._get_model(
            f"/v1/financials/{issuer}/latest", {"period": period}, CompanyLatestFinancialsResponse
        )

    def filings(
        self,
        issuer: str,
        *,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> CompaniesSearchResponse:
        """Annual and quarterly filings of a company, newest first."""
        params = {"limit": limit, "page": page}
        return self._client._get_model(f"/v1/financials/{issuer}/filings", params, CompaniesSearchResponse)

    def company_statement(
        self,
        issuer: str,
        statement: str,
        *,
        period: Optional[str] = None,
    ) -> CompanyFinancialStatement:
        """A statement as filed, from the company's latest filing that has it.

        ``statement`` is one of ``income-statement``, ``balance-sheet``,
        ``cash-flow``, ``stockholders-equity`` or ``comprehensive-income``.
        ``period`` restricts the filing to ``"annual"`` or ``"quarterly"``.
        """
        return self._client._get_model(
            f"/v1/financials/{issuer}/statements/{statement}", {"period": period}, CompanyFinancialStatement
        )

    def statement_history(
        self,
        issuer: str,
        statement: str,
        *,
        period: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> CompanyStandardizedStatementsResponse:
        """Standardized statement history: the most recent periods, newest first.

        ``statement`` is ``income-statement``, ``balance-sheet`` or
        ``cash-flow``. ``period`` is ``"annual"`` (fiscal years), ``"quarterly"``
        (single quarters) or ``"ytd"`` (year-to-date spans from quarterly
        filings - the complete series for cash flow, which 10-Qs report year
        to date). ``limit`` is 1-40 periods. A restated period comes from the
        latest filing that reports it.

        Example::

            client.financials.statement_history("AAPL", "income-statement", period="annual", limit=5)
        """
        params = {"period": period, "limit": limit}
        return self._client._get_model(
            f"/v1/financials/{issuer}/statements/{statement}/standardized",
            params,
            CompanyStandardizedStatementsResponse,
        )

    def shares_outstanding(
        self, *, ticker: Optional[str] = None, cik: Optional[str] = None
    ) -> CompanySharesOutstandingResponse:
        """Latest reported shares outstanding (``cik`` takes precedence over ``ticker``)."""
        params = {"ticker": ticker, "cik": cik}
        return self._client._get_model(
            "/v1/financials/shares-outstanding", params, CompanySharesOutstandingResponse
        )

    # -- as-reported statements (by accession or ticker/cik) ---------------

    def income_statement(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
    ) -> CompanyFinancialStatement:
        """As-reported income statement for a filing.

        Pass an ``accession_number`` directly, or pass ``ticker=`` / ``cik=``
        to use that company's most recent filing (optionally ``form="10-K"``).

        Example::

            client.financials.income_statement(ticker="MSFT")
            client.financials.income_statement("0000320193-26-000006")
        """
        return self._statement_for("income-statement", accession_number, ticker=ticker, cik=cik, form=form)

    def balance_sheet(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
    ) -> CompanyFinancialStatement:
        """As-reported balance sheet for a filing (by accession or ticker/cik)."""
        return self._statement_for("balance-sheet", accession_number, ticker=ticker, cik=cik, form=form)

    def cash_flow(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
    ) -> CompanyFinancialStatement:
        """As-reported cash flow statement (by accession or ticker/cik)."""
        return self._statement_for("cash-flow", accession_number, ticker=ticker, cik=cik, form=form)

    def stockholders_equity(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
    ) -> CompanyFinancialStatement:
        """As-reported stockholders' equity statement (by accession or ticker/cik)."""
        return self._statement_for("stockholders-equity", accession_number, ticker=ticker, cik=cik, form=form)

    def comprehensive_income(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
    ) -> CompanyFinancialStatement:
        """As-reported comprehensive income statement (by accession or ticker/cik)."""
        return self._statement_for("comprehensive-income", accession_number, ticker=ticker, cik=cik, form=form)

    def xbrl(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
        role_uri: Optional[str] = None,
    ) -> FinancialXbrl:
        """Raw XBRL statement blocks for a filing (optionally one section)."""
        accession = self._require_accession(accession_number, ticker=ticker, cik=cik, form=form)
        params = {"roleUri": role_uri}
        return self._client._get_model(
            f"/v1/financials/filings/{accession}/xbrl", params, FinancialXbrl
        )

    # -- standardized statements (paid feature) ----------------------------

    def income_statement_standardized(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
        end_date: Optional[int] = None,
        qtrs: Optional[int] = None,
    ) -> CanonicalIncomeStatement:
        """Standardized (canonical) income statement. ``end_date`` is YYYYMMDD."""
        accession = self._require_accession(accession_number, ticker=ticker, cik=cik, form=form)
        params = {"endDate": end_date, "qtrs": qtrs}
        return self._client._get_model(
            f"{_STATEMENTS_BASE.format(accession=accession)}/income-statement/standardized",
            params,
            CanonicalIncomeStatement,
        )

    def balance_sheet_standardized(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
        end_date: Optional[int] = None,
    ) -> CanonicalBalanceSheet:
        """Standardized (canonical) balance sheet. ``end_date`` is YYYYMMDD."""
        accession = self._require_accession(accession_number, ticker=ticker, cik=cik, form=form)
        params = {"endDate": end_date}
        return self._client._get_model(
            f"{_STATEMENTS_BASE.format(accession=accession)}/balance-sheet/standardized",
            params,
            CanonicalBalanceSheet,
        )

    def cash_flow_standardized(
        self,
        accession_number: Optional[str] = None,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        form: Optional[str] = None,
        end_date: Optional[int] = None,
        qtrs: Optional[int] = None,
    ) -> CanonicalCashFlow:
        """Standardized (canonical) cash flow statement. ``end_date`` is YYYYMMDD."""
        accession = self._require_accession(accession_number, ticker=ticker, cik=cik, form=form)
        params = {"endDate": end_date, "qtrs": qtrs}
        return self._client._get_model(
            f"{_STATEMENTS_BASE.format(accession=accession)}/cash-flow/standardized",
            params,
            CanonicalCashFlow,
        )

    # -- company analytics -------------------------------------------------

    def metrics(
        self,
        symbols: ListParam,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        source: str = "all",
        version: Optional[str] = None,
        start_date: Optional[DateParam] = None,
        end_date: Optional[DateParam] = None,
        qtrs: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialMetricSeriesResponse:
        """Time series of raw and/or canonical metrics for one company.

        ``symbols`` is one metric or a list (e.g. ``["revenue", "net_income"]``).
        ``source`` is ``raw``, ``canonical`` or ``all``. Provide ``ticker`` or ``cik``.
        """
        params = {
            "ticker": ticker,
            "cik": cik,
            "symbols": symbols,
            "source": source,
            "version": version,
            "startDate": start_date,
            "endDate": end_date,
            "qtrs": qtrs,
            "limit": limit,
        }
        return self._client._get_model("/v1/financials/metrics", params, FinancialMetricSeriesResponse)

    def top_metrics(
        self,
        metric: str,
        *,
        quarterly: Optional[bool] = None,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialMetricRankingResponse:
        """Rank companies by a canonical metric (e.g. ``metric="revenue"``)."""
        params = {"metric": metric, "quarterly": quarterly, "year": year, "quarter": quarter, "limit": limit}
        return self._client._get_model("/v1/financials/metrics/top", params, FinancialMetricRankingResponse)

    def ratios(
        self,
        *,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        ratio: Optional[ListParam] = None,
        group: Optional[str] = None,
        start_date: Optional[DateParam] = None,
        end_date: Optional[DateParam] = None,
        qtrs: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialRatioSeriesResponse:
        """Precalculated financial ratios for one company.

        ``ratio`` is one or more identifiers (e.g. ``["gross_margin", "current_ratio"]``);
        omit it and pass ``group`` (liquidity/leverage/profitability/efficiency/all) instead.
        """
        params = {
            "ticker": ticker,
            "cik": cik,
            "ratio": ratio,
            "group": group,
            "startDate": start_date,
            "endDate": end_date,
            "qtrs": qtrs,
            "limit": limit,
        }
        return self._client._get_model("/v1/financials/ratios", params, FinancialRatioSeriesResponse)

    def top_ratios(
        self,
        ratio: str,
        *,
        group: Optional[str] = None,
        start_date: Optional[DateParam] = None,
        end_date: Optional[DateParam] = None,
        qtrs: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialRatioRankingResponse:
        """Rank companies by a single calculated ratio (e.g. ``"gross_margin"``)."""
        params = {
            "ratio": ratio,
            "group": group,
            "startDate": start_date,
            "endDate": end_date,
            "qtrs": qtrs,
            "limit": limit,
        }
        return self._client._get_model("/v1/financials/ratios/top", params, FinancialRatioRankingResponse)

    # -- segments ----------------------------------------------------------

    def segments(
        self,
        issuer: str,
        *,
        metric: Optional[str] = None,
        axis: Optional[str] = None,
        segment_type: Optional[str] = None,
        period: Optional[str] = None,
        qtrs: Optional[int] = None,
        accession_number: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> FinancialSegmentResponse:
        """Revenue segment breakdown for a company (CIK or ticker)."""
        params = {
            "metric": metric,
            "axis": axis,
            "segmentType": segment_type,
            "period": period,
            "qtrs": qtrs,
            "accessionNumber": accession_number,
            "limit": limit,
        }
        return self._client._get_model(f"/v1/financials/{issuer}/segments", params, FinancialSegmentResponse)

    def segments_geography(
        self,
        issuer: str,
        *,
        metric: Optional[str] = None,
        axis: Optional[str] = None,
        period: Optional[str] = None,
        qtrs: Optional[int] = None,
        accession_number: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> FinancialSegmentResponse:
        """Geographic revenue segment breakdown for a company."""
        params = {
            "metric": metric,
            "axis": axis,
            "period": period,
            "qtrs": qtrs,
            "accessionNumber": accession_number,
            "limit": limit,
        }
        return self._client._get_model(
            f"/v1/financials/{issuer}/segments/geography", params, FinancialSegmentResponse
        )

    def segments_product_service(
        self,
        issuer: str,
        *,
        metric: Optional[str] = None,
        axis: Optional[str] = None,
        period: Optional[str] = None,
        qtrs: Optional[int] = None,
        accession_number: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> FinancialSegmentResponse:
        """Product/service revenue segment breakdown for a company."""
        params = {
            "metric": metric,
            "axis": axis,
            "period": period,
            "qtrs": qtrs,
            "accessionNumber": accession_number,
            "limit": limit,
        }
        return self._client._get_model(
            f"/v1/financials/{issuer}/segments/product-service", params, FinancialSegmentResponse
        )

    def segments_compare(
        self,
        issuer: str,
        *,
        metric: Optional[str] = None,
        axis: Optional[str] = None,
        segment_type: Optional[str] = None,
        periods: Optional[ListParam] = None,
        qtrs: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialSegmentResponse:
        """Compare a company's segment breakdown across fiscal periods."""
        params = {
            "metric": metric,
            "axis": axis,
            "segmentType": segment_type,
            "periods": periods,
            "qtrs": qtrs,
            "limit": limit,
        }
        return self._client._get_model(
            f"/v1/financials/{issuer}/segments/compare", params, FinancialSegmentResponse
        )

    def segments_geography_compare(
        self,
        issuer: str,
        *,
        metric: Optional[str] = None,
        axis: Optional[str] = None,
        periods: Optional[ListParam] = None,
        qtrs: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialSegmentResponse:
        """Compare geographic segment breakdowns across fiscal periods."""
        params = {"metric": metric, "axis": axis, "periods": periods, "qtrs": qtrs, "limit": limit}
        return self._client._get_model(
            f"/v1/financials/{issuer}/segments/geography/compare", params, FinancialSegmentResponse
        )

    def segments_product_service_compare(
        self,
        issuer: str,
        *,
        metric: Optional[str] = None,
        axis: Optional[str] = None,
        periods: Optional[ListParam] = None,
        qtrs: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> FinancialSegmentResponse:
        """Compare product/service segment breakdowns across fiscal periods."""
        params = {"metric": metric, "axis": axis, "periods": periods, "qtrs": qtrs, "limit": limit}
        return self._client._get_model(
            f"/v1/financials/{issuer}/segments/product-service/compare", params, FinancialSegmentResponse
        )

    # -- internals ---------------------------------------------------------

    def _statement(self, accession: str, kind: str) -> CompanyFinancialStatement:
        path = f"{_STATEMENTS_BASE.format(accession=accession)}/{kind}"
        return self._client._get_model(path, None, CompanyFinancialStatement)

    def _statement_for(
        self,
        kind: str,
        accession_number: Optional[str],
        *,
        ticker: Optional[str],
        cik: Optional[str],
        form: Optional[str],
    ) -> CompanyFinancialStatement:
        """One statement, by accession number or by company.

        By company the API picks the latest filing that has the statement, in
        one request. A ``form`` other than 10-K / 10-Q still goes through the
        filing search, which can match any form.
        """
        issuer = cik or ticker
        period = _period_for_form(form)
        if not accession_number and issuer and period is not _OTHER_FORM:
            return self.company_statement(issuer, kind, period=period)
        accession = self._require_accession(accession_number, ticker=ticker, cik=cik, form=form)
        return self._statement(accession, kind)

    def _require_accession(
        self,
        accession_number: Optional[str],
        *,
        ticker: Optional[str],
        cik: Optional[str],
        form: Optional[str],
    ) -> str:
        if accession_number:
            return accession_number
        if ticker or cik:
            return self._resolve_latest_accession(ticker=ticker, cik=cik, form=form)
        raise TypeError(
            "Provide an accession_number, or ticker=/cik= to resolve the latest filing."
        )

    def _resolve_latest_accession(
        self, *, ticker: Optional[str], cik: Optional[str], form: Optional[str]
    ) -> str:
        """Resolve the most recent filing's accession number for a company.

        Uses the companies search endpoint, optionally filtering by ``form``,
        and picks the filing with the latest filed date.
        """
        response = self.companies(ticker=ticker, cik=cik, limit=100)
        filings = response.filings or []
        if form:
            wanted = form.upper()
            matching = [f for f in filings if (f.form or "").upper() == wanted]
            filings = matching or filings
        filings = sorted(filings, key=lambda f: f.filed or datetime.date.min, reverse=True)
        for filing in filings:
            if filing.accession_number:
                return filing.accession_number
        who = ticker or cik
        raise ValueError(
            f"Could not find a filing to resolve a statement for {who!r}. "
            "Pass an explicit accession_number instead."
        )
