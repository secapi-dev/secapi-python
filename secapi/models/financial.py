"""Auto-generated SEC API models. Do not edit by hand.

Regenerate with: python scripts/generate_models.py
"""

from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field

from ._base import SecBaseModel
from .filing import FilingContext


class BalanceSheetLine(SecBaseModel):
    """One balance-sheet figure with a short label for UI"""
    label: Optional[str] = Field(default=None, description="Human-readable line title")
    value: Optional[float] = Field(default=None, description="Reported amount")
    currency: Optional[str] = Field(default=None, description="Currency the amount is in")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Balance-sheet date for this figure (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="Number of quarters spanned by this instant fact (0 for balance sheet)")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year this row is tied to")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period label when available")


class CanonicalBalanceSheet(SecBaseModel):
    """Key balance-sheet figures for one filing date, in plain language"""
    filing: Optional[FilingContext] = Field(default=None, description="Filing these numbers came from")
    statement: Optional[str] = Field(default=None, description="Which statement this is")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Balance-sheet date (YYYYMMDD)")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Line items keyed by short JSON names. Example keys: cashAndCashEquivalents, totalAssets, totalLiabilities. Missing lines are present with null values.")


class CanonicalCashFlow(SecBaseModel):
    """Key cash-flow figures for one filing and reporting window, in plain language"""
    filing: Optional[FilingContext] = Field(default=None, description="Filing these numbers came from")
    statement: Optional[str] = Field(default=None, description="Which statement this is")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Last day of the reporting window (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="How many fiscal quarters the figures span (1 = one quarter, 4 = full year)")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Line items keyed by short JSON names. Example keys: cfo, capitalExpenditures, netChangeInCash. Missing lines are present with null values.")


class CanonicalIncomeStatement(SecBaseModel):
    """Key income-statement figures for one filing and reporting window, in plain language"""
    filing: Optional[FilingContext] = Field(default=None, description="Filing these numbers came from")
    statement: Optional[str] = Field(default=None, description="Which statement this is")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Last day of the reporting window (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="How many fiscal quarters the figures span (1 = one quarter, 4 = full year)")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Line items keyed by short JSON names. Example keys: revenue, grossProfit, netIncome. Missing lines are present with null values.")


class CashFlowLine(SecBaseModel):
    """One cash-flow figure with a short label for UI"""
    label: Optional[str] = Field(default=None, description="Human-readable line title")
    value: Optional[float] = Field(default=None, description="Reported amount")
    currency: Optional[str] = Field(default=None, description="Currency the amount is in")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Last day of the reporting window for this figure (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="How many fiscal quarters this figure spans")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year this row is tied to")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period label (FY, Q1, ...)")


class CompaniesPagination(SecBaseModel):
    """Pagination metadata for company search results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class CompaniesSearchFilter(SecBaseModel):
    """Normalized filters applied to the company financials lookup"""
    ticker: Optional[str] = Field(default=None, description="Exact ticker symbol (case-insensitive)")
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit CIK filter (takes precedence over ticker)")


class CompanyFilingSubmission(SecBaseModel):
    """Single processed 10-K/10-Q financial submission row from pipelines_sec.sec_financial_statement_sub"""
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="SEC accession number (dashed canonical form)")
    form: Optional[str] = Field(default=None, description="SEC form type Allowed values: 10-K, 10-Q, 10-K/A, 10-Q/A")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period label Allowed values: FY, Q1, Q2, Q3")
    period_end: Optional[datetime.date] = Field(default=None, alias="periodEnd", description="Fiscal period end date (from SEC `period` column)")
    filed: Optional[datetime.date] = Field(default=None, description="Filing date (from SEC `filed` column)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="Timestamp when the SEC accepted the filing")


class CompanyIssuer(SecBaseModel):
    """Issuer identity derived from the most recent matching filing in pipelines_sec"""
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit Central Index Key")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol recorded on the most recent filing")
    name: Optional[str] = Field(default=None, description="Company name recorded on the most recent filing")
    sic: Optional[int] = Field(default=None, description="SEC Standard Industrial Classification code")
    country_inc: Optional[str] = Field(default=None, alias="countryInc", description="Country of incorporation (ISO-2 when available)")


class CompaniesSearchResponse(SecBaseModel):
    """A single issuer's most recent processed XBRL financial submissions, paginated"""
    issuer: Optional[CompanyIssuer] = Field(default=None, description="Issuer identity taken from the most recent matching filing (null when no filings exist for the lookup)")
    filings: Optional[List[CompanyFilingSubmission]] = Field(default=None, description="Latest financial submissions for the issuer, ordered by `accepted` descending")
    pagination: Optional[CompaniesPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[CompaniesSearchFilter] = Field(default=None, description="Normalized filters that were applied to the query")


class StatementValueContext(SecBaseModel):
    """SEC numeric fact period context (ddate / qtrs / unit), attached to the statement line value"""
    ddate: Optional[int] = Field(default=None, description="Data date (balance sheet instant or period end), YYYYMMDD")
    qtrs: Optional[int] = Field(default=None, description="Number of quarters represented (0 = point in time, 1 = quarter, 4 = annual)")
    uom: Optional[str] = Field(default=None, description="Unit of measure")
    segments: Optional[str] = Field(default=None, description="Segment key when dimensional (empty in this view)")
    coreg: Optional[str] = Field(default=None, description="Co-registrant key when present")
    value: Optional[float] = Field(default=None, description="Numeric fact value")
    footnote: Optional[str] = Field(default=None, description="Footnote reference text when present")
    period_label: Optional[str] = Field(default=None, alias="periodLabel", description="Human-readable period label derived from ddate and qtrs")


class StatementTableRow(SecBaseModel):
    """One presentation line with resolved numeric fact and taxonomy metadata"""
    report: Optional[int] = Field(default=None, description="Presentation report number")
    line: Optional[int] = Field(default=None, description="Line order within the report")
    stmt: Optional[str] = Field(default=None, description="Statement key on the presentation line")
    inpth: Optional[int] = Field(default=None, description="Presentation tree depth")
    rfile: Optional[str] = Field(default=None, description="Source instance / role file name")
    tag: Optional[str] = Field(default=None, description="XBRL local tag name")
    version: Optional[str] = Field(default=None, description="Taxonomy version")
    plabel: Optional[str] = Field(default=None, description="Preferred label on the statement")
    negating: Optional[int] = Field(default=None, description="Negating flag from presentation (0/1)")
    value_context: Optional[StatementValueContext] = Field(default=None, alias="valueContext", description="Resolved numeric fact and period context for this line")
    custom: Optional[int] = Field(default=None, description="Issuer-defined custom tag flag (0/1)")
    datatype: Optional[str] = Field(default=None, description="XBRL datatype")
    iord: Optional[str] = Field(default=None, description="Income statement ordering hint")
    crdr: Optional[str] = Field(default=None, description="Debit/credit balance type")
    tlabel: Optional[str] = Field(default=None, description="Standard taxonomy label")
    doc: Optional[str] = Field(default=None, description="Taxonomy documentation")
    abstract: Optional[bool] = Field(default=None, description="Whether the taxonomy concept is abstract")


class CompanyFinancialStatement(SecBaseModel):
    """Presentation-ordered financial statement rows for one filing, with filing context and per-fact period metadata"""
    filing: Optional[FilingContext] = Field(default=None, description="Filing the statement rows were taken from")
    stmt: Optional[str] = Field(default=None, description="Statement key (IS, BS, CF, SE, CI)")
    rows: Optional[List[StatementTableRow]] = Field(default=None, description="Flat table of presentation lines joined to tag metadata and numeric facts")


class Concept(SecBaseModel):
    """Single XBRL concept / tag row from pipelines_sec.sec_financial_statement_tag"""
    tag: Optional[str] = Field(default=None, description="XBRL tag local name")
    version: Optional[str] = Field(default=None, description="Taxonomy version")
    custom: Optional[bool] = Field(default=None, description="Whether the tag is a registrant-defined (custom) extension")
    abstract: Optional[bool] = Field(default=None, description="Whether the taxonomy concept is abstract")
    datatype: Optional[str] = Field(default=None, description="XBRL datatype")
    iord: Optional[str] = Field(default=None, description="Instant/duration period type (I or D)")
    crdr: Optional[str] = Field(default=None, description="Debit/credit balance type (C or D)")
    tlabel: Optional[str] = Field(default=None, description="Standard taxonomy label")
    doc: Optional[str] = Field(default=None, description="Taxonomy documentation")


class ConceptsFilter(SecBaseModel):
    """Normalized filters applied to the concepts search query"""
    q: Optional[str] = Field(default=None, description="Free-text query on tag, label or documentation")
    version: Optional[str] = Field(default=None, description="Taxonomy version substring filter")
    custom: Optional[bool] = Field(default=None, description="When set, restricts to custom (true) or standard (false) tags")


class ConceptsPagination(SecBaseModel):
    """Pagination metadata for concept search results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class ConceptsListResponse(SecBaseModel):
    """Paginated XBRL concepts search response"""
    data: Optional[List[Concept]] = Field(default=None, description="Concepts returned for the current page")
    pagination: Optional[ConceptsPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[ConceptsFilter] = Field(default=None, description="Normalized filters that were applied to the query")


class FinancialMetricRankingCompany(SecBaseModel):
    """One company ranked by a canonical financial metric"""
    rank: Optional[int] = Field(default=None, description="One-based rank after sorting by value descending")
    metric: Optional[str] = Field(default=None, description="Canonical metric storage key")
    label: Optional[str] = Field(default=None, description="Human-readable canonical metric label when available")
    adsh: Optional[str] = Field(default=None, description="EDGAR accession number (ADSH)")
    cik: Optional[int] = Field(default=None, description="Central Index Key")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol recorded on the submission")
    entity_name: Optional[str] = Field(default=None, alias="entityName", description="Legal entity name")
    sic: Optional[int] = Field(default=None, description="SEC Standard Industrial Classification code")
    country_inc: Optional[str] = Field(default=None, alias="countryInc", description="Country of incorporation")
    form: Optional[str] = Field(default=None, description="SEC form type")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year on the submission")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period on the submission")
    period: Optional[int] = Field(default=None, description="Document period end from the submission (YYYYMMDD)")
    filed: Optional[int] = Field(default=None, description="SEC filing date (YYYYMMDD)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Metric period end date (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="Number of quarters represented: 0 = instant, 1 = quarter, 4 = annual")
    unit: Optional[str] = Field(default=None, description="Unit of measure")
    value: Optional[float] = Field(default=None, description="Numeric metric value")
    source_tag: Optional[str] = Field(default=None, alias="sourceTag", description="SEC tag used by the canonical mapper")
    source_version: Optional[str] = Field(default=None, alias="sourceVersion", description="Source taxonomy version")
    strategy: Optional[str] = Field(default=None, description="Canonical mapping strategy")
    rule_id: Optional[str] = Field(default=None, alias="ruleId", description="Canonical mapping rule identifier")
    confidence: Optional[float] = Field(default=None, description="Canonical mapping confidence")


class FinancialMetricRankingFilter(SecBaseModel):
    """Filters used to build a financial metric ranking response"""
    metric: Optional[str] = Field(default=None, description="Canonical metric storage key")
    basis: Optional[str] = Field(default=None, description="Ranking period basis Allowed values: annual, quarterly")
    year: Optional[int] = Field(default=None, description="Fiscal/calendar year used for the ranking. Defaults to the latest completed year.")
    quarter: Optional[int] = Field(default=None, description="Quarter used for quarterly rankings Allowed values: 1, 2, 3, 4")
    qtrs: Optional[int] = Field(default=None, description="Quarter span used for comparison: 0 = instant balance sheet, 1 = quarter, 4 = annual")
    unit: Optional[str] = Field(default=None, description="Unit of measure used for ranking. Rankings are USD-only until currency conversion is available.")
    limit: Optional[int] = Field(default=None, description="Maximum companies returned")


class FinancialMetricRankingResponse(SecBaseModel):
    """Companies ranked by a canonical financial metric"""
    filters: Optional[FinancialMetricRankingFilter] = Field(default=None, description="Filters used for the query")
    companies: Optional[List[FinancialMetricRankingCompany]] = Field(default=None, description="Companies ranked by metric value")


class FinancialMetricSeriesPoint(SecBaseModel):
    """One period in a financial metric time series"""
    adsh: Optional[str] = Field(default=None, description="EDGAR accession number (ADSH)")
    cik: Optional[int] = Field(default=None, description="Central Index Key")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol recorded on the submission")
    entity_name: Optional[str] = Field(default=None, alias="entityName", description="Legal entity name")
    form: Optional[str] = Field(default=None, description="SEC form type")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year on the submission")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period on the submission")
    period: Optional[int] = Field(default=None, description="Document period end from the submission (YYYYMMDD)")
    filed: Optional[int] = Field(default=None, description="SEC filing date (YYYYMMDD)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Metric period end date (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="Number of quarters represented: 0 = instant, 1 = quarter, 4 = annual")
    unit: Optional[str] = Field(default=None, description="Unit of measure")
    value: Optional[float] = Field(default=None, description="Numeric metric value")
    tag: Optional[str] = Field(default=None, description="SEC tag local name for raw facts, or source tag for canonical metrics")
    version: Optional[str] = Field(default=None, description="Source taxonomy version")
    label: Optional[str] = Field(default=None, description="Raw SEC tag label")
    custom: Optional[int] = Field(default=None, description="Issuer-defined custom tag flag (0/1)")
    datatype: Optional[str] = Field(default=None, description="XBRL datatype")
    segments: Optional[str] = Field(default=None, description="Segment key when dimensional")
    coreg: Optional[str] = Field(default=None, description="Co-registrant key when present")
    strategy: Optional[str] = Field(default=None, description="Canonical mapping strategy")
    rule_id: Optional[str] = Field(default=None, alias="ruleId", description="Canonical mapping rule identifier")
    confidence: Optional[float] = Field(default=None, description="Canonical mapping confidence")


class FinancialMetricSeries(SecBaseModel):
    """One financial metric time series"""
    symbol: Optional[str] = Field(default=None, description="Requested canonical metric or SEC tag local name")
    source: Optional[str] = Field(default=None, description="Metric source Allowed values: canonical, raw")
    version: Optional[str] = Field(default=None, description="Taxonomy version for raw SEC tags")
    quarters: Optional[int] = Field(default=None, description="Number of quarters represented by this series: 0 = instant, 1 = quarter, 4 = annual")
    label: Optional[str] = Field(default=None, description="Human-readable label when available")
    points: Optional[List[FinancialMetricSeriesPoint]] = Field(default=None, description="Chronological metric points")


class FinancialMetricSeriesFilter(SecBaseModel):
    """Filters used to build a financial metric time series response"""
    symbols: Optional[List[str]] = Field(default=None, description="Requested canonical metric storage keys and/or raw SEC tag local names")
    source: Optional[str] = Field(default=None, description="Metric source queried Allowed values: canonical, raw, all")
    version: Optional[str] = Field(default=None, description="Optional taxonomy version filter for raw SEC tags")
    start_date: Optional[datetime.date] = Field(default=None, alias="startDate", description="Include periods ending on or after this date")
    end_date: Optional[datetime.date] = Field(default=None, alias="endDate", description="Include periods ending on or before this date")
    qtrs: Optional[int] = Field(default=None, description="Optional quarter span filter: 0 = instant, 1 = quarter, 4 = annual")
    limit: Optional[int] = Field(default=None, description="Maximum points returned per metric series")


class FinancialMetricSeriesResponse(SecBaseModel):
    """Financial metric time series grouped by requested symbol"""
    issuer: Optional[CompanyIssuer] = Field(default=None, description="Issuer matched by CIK or ticker")
    filters: Optional[FinancialMetricSeriesFilter] = Field(default=None, description="Filters used for the query")
    series: Optional[List[FinancialMetricSeries]] = Field(default=None, description="One time series per source/symbol/version")


class FinancialRatioComponent(SecBaseModel):
    """Canonical metric value used to calculate a financial ratio"""
    metric: Optional[str] = Field(default=None, description="Canonical metric key")
    value: Optional[float] = Field(default=None, description="Metric value used in the ratio")
    unit: Optional[str] = Field(default=None, description="Metric unit of measure")


class FinancialRatioFilter(SecBaseModel):
    """Filters used to build a precalculated financial ratio response"""
    ratios: Optional[List[str]] = Field(default=None, description="Requested ratio identifiers")
    group: Optional[str] = Field(default=None, description="Ratio group queried Allowed values: liquidity, leverage, profitability, efficiency, all")
    start_date: Optional[datetime.date] = Field(default=None, alias="startDate", description="Include periods ending on or after this date")
    end_date: Optional[datetime.date] = Field(default=None, alias="endDate", description="Include periods ending on or before this date")
    qtrs: Optional[int] = Field(default=None, description="Optional quarter span filter: 0 = instant, 1 = quarter, 4 = annual")
    limit: Optional[int] = Field(default=None, description="Maximum points returned per ratio series")


class FinancialRatioPoint(SecBaseModel):
    """One precalculated financial ratio value for a reporting period"""
    adsh: Optional[str] = Field(default=None, description="EDGAR accession number (ADSH)")
    cik: Optional[int] = Field(default=None, description="Central Index Key")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol recorded on the submission")
    entity_name: Optional[str] = Field(default=None, alias="entityName", description="Legal entity name")
    form: Optional[str] = Field(default=None, description="SEC form type")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year on the submission")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period on the submission")
    period: Optional[int] = Field(default=None, description="Document period end from the submission (YYYYMMDD)")
    filed: Optional[int] = Field(default=None, description="SEC filing date (YYYYMMDD)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Ratio period end date (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="Number of quarters represented: 0 = instant, 1 = quarter, 4 = annual")
    value: Optional[float] = Field(default=None, description="Precalculated ratio value")
    unit: Optional[str] = Field(default=None, description="Ratio unit Allowed values: decimal, turns")
    components: Optional[List[FinancialRatioComponent]] = Field(default=None, description="Canonical metrics used in the calculation, when available")


class FinancialRatioRankingCompany(SecBaseModel):
    """One company ranked by a calculated financial ratio"""
    rank: Optional[int] = Field(default=None, description="One-based rank after sorting by ratio value descending")
    ratio: Optional[str] = Field(default=None, description="Ratio identifier")
    group: Optional[str] = Field(default=None, description="Ratio group")
    label: Optional[str] = Field(default=None, description="Human-readable label")
    description: Optional[str] = Field(default=None, description="What the ratio measures")
    formula: Optional[str] = Field(default=None, description="Plain formula using canonical metric keys")
    adsh: Optional[str] = Field(default=None, description="EDGAR accession number (ADSH)")
    cik: Optional[int] = Field(default=None, description="Central Index Key")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol recorded on the submission")
    entity_name: Optional[str] = Field(default=None, alias="entityName", description="Legal entity name")
    sic: Optional[int] = Field(default=None, description="SEC Standard Industrial Classification code")
    country_inc: Optional[str] = Field(default=None, alias="countryInc", description="Country of incorporation")
    form: Optional[str] = Field(default=None, description="SEC form type")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year on the submission")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period on the submission")
    period: Optional[int] = Field(default=None, description="Document period end from the submission (YYYYMMDD)")
    filed: Optional[int] = Field(default=None, description="SEC filing date (YYYYMMDD)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Ratio period end date (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="Number of quarters represented: 0 = instant, 1 = quarter, 4 = annual")
    value: Optional[float] = Field(default=None, description="Calculated ratio value")
    unit: Optional[str] = Field(default=None, description="Ratio unit Allowed values: decimal, turns")
    components: Optional[List[FinancialRatioComponent]] = Field(default=None, description="Canonical metrics used in the calculation")


class FinancialRatioRankingFilter(SecBaseModel):
    """Filters used to build a calculated financial ratio ranking response"""
    ratio: Optional[str] = Field(default=None, description="Ratio identifier")
    group: Optional[str] = Field(default=None, description="Ratio group queried Allowed values: liquidity, leverage, profitability, efficiency, all")
    start_date: Optional[datetime.date] = Field(default=None, alias="startDate", description="Include periods ending on or after this date")
    end_date: Optional[datetime.date] = Field(default=None, alias="endDate", description="Include periods ending on or before this date")
    qtrs: Optional[int] = Field(default=None, description="Quarter span used for comparison: 0 = instant, 1 = quarter, 4 = annual")
    limit: Optional[int] = Field(default=None, description="Maximum companies returned")


class FinancialRatioRankingResponse(SecBaseModel):
    """Companies ranked by a calculated financial ratio"""
    filters: Optional[FinancialRatioRankingFilter] = Field(default=None, description="Filters used for the query")
    companies: Optional[List[FinancialRatioRankingCompany]] = Field(default=None, description="Companies ranked by calculated ratio value")


class FinancialRatioSeries(SecBaseModel):
    """One precalculated financial ratio time series"""
    ratio: Optional[str] = Field(default=None, description="Ratio identifier")
    group: Optional[str] = Field(default=None, description="Ratio group")
    label: Optional[str] = Field(default=None, description="Human-readable label")
    description: Optional[str] = Field(default=None, description="What the ratio measures")
    formula: Optional[str] = Field(default=None, description="Plain formula describing the precalculated ratio")
    unit: Optional[str] = Field(default=None, description="Ratio unit Allowed values: decimal, turns")
    points: Optional[List[FinancialRatioPoint]] = Field(default=None, description="Chronological ratio points")


class FinancialRatioSeriesResponse(SecBaseModel):
    """Precalculated financial ratios grouped by ratio identifier"""
    issuer: Optional[CompanyIssuer] = Field(default=None, description="Issuer matched by CIK or ticker")
    filters: Optional[FinancialRatioFilter] = Field(default=None, description="Filters used for the query")
    series: Optional[List[FinancialRatioSeries]] = Field(default=None, description="One time series per precalculated ratio")


class FinancialSegmentFilter(SecBaseModel):
    """Filters used to build a company segment revenue breakdown"""
    metric: Optional[str] = Field(default=None, description="Canonical metric requested")
    axis: Optional[str] = Field(default=None, description="Optional XBRL axis filter")
    segment_type: Optional[str] = Field(default=None, alias="segmentType", description="Segment type filter. One or more of: product, service, geography, business, other. Allowed values: product, service, geography, business, other")
    period: Optional[str] = Field(default=None, description="Single fiscal period filter, such as YYYY or YYYYQN")
    periods: Optional[str] = Field(default=None, description="Comma-separated fiscal periods for compare requests")
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="SEC accession number used to scope the query")
    qtrs: Optional[int] = Field(default=None, description="Quarter span filter: 1 = quarterly, 4 = annual")
    limit: Optional[int] = Field(default=None, description="Maximum rows returned")


class FinancialSegmentRow(SecBaseModel):
    """One segment member value in a company revenue breakdown"""
    name: Optional[str] = Field(default=None, description="Retail-friendly segment name")
    segment_type: Optional[str] = Field(default=None, alias="segmentType", description="Classified segment type Allowed values: product, service, geography, business, other")
    axis_qname: Optional[str] = Field(default=None, alias="axisQname", description="XBRL axis QName")
    axis_label: Optional[str] = Field(default=None, alias="axisLabel", description="Human-readable axis label")
    member_qname: Optional[str] = Field(default=None, alias="memberQname", description="XBRL member QName")
    member_label: Optional[str] = Field(default=None, alias="memberLabel", description="Human-readable member label")
    value: Optional[float] = Field(default=None, description="Segment value")
    unit: Optional[str] = Field(default=None, description="Unit of measure")
    percent_of_revenue: Optional[float] = Field(default=None, alias="percentOfRevenue", description="Share of total canonical revenue, when total revenue is available")
    source_tag: Optional[str] = Field(default=None, alias="sourceTag", description="Source SEC tag")
    source_version: Optional[str] = Field(default=None, alias="sourceVersion", description="Source taxonomy version")
    strategy: Optional[str] = Field(default=None, description="Mapping strategy")
    rule_id: Optional[str] = Field(default=None, alias="ruleId", description="Rule identifier")
    confidence: Optional[float] = Field(default=None, description="Mapping confidence")


class FinancialSegmentPeriod(SecBaseModel):
    """Segment breakdown rows for one fiscal period"""
    adsh: Optional[str] = Field(default=None, description="EDGAR accession number (ADSH)")
    form: Optional[str] = Field(default=None, description="SEC form type")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period")
    period: Optional[int] = Field(default=None, description="Document period end from the filing (YYYYMMDD)")
    filed: Optional[int] = Field(default=None, description="SEC filing date (YYYYMMDD)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Metric period end date (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="Quarter span: 1 = quarterly, 4 = annual")
    total_revenue: Optional[float] = Field(default=None, alias="totalRevenue", description="Total canonical revenue for this period, when available")
    segment_revenue_total: Optional[float] = Field(default=None, alias="segmentRevenueTotal", description="Sum of segment rows returned for this period")
    coverage_pct: Optional[float] = Field(default=None, alias="coveragePct", description="Returned segment total divided by total revenue, when total revenue is available")
    rows: Optional[List[FinancialSegmentRow]] = Field(default=None, description="Segment rows")


class FinancialSegmentResponse(SecBaseModel):
    """Company segment revenue breakdown across one or more fiscal periods"""
    issuer: Optional[CompanyIssuer] = Field(default=None, description="Issuer matched by CIK or ticker")
    filters: Optional[FinancialSegmentFilter] = Field(default=None, description="Filters used for the query")
    periods: Optional[List[FinancialSegmentPeriod]] = Field(default=None, description="Breakdown grouped by fiscal period")


class XbrlPeriod(SecBaseModel):
    """Statement column describing the reporting period for fact values"""
    key: Optional[str] = Field(default=None, description="Stable internal key used to map row values to this period")
    label: Optional[str] = Field(default=None, description="Display label for the period")
    period_type: Optional[str] = Field(default=None, alias="periodType", description="XBRL period type")
    instant_date: Optional[str] = Field(default=None, alias="instantDate", description="Instant date for instant contexts")
    start_date: Optional[str] = Field(default=None, alias="startDate", description="Start date for duration contexts")
    end_date: Optional[str] = Field(default=None, alias="endDate", description="End date for duration contexts")


class XbrlRow(SecBaseModel):
    """Presentation row with values keyed by period"""
    label: Optional[str] = Field(default=None, description="Preferred label shown for the concept")
    depth: Optional[int] = Field(default=None, description="Indent depth in the presentation tree")
    qname: Optional[str] = Field(default=None, description="QName of the concept")
    values: Optional[Dict[str, Any]] = Field(default=None, description="Numeric fact values keyed by period key")
    abstract: Optional[bool] = Field(default=None, description="Whether the row is a structural abstract node")


class XbrlStatement(SecBaseModel):
    """Single XBRL presentation role with its periods and rows"""
    role_uri: Optional[str] = Field(default=None, alias="roleUri", description="Presentation role URI")
    role_label: Optional[str] = Field(default=None, alias="roleLabel", description="Human-readable role label")
    role_definition: Optional[str] = Field(default=None, alias="roleDefinition", description="Role definition when available")
    periods: Optional[List[XbrlPeriod]] = Field(default=None, description="Primary reporting periods selected for the statement")
    rows: Optional[List[XbrlRow]] = Field(default=None, description="Rows ordered according to the XBRL presentation linkbase")


class FinancialXbrl(SecBaseModel):
    """Form-agnostic XBRL statement view assembled from SEC raw financial statement tables"""
    adsh: Optional[str] = Field(default=None, description="EDGAR accession data set header string (ADSH)")
    company_name: Optional[str] = Field(default=None, alias="companyName", description="Display name of the filing entity")
    form_type: Optional[str] = Field(default=None, alias="formType", description="SEC form type associated with the XBRL filing")
    statements: Optional[List[XbrlStatement]] = Field(default=None, description="Statement trees grouped by presentation role")


class IncomeStatementLine(SecBaseModel):
    """One headline figure with a short label for UI"""
    label: Optional[str] = Field(default=None, description="Human-readable line title")
    value: Optional[float] = Field(default=None, description="Reported amount")
    currency: Optional[str] = Field(default=None, description="Currency the amount is in")
    end_date: Optional[int] = Field(default=None, alias="endDate", description="Last day of the reporting window for this figure (YYYYMMDD)")
    quarters: Optional[int] = Field(default=None, description="How many fiscal quarters this figure spans")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year this row is tied to")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period label (FY, Q1, …)")


__all__ = [
    "BalanceSheetLine",
    "CanonicalBalanceSheet",
    "CanonicalCashFlow",
    "CanonicalIncomeStatement",
    "CashFlowLine",
    "CompaniesPagination",
    "CompaniesSearchFilter",
    "CompaniesSearchResponse",
    "CompanyFilingSubmission",
    "CompanyFinancialStatement",
    "CompanyIssuer",
    "Concept",
    "ConceptsFilter",
    "ConceptsListResponse",
    "ConceptsPagination",
    "FinancialMetricRankingCompany",
    "FinancialMetricRankingFilter",
    "FinancialMetricRankingResponse",
    "FinancialMetricSeries",
    "FinancialMetricSeriesFilter",
    "FinancialMetricSeriesPoint",
    "FinancialMetricSeriesResponse",
    "FinancialRatioComponent",
    "FinancialRatioFilter",
    "FinancialRatioPoint",
    "FinancialRatioRankingCompany",
    "FinancialRatioRankingFilter",
    "FinancialRatioRankingResponse",
    "FinancialRatioSeries",
    "FinancialRatioSeriesResponse",
    "FinancialSegmentFilter",
    "FinancialSegmentPeriod",
    "FinancialSegmentResponse",
    "FinancialSegmentRow",
    "FinancialXbrl",
    "IncomeStatementLine",
    "StatementTableRow",
    "StatementValueContext",
    "XbrlPeriod",
    "XbrlRow",
    "XbrlStatement",
]

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, SecBaseModel):
        _m.model_rebuild()
