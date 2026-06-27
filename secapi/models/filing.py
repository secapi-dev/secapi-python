"""Auto-generated SEC API models. Do not edit by hand.

Regenerate with: python scripts/generate_models.py
"""

from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import Field

from ._base import SecBaseModel


class FilingContext(SecBaseModel):
    """SEC submission header context for the statement"""
    adsh: Optional[str] = Field(default=None, description="EDGAR accession number (ADSH)")
    cik: Optional[int] = Field(default=None, description="Central Index Key")
    entity_name: Optional[str] = Field(default=None, alias="entityName", description="Legal entity name")
    ticker: Optional[str] = Field(default=None, description="Trading symbol when present on the submission row")
    form: Optional[str] = Field(default=None, description="SEC form type")
    fiscal_year: Optional[int] = Field(default=None, alias="fiscalYear", description="Fiscal year on the submission")
    fiscal_period: Optional[str] = Field(default=None, alias="fiscalPeriod", description="Fiscal period on the submission (FY, Q1–Q4)")
    period: Optional[int] = Field(default=None, description="Balance sheet / document period end (SEC period, YYYYMMDD)")
    filed: Optional[int] = Field(default=None, description="SEC filing date (YYYYMMDD)")
    accepted: Optional[datetime.datetime] = Field(default=None, description="SEC acceptance datetime")


class Filing(SecBaseModel):
    """Summary view of an SEC filing"""
    accession_number: Optional[str] = Field(default=None, alias="accessionNumber", description="SEC accession number")
    cik: Optional[str] = Field(default=None, description="Central Index Key of the filing entity")
    form_type: Optional[str] = Field(default=None, alias="formType", description="SEC form type")
    form_type_category: Optional[str] = Field(default=None, alias="formTypeCategory", description="Normalized category of the SEC form type")
    ticker: Optional[str] = Field(default=None, description="Ticker symbol when available")
    filing_date: Optional[datetime.date] = Field(default=None, alias="filingDate", description="Filing date")
    filing_url: Optional[str] = Field(default=None, alias="filingUrl", description="Public SEC URL for the filing")
    accepted_date: Optional[datetime.datetime] = Field(default=None, alias="acceptedDate", description="Timestamp when the SEC accepted the filing")
    entity_name: Optional[str] = Field(default=None, alias="entityName", description="Display name of the filing entity")


class FilingDocument(SecBaseModel):
    """Document that belongs to an SEC filing"""
    document_type: Optional[str] = Field(default=None, alias="documentType", description="SEC document type")
    filename: Optional[str] = Field(default=None, description="Filename published by the SEC")
    url: Optional[str] = Field(default=None, description="Direct public URL to the filing document")
    description: Optional[str] = Field(default=None, description="Human-readable document description")


class FilingFormType(SecBaseModel):
    """SEC form type metadata for filings filters"""
    form_name: Optional[str] = Field(default=None, alias="formName", description="SEC form type name")
    category: Optional[str] = Field(default=None, description="Normalized category of the form type")
    description: Optional[str] = Field(default=None, description="Human-readable description of the form type")


class FilingsPagination(SecBaseModel):
    """Pagination metadata for filings results"""
    page: Optional[int] = Field(default=None, description="Current 1-based page number")
    limit: Optional[int] = Field(default=None, description="Maximum number of records requested per page")
    has_more_data: Optional[bool] = Field(default=None, alias="hasMoreData", description="Whether another page of results is available")


class FilingFormTypesListResponse(SecBaseModel):
    """Paginated active SEC form types for filings filters"""
    data: Optional[List[FilingFormType]] = Field(default=None, description="Form types returned for the current page")
    pagination: Optional[FilingsPagination] = Field(default=None, description="Pagination metadata for the current result set")


class FilingsFilter(SecBaseModel):
    """Normalized filters applied to the filings query"""
    form_types: Optional[List[str]] = Field(default=None, alias="formTypes", description="List of requested SEC form types")
    cik: Optional[str] = Field(default=None, description="Normalized company CIK filter")
    ticker: Optional[str] = Field(default=None, description="Normalized uppercase ticker filter")
    start_date: Optional[datetime.date] = Field(default=None, alias="startDate", description="Start of the filing date range")
    end_date: Optional[datetime.date] = Field(default=None, alias="endDate", description="End of the filing date range")


class FilingsListResponse(SecBaseModel):
    """Paginated filings response"""
    data: Optional[List[Filing]] = Field(default=None, description="Filings returned for the current page")
    pagination: Optional[FilingsPagination] = Field(default=None, description="Pagination metadata for the current result set")
    filters: Optional[FilingsFilter] = Field(default=None, description="Normalized filters that were applied to the query")


__all__ = [
    "Filing",
    "FilingContext",
    "FilingDocument",
    "FilingFormType",
    "FilingFormTypesListResponse",
    "FilingsFilter",
    "FilingsListResponse",
    "FilingsPagination",
]

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, SecBaseModel):
        _m.model_rebuild()
