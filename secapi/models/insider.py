"""Auto-generated SEC API models. Do not edit by hand.

Regenerate with: python scripts/generate_models.py
"""

from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import Field

from ._base import SecBaseModel


class InsiderIssuer(SecBaseModel):
    """Issuer identity from a Form 4 filing"""
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit issuer CIK")
    ticker: Optional[str] = Field(default=None, description="Issuer ticker symbol recorded on the filing")
    name: Optional[str] = Field(default=None, description="Issuer legal name recorded on the filing")


class InsiderBuySellRatioResponse(SecBaseModel):
    """Ticker-level Form 4 insider buy/sell ratio snapshot"""
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer represented by the Form 4 insider transaction snapshot")
    buy_transaction_count: Optional[int] = Field(default=None, alias="buyTransactionCount", description="Number of acquired transaction rows")
    sell_transaction_count: Optional[int] = Field(default=None, alias="sellTransactionCount", description="Number of disposed transaction rows")
    directional_transaction_count: Optional[int] = Field(default=None, alias="directionalTransactionCount", description="Number of acquired plus disposed transaction rows")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Total Form 4 transaction rows in the snapshot")
    buy_sell_ratio: Optional[float] = Field(default=None, alias="buySellRatio", description="Buy transaction count divided by sell transaction count. Null when there are no sell rows.")
    latest_transaction_date: Optional[datetime.date] = Field(default=None, alias="latestTransactionDate", description="Most recent transaction date found for the issuer")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime for the most recent Form 4")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Most recent Form 4 accession number for the issuer")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL for the most recent Form 4")


class InsiderCompaniesFilter(SecBaseModel):
    """Normalized filters applied to the insider companies query"""
    q: Optional[str] = Field(default=None, description="Issuer name, ticker, or CIK search substring")


class InsiderCompaniesPagination(SecBaseModel):
    """Pagination metadata for insider company results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class InsiderCompany(SecBaseModel):
    """Company with Form 4 insider data"""
    cik: Optional[str] = Field(default=None, description="Issuer CIK recorded on Form 4 filings")
    ticker: Optional[str] = Field(default=None, description="Issuer ticker symbol recorded on the latest Form 4 filing")
    name: Optional[str] = Field(default=None, description="Issuer legal name recorded on the latest Form 4 filing")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Most recent Form 4 accession number for the issuer")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL for the most recent Form 4")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime for the most recent Form 4")
    latest_transaction_date: Optional[datetime.date] = Field(default=None, alias="latestTransactionDate", description="Most recent transaction date found for the issuer")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Number of Form 4 filings stored for the issuer")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Number of Form 4 transaction rows stored for the issuer")
    reporter_count: Optional[int] = Field(default=None, alias="reporterCount", description="Number of distinct reporting owner CIKs linked to the issuer")


class InsiderCompaniesResponse(SecBaseModel):
    """Paginated directory of companies with Form 4 insider data"""
    data: Optional[List[InsiderCompany]] = Field(default=None, description="Companies returned for the current page")
    pagination: Optional[InsiderCompaniesPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[InsiderCompaniesFilter] = Field(default=None, description="Normalized filters that were applied to the query")


class InsiderHoldingSecurityTypeSummary(SecBaseModel):
    """Aggregated insider ownership shares for one issuer security type"""
    security_type: Optional[str] = Field(default=None, alias="securityType", description="Security title/type. Different share classes remain separate here.")
    total_shares: Optional[float] = Field(default=None, alias="totalShares", description="Heuristic sum of current shares for this security type")
    direct_shares: Optional[float] = Field(default=None, alias="directShares", description="Heuristic sum of shares marked direct ownership (D)")
    indirect_shares: Optional[float] = Field(default=None, alias="indirectShares", description="Heuristic sum of shares marked indirect ownership (I)")
    unspecified_ownership_shares: Optional[float] = Field(default=None, alias="unspecifiedOwnershipShares", description="Heuristic sum of shares without a D/I ownership flag")
    non_derivative_shares: Optional[float] = Field(default=None, alias="nonDerivativeShares", description="Heuristic sum of non-derivative shares for this security type")
    derivative_shares: Optional[float] = Field(default=None, alias="derivativeShares", description="Heuristic sum of derivative shares for this security type")
    position_count: Optional[int] = Field(default=None, alias="positionCount", description="Number of snapshot positions contributing to this security-type total")


class InsiderCompanyOwner(SecBaseModel):
    """Ranked insider owner for one issuer"""
    rank: Optional[int] = Field(default=None, description="Rank within the issuer by total included shares")
    reporter_cik: Optional[str] = Field(default=None, alias="reporterCik", description="Zero-padded 10-digit reporting owner CIK")
    reporter_name: Optional[str] = Field(default=None, alias="reporterName", description="Reporting owner name")
    director: Optional[bool] = Field(default=None, description="Whether the owner is reported as a director")
    officer: Optional[bool] = Field(default=None, description="Whether the owner is reported as an officer")
    ten_percent_owner: Optional[bool] = Field(default=None, alias="tenPercentOwner", description="Whether the owner is reported as a ten percent owner")
    officer_title: Optional[str] = Field(default=None, alias="officerTitle", description="Latest reported officer title")
    total_shares: Optional[float] = Field(default=None, alias="totalShares", description="Heuristic sum of current shares across included positions and security types")
    direct_shares: Optional[float] = Field(default=None, alias="directShares", description="Heuristic sum of shares marked direct ownership (D)")
    indirect_shares: Optional[float] = Field(default=None, alias="indirectShares", description="Heuristic sum of shares marked indirect ownership (I)")
    unspecified_ownership_shares: Optional[float] = Field(default=None, alias="unspecifiedOwnershipShares", description="Heuristic sum of shares without a D/I ownership flag")
    non_derivative_shares: Optional[float] = Field(default=None, alias="nonDerivativeShares", description="Heuristic sum of included non-derivative shares")
    derivative_shares: Optional[float] = Field(default=None, alias="derivativeShares", description="Heuristic sum of included derivative shares")
    position_count: Optional[int] = Field(default=None, alias="positionCount", description="Number of snapshot positions contributing to this owner total")
    latest_position_date: Optional[datetime.date] = Field(default=None, alias="latestPositionDate", description="Latest date used to compute this owner's included positions")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime from the latest contributing snapshot row")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Latest source filing accession number")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL from the latest source filing")
    security_types: Optional[List[InsiderHoldingSecurityTypeSummary]] = Field(default=None, alias="securityTypes", description="Breakdown by security title/type. Share classes such as Class A and Class B remain separate here.")


class InsiderDailyActivityFilter(SecBaseModel):
    """Normalized filters applied to the daily insider activity query"""
    activity_date: Optional[datetime.date] = Field(default=None, alias="activityDate", description="Transaction date for the leaderboard")
    activity_type: Optional[str] = Field(default=None, alias="activityType", description="Leaderboard type Allowed values: top_buyers, top_sellers")
    limit: Optional[int] = Field(default=None, description="Maximum number of ranked issuers returned")


class InsiderDailyActivityLeader(SecBaseModel):
    """Ranked issuer on a single day by insider buy or sell activity"""
    rank: Optional[int] = Field(default=None, description="Rank for the activity type on this date (1 = largest)")
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer on the leaderboard")
    buy_value: Optional[float] = Field(default=None, alias="buyValue", description="Total acquired transaction value on this date (USD)")
    sell_value: Optional[float] = Field(default=None, alias="sellValue", description="Total disposed transaction value on this date (USD)")
    net_value: Optional[float] = Field(default=None, alias="netValue", description="Acquired minus disposed transaction value on this date (USD)")
    buy_shares: Optional[float] = Field(default=None, alias="buyShares", description="Total acquired shares on this date")
    sell_shares: Optional[float] = Field(default=None, alias="sellShares", description="Total disposed shares on this date")
    buy_transaction_count: Optional[int] = Field(default=None, alias="buyTransactionCount", description="Acquired Form 4 transaction rows on this date")
    sell_transaction_count: Optional[int] = Field(default=None, alias="sellTransactionCount", description="Disposed Form 4 transaction rows on this date")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Total Form 4 transaction rows on this date")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Distinct Form 4 filings on this date")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="Most recent SEC acceptance datetime among filings on this date")


class InsiderDailyActivityResponse(SecBaseModel):
    """Daily ranked insider buyers or sellers by issuer transaction value"""
    activity_date: Optional[datetime.date] = Field(default=None, alias="activityDate", description="Transaction date for the leaderboard")
    activity_type: Optional[str] = Field(default=None, alias="activityType", description="Leaderboard type")
    data: Optional[List[InsiderDailyActivityLeader]] = Field(default=None, description="Ranked issuers for the date and activity type")
    filters: Optional[InsiderDailyActivityFilter] = Field(default=None, description="Normalized filters that were applied to the query")


class InsiderHolding(SecBaseModel):
    """Current insider ownership position from the ownership snapshot"""
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer for this ownership position")
    security_type: Optional[str] = Field(default=None, alias="securityType", description="Security title/type")
    current_shares: Optional[float] = Field(default=None, alias="currentShares", description="Current shares owned in this position")
    direct_or_indirect_ownership: Optional[str] = Field(default=None, alias="directOrIndirectOwnership", description="Direct or indirect ownership flag")
    nature_of_ownership: Optional[str] = Field(default=None, alias="natureOfOwnership", description="Nature of ownership")
    derivative: Optional[bool] = Field(default=None, description="Whether this is a derivative ownership position")
    underlying_security_title: Optional[str] = Field(default=None, alias="underlyingSecurityTitle", description="Underlying security title for derivative positions")
    underlying_security_shares: Optional[float] = Field(default=None, alias="underlyingSecurityShares", description="Underlying security shares for derivative positions")
    exercise_price: Optional[float] = Field(default=None, alias="exercisePrice", description="Exercise price for derivative positions")
    exercise_date: Optional[datetime.date] = Field(default=None, alias="exerciseDate", description="Exercise date for derivative positions")
    expiration_date: Optional[datetime.date] = Field(default=None, alias="expirationDate", description="Expiration date for derivative positions")
    latest_position_date: Optional[datetime.date] = Field(default=None, alias="latestPositionDate", description="Latest date used to compute this position")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime for the latest source filing")
    latest_source_form: Optional[str] = Field(default=None, alias="latestSourceForm", description="Latest source form that contributed this position")
    latest_source_kind: Optional[str] = Field(default=None, alias="latestSourceKind", description="Latest source row kind that contributed this position")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Latest source filing accession number")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL for the latest source filing")


class InsiderHoldingIssuerSummary(SecBaseModel):
    """Aggregated insider ownership shares for one issuer"""
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer represented by the latest contributing snapshot row")
    total_shares: Optional[float] = Field(default=None, alias="totalShares", description="Heuristic sum of current shares across included positions and security types")
    direct_shares: Optional[float] = Field(default=None, alias="directShares", description="Heuristic sum of shares marked direct ownership (D)")
    indirect_shares: Optional[float] = Field(default=None, alias="indirectShares", description="Heuristic sum of shares marked indirect ownership (I)")
    unspecified_ownership_shares: Optional[float] = Field(default=None, alias="unspecifiedOwnershipShares", description="Heuristic sum of shares without a D/I ownership flag")
    non_derivative_shares: Optional[float] = Field(default=None, alias="nonDerivativeShares", description="Heuristic sum of included non-derivative shares")
    derivative_shares: Optional[float] = Field(default=None, alias="derivativeShares", description="Heuristic sum of included derivative shares")
    position_count: Optional[int] = Field(default=None, alias="positionCount", description="Number of snapshot positions contributing to this issuer total")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime from the latest contributing snapshot row")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Latest source filing accession number from the chosen issuer source row")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL from the chosen issuer source row")
    security_types: Optional[List[InsiderHoldingSecurityTypeSummary]] = Field(default=None, alias="securityTypes", description="Breakdown by security title/type. Share classes such as Class A and Class B remain separate here.")


class InsiderHoldingsResponse(SecBaseModel):
    """Current ownership positions for an insider person"""
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit reporting owner CIK")
    holdings: Optional[List[InsiderHolding]] = Field(default=None, description="Current ownership positions ordered by issuer and security")


class InsiderHoldingsSummaryFilter(SecBaseModel):
    """Filters applied to the insider holdings summary"""
    include_derivative: Optional[bool] = Field(default=None, alias="includeDerivative", description="Whether derivative ownership positions were included")
    include_non_derivative: Optional[bool] = Field(default=None, alias="includeNonDerivative", description="Whether non-derivative ownership positions were included")


class InsiderHoldingsSummaryResponse(SecBaseModel):
    """Per-issuer summary of current ownership snapshot positions for an insider person"""
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit reporting owner CIK")
    filters: Optional[InsiderHoldingsSummaryFilter] = Field(default=None, description="Filters applied to the summary")
    methodology: Optional[str] = Field(default=None, description="Heuristic methodology warning. These totals are not SEC-certified total beneficial ownership and may double-count or omit exposure across trusts, ownership forms, derivatives, and share classes.")
    issuers: Optional[List[InsiderHoldingIssuerSummary]] = Field(default=None, description="Issuer-level holdings summaries ordered by issuer ticker/name/CIK")


class InsiderNetSharesResponse(SecBaseModel):
    """Ticker-level Form 4 insider net shares snapshot"""
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer represented by the Form 4 insider transaction snapshot")
    buy_shares: Optional[float] = Field(default=None, alias="buyShares", description="Total acquired shares in Form 4 transaction rows")
    sell_shares: Optional[float] = Field(default=None, alias="sellShares", description="Total disposed shares in Form 4 transaction rows")
    net_shares: Optional[float] = Field(default=None, alias="netShares", description="Acquired shares minus disposed shares")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Total Form 4 transaction rows in the snapshot")
    latest_transaction_date: Optional[datetime.date] = Field(default=None, alias="latestTransactionDate", description="Most recent transaction date found for the issuer")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime for the most recent Form 4")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Most recent Form 4 accession number for the issuer")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL for the most recent Form 4")


class InsiderNetValueResponse(SecBaseModel):
    """Ticker-level Form 4 insider net transaction value snapshot"""
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer represented by the Form 4 insider transaction snapshot")
    buy_value: Optional[float] = Field(default=None, alias="buyValue", description="Total value of acquired Form 4 transaction rows")
    sell_value: Optional[float] = Field(default=None, alias="sellValue", description="Total value of disposed Form 4 transaction rows")
    net_value: Optional[float] = Field(default=None, alias="netValue", description="Acquired transaction value minus disposed transaction value")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Total Form 4 transaction rows in the snapshot")
    latest_transaction_date: Optional[datetime.date] = Field(default=None, alias="latestTransactionDate", description="Most recent transaction date found for the issuer")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime for the most recent Form 4")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Most recent Form 4 accession number for the issuer")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL for the most recent Form 4")


class InsiderOwnersFilter(SecBaseModel):
    """Filters applied to company insider owner rankings"""
    include_derivative: Optional[bool] = Field(default=None, alias="includeDerivative", description="Whether derivative ownership positions were included")
    include_non_derivative: Optional[bool] = Field(default=None, alias="includeNonDerivative", description="Whether non-derivative ownership positions were included")
    active_since: Optional[datetime.date] = Field(default=None, alias="activeSince", description="Only ownership positions updated on or after this date were included")
    limit: Optional[int] = Field(default=None, description="Maximum owners returned")


class InsiderOwnersResponse(SecBaseModel):
    """Ranked current insider owners for a company"""
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer represented by the ownership snapshot rows")
    filters: Optional[InsiderOwnersFilter] = Field(default=None, description="Filters applied to the ranking")
    methodology: Optional[str] = Field(default=None, description="Heuristic methodology warning. These totals are not SEC-certified total beneficial ownership and may double-count or omit exposure across trusts, ownership forms, derivatives, and share classes.")
    owners: Optional[List[InsiderCompanyOwner]] = Field(default=None, description="Insider owners ordered by included total shares descending")


class InsiderPerson(SecBaseModel):
    """Insider person derived from the ownership snapshot"""
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit reporting owner CIK")
    name: Optional[str] = Field(default=None, description="Latest reported owner name")
    director: Optional[bool] = Field(default=None, description="Whether any stored filing reports this person as a director")
    officer: Optional[bool] = Field(default=None, description="Whether any stored filing reports this person as an officer")
    ten_percent_owner: Optional[bool] = Field(default=None, alias="tenPercentOwner", description="Whether any stored filing reports this person as a ten percent owner")
    latest_officer_title: Optional[str] = Field(default=None, alias="latestOfficerTitle", description="Officer title from the latest stored filing when available")
    latest_issuer: Optional[InsiderIssuer] = Field(default=None, alias="latestIssuer", description="Issuer from the latest source filing for this person")
    latest_accession_number: Optional[str] = Field(default=None, alias="latestAccessionNumber", description="Most recent source filing accession number for this person")
    latest_filing_url: Optional[str] = Field(default=None, alias="latestFilingUrl", description="SEC filing URL for the most recent source filing")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="SEC acceptance datetime for the most recent source filing")
    latest_transaction_date: Optional[datetime.date] = Field(default=None, alias="latestTransactionDate", description="Most recent position date represented by this person's snapshot rows")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Number of distinct source filings represented by this person's snapshot rows")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Number of transaction source rows represented by this person's snapshot rows")
    issuer_count: Optional[int] = Field(default=None, alias="issuerCount", description="Number of distinct issuers linked to this person")


class InsiderPersonsFilter(SecBaseModel):
    """Normalized filters applied to the insider persons query"""
    q: Optional[str] = Field(default=None, description="Reporter name or CIK search substring")


class InsiderPersonsPagination(SecBaseModel):
    """Pagination metadata for insider person results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class InsiderPersonsResponse(SecBaseModel):
    """Paginated directory of insider persons from the ownership snapshot"""
    data: Optional[List[InsiderPerson]] = Field(default=None, description="Insider persons returned for the current page")
    pagination: Optional[InsiderPersonsPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[InsiderPersonsFilter] = Field(default=None, description="Normalized filters that were applied to the query")


class InsiderReporter(SecBaseModel):
    """Reporting owner associated with a Form 4 transaction"""
    cik: Optional[str] = Field(default=None, description="Zero-padded 10-digit reporter CIK")
    name: Optional[str] = Field(default=None, description="Reporter name")
    director: Optional[bool] = Field(default=None, description="Whether the reporter is a director")
    officer: Optional[bool] = Field(default=None, description="Whether the reporter is an officer")
    ten_percent_owner: Optional[bool] = Field(default=None, alias="tenPercentOwner", description="Whether the reporter is a ten percent owner")
    officer_title: Optional[str] = Field(default=None, alias="officerTitle", description="Officer title as reported on the filing")


class InsiderStatisticsResponse(SecBaseModel):
    """Aggregated Form 4 insider statistics across all covered issuers"""
    company_count: Optional[int] = Field(default=None, alias="companyCount", description="Number of issuers with Form 4 insider transaction snapshot data")
    person_count: Optional[int] = Field(default=None, alias="personCount", description="Number of distinct reporting owners in the insider ownership snapshot")
    filing_count: Optional[int] = Field(default=None, alias="filingCount", description="Total Form 4 filings across all issuers")
    transaction_count: Optional[int] = Field(default=None, alias="transactionCount", description="Total Form 4 transaction rows across all issuers")
    buy_transaction_count: Optional[int] = Field(default=None, alias="buyTransactionCount", description="Total acquired Form 4 transaction rows")
    sell_transaction_count: Optional[int] = Field(default=None, alias="sellTransactionCount", description="Total disposed Form 4 transaction rows")
    directional_transaction_count: Optional[int] = Field(default=None, alias="directionalTransactionCount", description="Total acquired plus disposed Form 4 transaction rows")
    derivative_transaction_count: Optional[int] = Field(default=None, alias="derivativeTransactionCount", description="Total derivative Form 4 transaction rows")
    buy_sell_ratio: Optional[float] = Field(default=None, alias="buySellRatio", description="Buy transaction count divided by sell transaction count. Null when there are no sell rows.")
    buy_shares: Optional[float] = Field(default=None, alias="buyShares", description="Total acquired shares in Form 4 transaction rows")
    sell_shares: Optional[float] = Field(default=None, alias="sellShares", description="Total disposed shares in Form 4 transaction rows")
    net_shares: Optional[float] = Field(default=None, alias="netShares", description="Acquired shares minus disposed shares")
    buy_value: Optional[float] = Field(default=None, alias="buyValue", description="Total value of acquired Form 4 transaction rows (USD)")
    sell_value: Optional[float] = Field(default=None, alias="sellValue", description="Total value of disposed Form 4 transaction rows (USD)")
    net_value: Optional[float] = Field(default=None, alias="netValue", description="Acquired transaction value minus disposed transaction value (USD)")
    latest_transaction_date: Optional[datetime.date] = Field(default=None, alias="latestTransactionDate", description="Most recent transaction date found in the universe")
    latest_accepted: Optional[datetime.datetime] = Field(default=None, alias="latestAccepted", description="Most recent SEC acceptance datetime found in the universe")


class InsiderTransaction(SecBaseModel):
    """One Form 4 transaction row"""
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="SEC accession number for the Form 4 filing")
    filing_url: Optional[str] = Field(default=None, alias="filingUrl", description="SEC filing URL when available")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")
    issuer: Optional[InsiderIssuer] = Field(default=None, description="Issuer from the Form 4 filing")
    reporter: Optional[InsiderReporter] = Field(default=None, description="Reporting owner from the Form 4 filing")
    security_type: Optional[str] = Field(default=None, alias="securityType", description="Security title/type")
    transaction_date: Optional[datetime.date] = Field(default=None, alias="transactionDate", description="Transaction date")
    deemed_execution_date: Optional[datetime.date] = Field(default=None, alias="deemedExecutionDate", description="Deemed execution date")
    transaction_code: Optional[str] = Field(default=None, alias="transactionCode", description="SEC transaction code")
    type: Optional[str] = Field(default=None, description="Buy/sell interpretation based on acquired/disposed flag")
    shares: Optional[float] = Field(default=None, description="Shares transacted")
    price_per_share: Optional[float] = Field(default=None, alias="pricePerShare", description="Transaction price per share")
    value: Optional[float] = Field(default=None, description="Estimated transaction value: shares multiplied by price per share")
    acquired_disposed: Optional[str] = Field(default=None, alias="acquiredDisposed", description="Acquired/disposed flag from SEC data Allowed values: A, D")
    shares_owned_following_transaction: Optional[float] = Field(default=None, alias="sharesOwnedFollowingTransaction", description="Shares owned following the transaction")
    direct_or_indirect_ownership: Optional[str] = Field(default=None, alias="directOrIndirectOwnership", description="Direct or indirect ownership flag")
    nature_of_ownership: Optional[str] = Field(default=None, alias="natureOfOwnership", description="Nature of ownership")
    derivative: Optional[bool] = Field(default=None, description="Whether this is a derivative transaction row")
    underlying_security_title: Optional[str] = Field(default=None, alias="underlyingSecurityTitle", description="Underlying security title for derivative rows")
    underlying_security_shares: Optional[float] = Field(default=None, alias="underlyingSecurityShares", description="Underlying security shares for derivative rows")
    exercise_price: Optional[float] = Field(default=None, alias="exercisePrice", description="Exercise price for derivative rows")
    exercise_date: Optional[datetime.date] = Field(default=None, alias="exerciseDate", description="Exercise date for derivative rows")
    expiration_date: Optional[datetime.date] = Field(default=None, alias="expirationDate", description="Expiration date for derivative rows")


class InsiderTransactionsFilter(SecBaseModel):
    """Filters applied to the insider transaction feed"""
    acquired_disposed: Optional[str] = Field(default=None, alias="acquiredDisposed", description="Requested acquired/disposed filter Allowed values: A, D")
    transaction_code: Optional[str] = Field(default=None, alias="transactionCode", description="SEC transaction code")
    derivative: Optional[bool] = Field(default=None, description="Derivative row filter")
    insider_role: Optional[str] = Field(default=None, alias="insiderRole", description="Reported insider role/title filter")
    min_value: Optional[int] = Field(default=None, alias="minValue", description="Minimum estimated transaction value")
    accepted_from: Optional[datetime.date] = Field(default=None, alias="acceptedFrom", description="Include SEC filings accepted on or after this date")
    transaction_from: Optional[datetime.date] = Field(default=None, alias="transactionFrom", description="Include transactions dated on or after this date")
    transaction_to: Optional[datetime.date] = Field(default=None, alias="transactionTo", description="Include transactions dated on or before this date")
    limit: Optional[int] = Field(default=None, description="Maximum rows returned")


class InsiderTransactionsPagination(SecBaseModel):
    """Pagination metadata for insider transaction feed results"""
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether more records are available after this result set")


class InsiderTransactionsResponse(SecBaseModel):
    """Global insider transaction feed response"""
    transactions: Optional[List[InsiderTransaction]] = Field(default=None, description="Transaction rows ordered by SEC acceptance time and transaction date descending")
    pagination: Optional[InsiderTransactionsPagination] = Field(default=None, description="Pagination metadata for this feed")
    filters: Optional[InsiderTransactionsFilter] = Field(default=None, description="Normalized filters applied to the query")


__all__ = [
    "InsiderBuySellRatioResponse",
    "InsiderCompaniesFilter",
    "InsiderCompaniesPagination",
    "InsiderCompaniesResponse",
    "InsiderCompany",
    "InsiderCompanyOwner",
    "InsiderDailyActivityFilter",
    "InsiderDailyActivityLeader",
    "InsiderDailyActivityResponse",
    "InsiderHolding",
    "InsiderHoldingIssuerSummary",
    "InsiderHoldingSecurityTypeSummary",
    "InsiderHoldingsResponse",
    "InsiderHoldingsSummaryFilter",
    "InsiderHoldingsSummaryResponse",
    "InsiderIssuer",
    "InsiderNetSharesResponse",
    "InsiderNetValueResponse",
    "InsiderOwnersFilter",
    "InsiderOwnersResponse",
    "InsiderPerson",
    "InsiderPersonsFilter",
    "InsiderPersonsPagination",
    "InsiderPersonsResponse",
    "InsiderReporter",
    "InsiderStatisticsResponse",
    "InsiderTransaction",
    "InsiderTransactionsFilter",
    "InsiderTransactionsPagination",
    "InsiderTransactionsResponse",
]

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, SecBaseModel):
        _m.model_rebuild()
