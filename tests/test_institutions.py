"""Integration tests for institutions (live API; needs SECAPI_API_KEY)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration

# Berkshire Hathaway's 13F filer CIK, used as a stable example.
BERKSHIRE_CIK = "0001067983"


def test_list_institutions(live_client):
    result = live_client.institutions.list(q="Berkshire", limit=5)
    assert result.data is not None


def test_holdings(live_client):
    result = live_client.institutions.holdings(BERKSHIRE_CIK, limit=10, sort="value")
    assert result.cik
    assert result.holdings is not None


def test_market_activity(live_client):
    result = live_client.institutions.activity(limit=5)
    assert result is not None
