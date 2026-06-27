"""Auto-generated SEC API models. Do not edit by hand.

Regenerate with: python scripts/generate_models.py
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ._base import SecBaseModel


class EntitiesFilter(SecBaseModel):
    """Normalized filters applied to the entities query"""
    cik: Optional[str] = Field(default=None, description="Normalized CIK filter")
    ticker: Optional[str] = Field(default=None, description="Normalized uppercase ticker filter")
    entity_type: Optional[str] = Field(default=None, alias="entityType", description="API entity class filter")
    q: Optional[str] = Field(default=None, description="Name search substring")


class EntitiesPagination(SecBaseModel):
    """Pagination metadata for entity results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class EntityAddress(SecBaseModel):
    """SEC entity mailing or business address"""
    street1: Optional[str] = Field(default=None, description="First street line")
    street2: Optional[str] = Field(default=None, description="Second street line")
    city: Optional[str] = Field(default=None, description="City")
    state_or_country: Optional[str] = Field(default=None, alias="stateOrCountry", description="State or country code")
    zip_code: Optional[str] = Field(default=None, alias="zipCode", description="Postal code")
    state_or_country_description: Optional[str] = Field(default=None, alias="stateOrCountryDescription", description="State or country description")
    foreign_location: Optional[bool] = Field(default=None, alias="foreignLocation", description="Whether the address is marked as foreign")
    foreign_state_territory: Optional[str] = Field(default=None, alias="foreignStateTerritory", description="Foreign state or territory")
    country: Optional[str] = Field(default=None, description="Country name")
    country_code: Optional[str] = Field(default=None, alias="countryCode", description="Country code")


class Entity(SecBaseModel):
    """SEC registrant identity (company, individual, fund, etc.)"""
    name: Optional[str] = Field(default=None, description="Display name")
    cik: Optional[str] = Field(default=None, description="10-digit Central Index Key")
    ticker: Optional[str] = Field(default=None, description="Primary trading symbol when available")
    entity_type: Optional[str] = Field(default=None, alias="entityType", description="High-level entity class for clients Allowed values: company, individual, institution, unknown")
    tickers: Optional[List[str]] = Field(default=None, description="All known ticker symbols for the entity")
    exchanges: Optional[List[str]] = Field(default=None, description="All known trading venues for the entity")
    sic: Optional[str] = Field(default=None, description="SEC Standard Industrial Classification code")
    sic_description: Optional[str] = Field(default=None, alias="sicDescription", description="SEC Standard Industrial Classification description")
    owner_org: Optional[str] = Field(default=None, alias="ownerOrg", description="Owner organization reported by SEC source data")
    insider_transaction_for_owner_exists: Optional[bool] = Field(default=None, alias="insiderTransactionForOwnerExists", description="Whether owner-side insider transactions exist for this entity")
    insider_transaction_for_issuer_exists: Optional[bool] = Field(default=None, alias="insiderTransactionForIssuerExists", description="Whether issuer-side insider transactions exist for this entity")
    ein: Optional[str] = Field(default=None, description="Employer Identification Number when available")
    lei: Optional[str] = Field(default=None, description="Legal Entity Identifier when available")
    description: Optional[str] = Field(default=None, description="Long-form entity description from SEC source data")
    website: Optional[str] = Field(default=None, description="Primary company website")
    investor_website: Optional[str] = Field(default=None, alias="investorWebsite", description="Investor relations website")
    category: Optional[str] = Field(default=None, description="SEC filing category such as accelerated filer status")
    fiscal_year_end: Optional[str] = Field(default=None, alias="fiscalYearEnd", description="Fiscal year end in MMDD format")
    state_of_incorporation: Optional[str] = Field(default=None, alias="stateOfIncorporation", description="State of incorporation code")
    state_of_incorporation_description: Optional[str] = Field(default=None, alias="stateOfIncorporationDescription", description="State of incorporation description")
    phone: Optional[str] = Field(default=None, description="Primary contact phone number")
    former_names: Optional[List[str]] = Field(default=None, alias="formerNames", description="Former names reported for the entity")
    mailing_address: Optional[EntityAddress] = Field(default=None, alias="mailingAddress", description="Mailing address")
    business_address: Optional[EntityAddress] = Field(default=None, alias="businessAddress", description="Business address")


class EntitiesListResponse(SecBaseModel):
    """Paginated SEC entities response"""
    data: Optional[List[Entity]] = Field(default=None, description="Entities returned for the current page")
    pagination: Optional[EntitiesPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[EntitiesFilter] = Field(default=None, description="Normalized filters that were applied to the query")


class EntitySic(SecBaseModel):
    """SEC Standard Industrial Classification (SIC) code metadata"""
    sic_code: Optional[str] = Field(default=None, alias="sicCode", description="SIC code")
    office: Optional[str] = Field(default=None, description="SEC office responsible for the industry group")
    industry_title: Optional[str] = Field(default=None, alias="industryTitle", description="Official industry title for the SIC code")
    large_size_tickers: Optional[str] = Field(default=None, alias="largeSizeTickers", description="Comma-separated tickers of large companies in this SIC (when available)")
    sector: Optional[str] = Field(default=None, description="Broad sector grouping")


class EntitySicListResponse(SecBaseModel):
    """Paginated SEC SIC codes for entity filters and reference lookups"""
    data: Optional[List[EntitySic]] = Field(default=None, description="SIC codes returned for the current page")
    pagination: Optional[EntitiesPagination] = Field(default=None, description="Pagination metadata for the current result set")


__all__ = [
    "EntitiesFilter",
    "EntitiesListResponse",
    "EntitiesPagination",
    "Entity",
    "EntityAddress",
    "EntitySic",
    "EntitySicListResponse",
]

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, SecBaseModel):
        _m.model_rebuild()
