"""Integration tests for filings (live API; needs SECAPI_API_KEY)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_search_filings(live_client):
    result = live_client.filings.search(ticker="AAPL", form="10-K", limit=3)
    assert result.data
    for filing in result.data:
        assert filing.accession_number
        assert (filing.form_type or "").startswith("10-K")


def test_form_types(live_client):
    result = live_client.filings.form_types(limit=5)
    assert result.data
    assert result.data[0].form_name


def test_get_and_documents(live_client):
    search = live_client.filings.search(ticker="AAPL", form="10-K", limit=1)
    sample = search.data[0]

    by_accession = live_client.filings.get(sample.accession_number)
    assert isinstance(by_accession, list)
    assert by_accession

    documents = live_client.filings.documents(sample.cik, sample.accession_number)
    assert isinstance(documents, list)
