"""Auto-generated SEC API models. Do not edit by hand.

Regenerate with: python scripts/generate_models.py
"""

from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import Field

from ._base import SecBaseModel


class InstitutionChangesFilter(SecBaseModel):
    """Filters applied to the institution changes query"""
    cik: Optional[str] = Field(default=None, description="Normalized institutional manager CIK")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")


class InstitutionChangesMetrics(SecBaseModel):
    """Quarter-over-quarter Form 13F metrics for one institutional manager"""
    current_aum: Optional[float] = Field(default=None, alias="currentAum", description="Current disclosed portfolio value in USD")
    prior_aum: Optional[float] = Field(default=None, alias="priorAum", description="Previous disclosed portfolio value in USD")
    aum_change: Optional[float] = Field(default=None, alias="aumChange", description="Current minus previous disclosed portfolio value in USD")
    aum_change_percent: Optional[float] = Field(default=None, alias="aumChangePercent", description="Percent change in disclosed portfolio value")
    reported_value_return_percent: Optional[float] = Field(default=None, alias="reportedValueReturnPercent", description="Reported value return proxy from 13F values, not a true time-weighted return")
    current_position_count: Optional[int] = Field(default=None, alias="currentPositionCount", description="Current holding row count")
    prior_position_count: Optional[int] = Field(default=None, alias="priorPositionCount", description="Previous holding row count")
    position_count_change: Optional[int] = Field(default=None, alias="positionCountChange", description="Current minus previous holding row count")
    current_security_count: Optional[int] = Field(default=None, alias="currentSecurityCount", description="Current distinct CUSIP count")
    prior_security_count: Optional[int] = Field(default=None, alias="priorSecurityCount", description="Previous distinct CUSIP count")
    security_count_change: Optional[int] = Field(default=None, alias="securityCountChange", description="Current minus previous distinct CUSIP count")
    additions_count: Optional[int] = Field(default=None, alias="additionsCount", description="Positions present in current quarter but not prior quarter")
    disposals_count: Optional[int] = Field(default=None, alias="disposalsCount", description="Positions present in prior quarter but not current quarter")
    increased_count: Optional[int] = Field(default=None, alias="increasedCount", description="Existing positions with higher reported value than prior quarter")
    decreased_count: Optional[int] = Field(default=None, alias="decreasedCount", description="Existing positions with lower reported value than prior quarter")
    unchanged_count: Optional[int] = Field(default=None, alias="unchangedCount", description="Existing positions with unchanged reported value")
    additions_value: Optional[float] = Field(default=None, alias="additionsValue", description="Reported value of additions in USD")
    disposals_value: Optional[float] = Field(default=None, alias="disposalsValue", description="Prior reported value of disposals in USD")
    increased_value: Optional[float] = Field(default=None, alias="increasedValue", description="Positive reported value changes on existing positions in USD")
    decreased_value: Optional[float] = Field(default=None, alias="decreasedValue", description="Absolute negative reported value changes on existing positions in USD")
    buy_value: Optional[float] = Field(default=None, alias="buyValue", description="Additions plus positive reported value changes in USD")
    sell_value: Optional[float] = Field(default=None, alias="sellValue", description="Disposals plus absolute negative reported value changes in USD")
    net_activity_value: Optional[float] = Field(default=None, alias="netActivityValue", description="Buy value minus sell value in USD")
    gross_activity_value: Optional[float] = Field(default=None, alias="grossActivityValue", description="Buy value plus sell value in USD")
    addition_rate_percent: Optional[float] = Field(default=None, alias="additionRatePercent", description="Additions as a percent of prior distinct CUSIPs")
    disposal_rate_percent: Optional[float] = Field(default=None, alias="disposalRatePercent", description="Disposals as a percent of prior distinct CUSIPs")
    turnover_percent: Optional[float] = Field(default=None, alias="turnoverPercent", description="Gross activity value as a percent of prior AUM")


class InstitutionChangesPeriod(SecBaseModel):
    """13F periods compared by an institution change snapshot"""
    current_quarter: Optional[str] = Field(default=None, alias="currentQuarter", description="Current fiscal quarter label")
    current_period_end: Optional[datetime.date] = Field(default=None, alias="currentPeriodEnd", description="Current 13F period end date")
    prior_quarter: Optional[str] = Field(default=None, alias="priorQuarter", description="Previous fiscal quarter label")
    prior_period_end: Optional[datetime.date] = Field(default=None, alias="priorPeriodEnd", description="Previous 13F period end date")
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="13F accession number for the current filing")
    filing_date: Optional[datetime.date] = Field(default=None, alias="filingDate", description="13F filing date for the current period")


class InstitutionChangesResponse(SecBaseModel):
    """Institutional Form 13F quarter-over-quarter changes response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    period: Optional[InstitutionChangesPeriod] = Field(default=None, description="13F periods compared by this response")
    metrics: Optional[InstitutionChangesMetrics] = Field(default=None, description="Quarter-over-quarter metrics")
    filters: Optional[InstitutionChangesFilter] = Field(default=None, description="Filters applied to the query")


class Institution(SecBaseModel):
    """Institutional Form 13F filer summary"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    latest_form_type: Optional[str] = Field(default=None, alias="latestFormType", description="Most recent 13F form type filed by the manager")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Most recent 13F accession number")
    latest_filing_date: Optional[datetime.date] = Field(default=None, alias="latestFilingDate", description="Most recent 13F filing date")
    latest_period_of_report: Optional[datetime.date] = Field(default=None, alias="latestPeriodOfReport", description="Most recent 13F period of report")
    latest_received_date: Optional[datetime.datetime] = Field(default=None, alias="latestReceivedDate", description="Timestamp when the most recent filing was received")
    latest_source_url: Optional[str] = Field(default=None, alias="latestSourceUrl", description="SEC source URL for the most recent filing")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Number of Form 13F filings stored for the manager")
    latest_position_count: Optional[int] = Field(default=None, alias="latestPositionCount", description="Number of holdings rows in the latest filing")
    latest_security_count: Optional[int] = Field(default=None, alias="latestSecurityCount", description="Number of distinct CUSIPs in the latest filing")
    latest_portfolio_value: Optional[float] = Field(default=None, alias="latestPortfolioValue", description="Aggregate latest 13F portfolio value in USD")


class InstitutionFilingManager(SecBaseModel):
    """Manager disclosed on a Form 13F filing"""
    type: Optional[str] = Field(default=None, description="Manager relationship source")
    sequence_number: Optional[int] = Field(default=None, alias="sequenceNumber", description="Sequence number used by holdings rows for other managers")
    manager_cik: Optional[str] = Field(default=None, alias="managerCik", description="Manager CIK when disclosed")
    manager_name: Optional[str] = Field(default=None, alias="managerName", description="Manager name")
    form13f_file_number: Optional[str] = Field(default=None, alias="form13fFileNumber", description="SEC Form 13F file number")
    crd_number: Optional[str] = Field(default=None, alias="crdNumber", description="CRD number when disclosed")
    sec_file_number: Optional[str] = Field(default=None, alias="secFileNumber", description="SEC file number when disclosed")


class InstitutionFiling(SecBaseModel):
    """Form 13F filing metadata and manager disclosures"""
    form13f_id: Optional[int] = Field(default=None, alias="form13fId", description="Internal Form 13F identifier")
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    form_type: Optional[str] = Field(default=None, alias="formType", description="SEC form type")
    report_type: Optional[str] = Field(default=None, alias="reportType", description="13F report type from the filing cover page")
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="SEC accession number")
    filing_date: Optional[datetime.date] = Field(default=None, alias="filingDate", description="Filing date")
    period_of_report: Optional[datetime.date] = Field(default=None, alias="periodOfReport", description="13F period of report")
    quarter: Optional[str] = Field(default=None, description="Quarter label for the period of report")
    received_date: Optional[datetime.datetime] = Field(default=None, alias="receivedDate", description="Timestamp when the filing was received")
    source_url: Optional[str] = Field(default=None, alias="sourceUrl", description="SEC source URL for the filing")
    is_notice: Optional[bool] = Field(default=None, alias="isNotice", description="Whether the filing is a 13F notice")
    is_amendment: Optional[bool] = Field(default=None, alias="isAmendment", description="Whether the filing is an amendment")
    amendment_type: Optional[str] = Field(default=None, alias="amendmentType", description="Amendment type from the filing cover page")
    has_information_table: Optional[bool] = Field(default=None, alias="hasInformationTable", description="Whether an information table was loaded for this filing")
    holdings_loaded_count: Optional[int] = Field(default=None, alias="holdingsLoadedCount", description="Number of holdings rows loaded for this filing")
    security_count: Optional[int] = Field(default=None, alias="securityCount", description="Number of distinct CUSIPs loaded for this filing")
    portfolio_value: Optional[float] = Field(default=None, alias="portfolioValue", description="Aggregate portfolio value in USD for loaded holdings")
    other_manager_count: Optional[int] = Field(default=None, alias="otherManagerCount", description="Number of summary other managers disclosed on holdings reports")
    notice_manager_count: Optional[int] = Field(default=None, alias="noticeManagerCount", description="Number of notice managers disclosed on notice filings")
    holding_manager_link_count: Optional[int] = Field(default=None, alias="holdingManagerLinkCount", description="Number of holding-to-manager links for holdings rows")
    notice_managers: Optional[List[InstitutionFilingManager]] = Field(default=None, alias="noticeManagers", description="Notice managers disclosed by 13F-NT filings")
    other_managers: Optional[List[InstitutionFilingManager]] = Field(default=None, alias="otherManagers", description="Other managers disclosed by holdings reports")


class InstitutionFilingPeriodFiling(SecBaseModel):
    """Compact Form 13F filing entry for a report period"""
    form_type: Optional[str] = Field(default=None, alias="formType", description="SEC form type")
    report_type: Optional[str] = Field(default=None, alias="reportType", description="13F report type from the filing cover page")
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="SEC accession number")
    filing_date: Optional[datetime.date] = Field(default=None, alias="filingDate", description="Filing date")
    is_notice: Optional[bool] = Field(default=None, alias="isNotice", description="Whether the filing is a 13F notice")
    is_amendment: Optional[bool] = Field(default=None, alias="isAmendment", description="Whether the filing is an amendment")
    has_information_table: Optional[bool] = Field(default=None, alias="hasInformationTable", description="Whether an information table was loaded for this filing")
    holdings_loaded_count: Optional[int] = Field(default=None, alias="holdingsLoadedCount", description="Number of holdings rows loaded for this filing")
    notice_manager_count: Optional[int] = Field(default=None, alias="noticeManagerCount", description="Number of notice managers disclosed by this filing")
    other_manager_count: Optional[int] = Field(default=None, alias="otherManagerCount", description="Number of summary other managers disclosed by this filing")


class InstitutionFilingPeriod(SecBaseModel):
    """Form 13F filing coverage for one report period"""
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    period_of_report: Optional[datetime.date] = Field(default=None, alias="periodOfReport", description="13F period of report")
    period_status: Optional[str] = Field(default=None, alias="periodStatus", description="Period coverage status Allowed values: holdings_reported, notice_only, mixed, metadata_only")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Number of 13F filings for this CIK/report period")
    holdings_filing_count: Optional[int] = Field(default=None, alias="holdingsFilingCount", description="Number of holdings-bearing filings for this period")
    notice_filing_count: Optional[int] = Field(default=None, alias="noticeFilingCount", description="Number of notice filings for this period")
    amendment_filing_count: Optional[int] = Field(default=None, alias="amendmentFilingCount", description="Number of amendment filings for this period")
    holdings_loaded_count: Optional[int] = Field(default=None, alias="holdingsLoadedCount", description="Total holdings rows loaded across filings in this period")
    notice_manager_count: Optional[int] = Field(default=None, alias="noticeManagerCount", description="Total notice managers disclosed across filings in this period")
    other_manager_count: Optional[int] = Field(default=None, alias="otherManagerCount", description="Total summary other managers disclosed across filings in this period")
    filings: Optional[List[InstitutionFilingPeriodFiling]] = Field(default=None, description="Filings submitted by the CIK for this report period")


class InstitutionFilingPeriodsFilter(SecBaseModel):
    """Filters applied to institution Form 13F filing periods"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    year: Optional[int] = Field(default=None, description="Calendar year")


class InstitutionFilingPeriodsResponse(SecBaseModel):
    """Institution Form 13F filing period coverage response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    periods: Optional[List[InstitutionFilingPeriod]] = Field(default=None, description="Report periods where this CIK submitted Form 13F filings")
    filters: Optional[InstitutionFilingPeriodsFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionFilingsFilter(SecBaseModel):
    """Filters applied to institution Form 13F filings"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    form_type: Optional[str] = Field(default=None, alias="formType", description="SEC Form 13F type")
    page: Optional[int] = Field(default=None, description="1-based page offset")
    limit: Optional[int] = Field(default=None, description="Maximum filings returned")


class InstitutionsPagination(SecBaseModel):
    """Pagination metadata for institution results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class InstitutionFilingsResponse(SecBaseModel):
    """Institution Form 13F filings response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    filings: Optional[List[InstitutionFiling]] = Field(default=None, description="Form 13F filing disclosures")
    pagination: Optional[InstitutionsPagination] = Field(default=None, description="Pagination metadata")
    filters: Optional[InstitutionFilingsFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionHolding(SecBaseModel):
    """Single Form 13F holding row"""
    ticker: Optional[str] = Field(default=None, description="Primary ticker symbol when known")
    issuer_cik: Optional[str] = Field(default=None, alias="issuerCik", description="Issuer CIK when known")
    issuer_name: Optional[str] = Field(default=None, alias="issuerName", description="Issuer name reported in the holding row")
    title_of_class: Optional[str] = Field(default=None, alias="titleOfClass", description="Security title/class")
    cusip: Optional[str] = Field(default=None, description="CUSIP")
    put_call: Optional[str] = Field(default=None, alias="putCall", description="Put/call marker for options positions")
    shares: Optional[float] = Field(default=None, description="Shares or principal amount held")
    share_type: Optional[str] = Field(default=None, alias="shareType", description="Share type reported by SEC")
    value: Optional[float] = Field(default=None, description="Position value in USD")
    weight_percent: Optional[float] = Field(default=None, alias="weightPercent", description="Position weight in the selected 13F portfolio")
    investment_discretion: Optional[str] = Field(default=None, alias="investmentDiscretion", description="Investment discretion")
    voting_authority_sole: Optional[int] = Field(default=None, alias="votingAuthoritySole", description="Sole voting authority")
    voting_authority_shared: Optional[int] = Field(default=None, alias="votingAuthorityShared", description="Shared voting authority")
    voting_authority_none: Optional[int] = Field(default=None, alias="votingAuthorityNone", description="No voting authority")


class InstitutionHoldingsPeriod(SecBaseModel):
    """13F filing period selected for institution holdings"""
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    period_of_report: Optional[datetime.date] = Field(default=None, alias="periodOfReport", description="13F period of report")
    filing_date: Optional[datetime.date] = Field(default=None, alias="filingDate", description="13F filing date")
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="13F accession number")


class InstitutionHoldingsHistoryPeriod(SecBaseModel):
    """Institutional Form 13F holdings for one historical filing period"""
    period: Optional[InstitutionHoldingsPeriod] = Field(default=None, description="Selected 13F filing period")
    total_position_count: Optional[int] = Field(default=None, alias="totalPositionCount", description="Total number of holding rows in the filing")
    total_security_count: Optional[int] = Field(default=None, alias="totalSecurityCount", description="Total number of distinct CUSIPs in the filing")
    total_portfolio_value: Optional[float] = Field(default=None, alias="totalPortfolioValue", description="Aggregate 13F portfolio value in USD")
    holdings: Optional[List[InstitutionHolding]] = Field(default=None, description="Holding rows for the filing period")


class InstitutionPortfolioComposition(SecBaseModel):
    """Institutional Form 13F portfolio composition row"""
    rank: Optional[int] = Field(default=None, description="Rank within the selected composition level")
    sector: Optional[str] = Field(default=None, description="Sector label")
    industry: Optional[str] = Field(default=None, description="Industry label for industry-level rows")
    sic_code: Optional[str] = Field(default=None, alias="sicCode", description="SIC code for industry-level rows")
    position_count: Optional[int] = Field(default=None, alias="positionCount", description="Number of holding rows in this allocation bucket")
    security_count: Optional[int] = Field(default=None, alias="securityCount", description="Number of distinct CUSIPs in this allocation bucket")
    value: Optional[float] = Field(default=None, description="Aggregate 13F position value in USD for this allocation bucket")
    portfolio_weight_percent: Optional[float] = Field(default=None, alias="portfolioWeightPercent", description="Percent of the selected 13F portfolio represented by this allocation bucket")


class InstitutionPortfolioCompositionFilter(SecBaseModel):
    """Filters applied to the institution portfolio composition query"""
    cik: Optional[str] = Field(default=None, description="Normalized institutional manager CIK")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    classification_level: Optional[str] = Field(default=None, alias="classificationLevel", description="Portfolio composition classification level Allowed values: sector, industry")


class InstitutionPortfolioCompositionResponse(SecBaseModel):
    """Institutional Form 13F portfolio composition response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    period: Optional[InstitutionHoldingsPeriod] = Field(default=None, description="Selected 13F filing period")
    classification_level: Optional[str] = Field(default=None, alias="classificationLevel", description="Portfolio composition classification level Allowed values: sector, industry")
    total_position_count: Optional[int] = Field(default=None, alias="totalPositionCount", description="Total number of holding rows represented by this composition")
    total_security_count: Optional[int] = Field(default=None, alias="totalSecurityCount", description="Total number of distinct CUSIPs represented by this composition")
    total_portfolio_value: Optional[float] = Field(default=None, alias="totalPortfolioValue", description="Aggregate selected 13F portfolio value in USD")
    breakdown: Optional[List[InstitutionPortfolioComposition]] = Field(default=None, description="Portfolio allocation rows for the selected classification level")
    filters: Optional[InstitutionPortfolioCompositionFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionProfileFilter(SecBaseModel):
    """Filters applied to the institution profile query"""
    cik: Optional[str] = Field(default=None, description="Normalized institutional manager CIK")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")


class InstitutionProfileResponse(SecBaseModel):
    """Institutional Form 13F filer profile"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    form_type: Optional[str] = Field(default=None, alias="formType", description="Selected 13F form type")
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="Selected 13F accession number")
    filing_date: Optional[datetime.date] = Field(default=None, alias="filingDate", description="Selected 13F filing date")
    period_of_report: Optional[datetime.date] = Field(default=None, alias="periodOfReport", description="Selected 13F period of report")
    received_date: Optional[datetime.datetime] = Field(default=None, alias="receivedDate", description="Timestamp when the selected filing was received")
    source_url: Optional[str] = Field(default=None, alias="sourceUrl", description="SEC source URL for the selected filing")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Number of Form 13F filings stored for the manager")
    position_count: Optional[int] = Field(default=None, alias="positionCount", description="Number of holdings rows in the selected filing")
    security_count: Optional[int] = Field(default=None, alias="securityCount", description="Number of distinct CUSIPs in the selected filing")
    portfolio_value: Optional[float] = Field(default=None, alias="portfolioValue", description="Aggregate selected 13F portfolio value in USD")
    average_position_value: Optional[float] = Field(default=None, alias="averagePositionValue", description="Average position value in USD")
    other_manager_count: Optional[int] = Field(default=None, alias="otherManagerCount", description="Number of other managers disclosed on the selected filing")
    filters: Optional[InstitutionProfileFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionTradingActivityFilter(SecBaseModel):
    """Filters applied to the institution trading activity query"""
    cik: Optional[str] = Field(default=None, description="Normalized institutional manager CIK")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    activity_type: Optional[str] = Field(default=None, alias="activityType", description="Activity direction Allowed values: buy, sell")
    new_only: Optional[bool] = Field(default=None, alias="newOnly", description="When true, buy rows are limited to securities not held in the prior period")
    sold_out_only: Optional[bool] = Field(default=None, alias="soldOutOnly", description="When true, sell rows are limited to securities no longer held in the current period")
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")


class InstitutionTradingActivitySecurity(SecBaseModel):
    """Quarter-over-quarter 13F trading activity for one security in an institution portfolio"""
    rank: Optional[int] = Field(default=None, description="Rank within the selected activity direction")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol when matched to a security reference")
    issuer_cik: Optional[str] = Field(default=None, alias="issuerCik", description="Issuer CIK when matched to a security reference")
    cusip: Optional[str] = Field(default=None, description="CUSIP from the 13F information table")
    issuer_name: Optional[str] = Field(default=None, alias="issuerName", description="Issuer/security name")
    title_of_class: Optional[str] = Field(default=None, alias="titleOfClass", description="13F title of class")
    put_call: Optional[str] = Field(default=None, alias="putCall", description="Option side for 13F option rows")
    current_shares: Optional[float] = Field(default=None, alias="currentShares", description="Current-period shares or principal amount")
    prior_shares: Optional[float] = Field(default=None, alias="priorShares", description="Previous-period shares or principal amount")
    net_shares: Optional[float] = Field(default=None, alias="netShares", description="Current minus previous shares or principal amount")
    current_value: Optional[float] = Field(default=None, alias="currentValue", description="Current 13F value in USD")
    prior_value: Optional[float] = Field(default=None, alias="priorValue", description="Previous 13F value in USD")
    net_value: Optional[float] = Field(default=None, alias="netValue", description="Current minus previous 13F value in USD")
    activity_value: Optional[float] = Field(default=None, alias="activityValue", description="Absolute value or share amount used to rank this activity row")


class InstitutionTradingActivityResponse(SecBaseModel):
    """Paginated quarter-over-quarter institutional 13F trading activity response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    period: Optional[InstitutionChangesPeriod] = Field(default=None, description="13F periods compared by this activity response")
    activity_type: Optional[str] = Field(default=None, alias="activityType", description="Activity direction Allowed values: buy, sell")
    securities: Optional[List[InstitutionTradingActivitySecurity]] = Field(default=None, description="Securities matching the selected activity direction")
    pagination: Optional[InstitutionsPagination] = Field(default=None, description="Pagination metadata")
    filters: Optional[InstitutionTradingActivityFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionsActivityFilter(SecBaseModel):
    """Filters applied to the institutional activity query"""
    year: Optional[int] = Field(default=None, description="Requested calendar year")
    quarter: Optional[str] = Field(default=None, description="Requested fiscal quarter label")
    limit: Optional[int] = Field(default=None, description="Maximum rows returned per activity category")


class InstitutionsActivityPagination(SecBaseModel):
    """Pagination metadata for institutional activity results"""
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per category")


class InstitutionsActivityPeriod(SecBaseModel):
    """13F reporting periods used for activity comparison"""
    current_quarter: Optional[str] = Field(default=None, alias="currentQuarter", description="Selected 13F quarter")
    current_period_end: Optional[datetime.date] = Field(default=None, alias="currentPeriodEnd", description="Selected 13F period end date")
    previous_quarter: Optional[str] = Field(default=None, alias="previousQuarter", description="Previous available 13F quarter")
    previous_period_end: Optional[datetime.date] = Field(default=None, alias="previousPeriodEnd", description="Previous available 13F period end date")


class InstitutionsActivitySecurity(SecBaseModel):
    """Aggregated 13F activity for one security"""
    ticker: Optional[str] = Field(default=None, description="Ticker symbol when matched to a security reference")
    cusip: Optional[str] = Field(default=None, description="CUSIP from the 13F information table")
    issuer_name: Optional[str] = Field(default=None, alias="issuerName", description="Issuer/security name")
    title_of_class: Optional[str] = Field(default=None, alias="titleOfClass", description="13F title of class")
    put_call: Optional[str] = Field(default=None, alias="putCall", description="Option side for 13F option rows")
    filer_count: Optional[int] = Field(default=None, alias="filerCount", description="Number of current-period filers reporting the security")
    prior_filer_count: Optional[int] = Field(default=None, alias="priorFilerCount", description="Number of previous-period filers reporting the security")
    current_shares: Optional[float] = Field(default=None, alias="currentShares", description="Current aggregate shares or principal amount")
    prior_shares: Optional[float] = Field(default=None, alias="priorShares", description="Previous aggregate shares or principal amount")
    net_shares: Optional[float] = Field(default=None, alias="netShares", description="Current minus previous aggregate shares")
    current_value: Optional[float] = Field(default=None, alias="currentValue", description="Current aggregate 13F value in USD")
    prior_value: Optional[float] = Field(default=None, alias="priorValue", description="Previous aggregate 13F value in USD")
    net_value: Optional[float] = Field(default=None, alias="netValue", description="Current minus previous aggregate 13F value in USD")


class InstitutionsActivityResponse(SecBaseModel):
    """Market-wide institutional 13F activity response"""
    period: Optional[InstitutionsActivityPeriod] = Field(default=None, description="13F periods compared by this response")
    most_bought: Optional[List[InstitutionsActivitySecurity]] = Field(default=None, alias="mostBought", description="Securities with the largest positive quarter-over-quarter changes")
    most_sold: Optional[List[InstitutionsActivitySecurity]] = Field(default=None, alias="mostSold", description="Securities with the largest negative quarter-over-quarter changes")
    new_positions: Optional[List[InstitutionsActivitySecurity]] = Field(default=None, alias="newPositions", description="Securities that appear in the selected period but not the previous period")
    closed_positions: Optional[List[InstitutionsActivitySecurity]] = Field(default=None, alias="closedPositions", description="Securities that appeared in the previous period but not the selected period")
    pagination: Optional[InstitutionsActivityPagination] = Field(default=None, description="Pagination metadata for category lists")
    filters: Optional[InstitutionsActivityFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionsFilter(SecBaseModel):
    """Filters applied to the institutions query"""
    q: Optional[str] = Field(default=None, description="Institution name search substring")


class InstitutionsHoldingsFilter(SecBaseModel):
    """Filters applied to the institution holdings query"""
    cik: Optional[str] = Field(default=None, description="Normalized institutional manager CIK")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    limit: Optional[int] = Field(default=None, description="Maximum number of holding rows requested")
    sort: Optional[str] = Field(default=None, description="Sort key Allowed values: value, shares, weight")


class InstitutionsHoldingsHistoryFilter(SecBaseModel):
    """Filters applied to the institution holdings history query"""
    cik: Optional[str] = Field(default=None, description="Normalized institutional manager CIK")
    year: Optional[int] = Field(default=None, description="Requested calendar year")
    quarter: Optional[str] = Field(default=None, description="Fiscal quarter label")
    limit: Optional[int] = Field(default=None, description="Maximum number of holding rows requested per filing period")
    sort: Optional[str] = Field(default=None, description="Sort key Allowed values: value, shares, weight")


class InstitutionsHoldingsPagination(SecBaseModel):
    """Pagination metadata for institution holdings results"""
    limit: Optional[int] = Field(default=None, description="Maximum number of holding rows requested")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether more holding rows are available")


class InstitutionsHoldingsHistoryResponse(SecBaseModel):
    """Historical institutional Form 13F holdings response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    periods: Optional[List[InstitutionHoldingsHistoryPeriod]] = Field(default=None, description="Historical filing periods and their holding rows")
    pagination: Optional[InstitutionsHoldingsPagination] = Field(default=None, description="Pagination metadata for holding rows per period")
    filters: Optional[InstitutionsHoldingsHistoryFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionsHoldingsResponse(SecBaseModel):
    """Institutional Form 13F holdings response"""
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    name: Optional[str] = Field(default=None, description="Institutional manager display name")
    period: Optional[InstitutionHoldingsPeriod] = Field(default=None, description="Selected 13F filing period")
    total_position_count: Optional[int] = Field(default=None, alias="totalPositionCount", description="Total number of holding rows in the selected filing")
    total_security_count: Optional[int] = Field(default=None, alias="totalSecurityCount", description="Total number of distinct CUSIPs in the selected filing")
    total_portfolio_value: Optional[float] = Field(default=None, alias="totalPortfolioValue", description="Aggregate selected 13F portfolio value in USD")
    holdings: Optional[List[InstitutionHolding]] = Field(default=None, description="Holding rows for the selected filing")
    pagination: Optional[InstitutionsHoldingsPagination] = Field(default=None, description="Pagination metadata for holding rows")
    filters: Optional[InstitutionsHoldingsFilter] = Field(default=None, description="Filters applied to the query")


class InstitutionsListResponse(SecBaseModel):
    """Paginated institutional Form 13F filer directory response"""
    data: Optional[List[Institution]] = Field(default=None, description="Institutional filers returned for the current page")
    pagination: Optional[InstitutionsPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[InstitutionsFilter] = Field(default=None, description="Filters applied to the query")


__all__ = [
    "Institution",
    "InstitutionChangesFilter",
    "InstitutionChangesMetrics",
    "InstitutionChangesPeriod",
    "InstitutionChangesResponse",
    "InstitutionFiling",
    "InstitutionFilingManager",
    "InstitutionFilingPeriod",
    "InstitutionFilingPeriodFiling",
    "InstitutionFilingPeriodsFilter",
    "InstitutionFilingPeriodsResponse",
    "InstitutionFilingsFilter",
    "InstitutionFilingsResponse",
    "InstitutionHolding",
    "InstitutionHoldingsHistoryPeriod",
    "InstitutionHoldingsPeriod",
    "InstitutionPortfolioComposition",
    "InstitutionPortfolioCompositionFilter",
    "InstitutionPortfolioCompositionResponse",
    "InstitutionProfileFilter",
    "InstitutionProfileResponse",
    "InstitutionsActivityFilter",
    "InstitutionsActivityPagination",
    "InstitutionsActivityPeriod",
    "InstitutionsActivityResponse",
    "InstitutionsActivitySecurity",
    "InstitutionsFilter",
    "InstitutionsHoldingsFilter",
    "InstitutionsHoldingsHistoryFilter",
    "InstitutionsHoldingsHistoryResponse",
    "InstitutionsHoldingsPagination",
    "InstitutionsHoldingsResponse",
    "InstitutionsListResponse",
    "InstitutionsPagination",
    "InstitutionTradingActivityFilter",
    "InstitutionTradingActivityResponse",
    "InstitutionTradingActivitySecurity",
]

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, SecBaseModel):
        _m.model_rebuild()
