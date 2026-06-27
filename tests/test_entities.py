"""Integration tests for entities (live API; needs SECAPI_API_KEY)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_get_entity_by_ticker(live_client):
    entity = live_client.entities.get("AAPL")
    assert entity.cik
    assert (entity.ticker or "").upper() == "AAPL" or entity.name


def test_list_entities(live_client):
    result = live_client.entities.list(ticker="AAPL", limit=1)
    assert result.data
    assert result.pagination.limit == 1


def test_list_sic_codes(live_client):
    result = live_client.entities.sic_codes(limit=5)
    assert result.data
    assert result.data[0].sic_code


def test_entity_filings(live_client):
    result = live_client.entities.filings("AAPL", form="10-K", limit=2)
    assert result.data
    for filing in result.data:
        assert filing.accession_number
