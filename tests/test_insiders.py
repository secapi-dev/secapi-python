"""Integration tests for insiders (live API; needs SECAPI_API_KEY)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_latest_transactions(live_client):
    result = live_client.insiders.latest(limit=5)
    assert result.transactions is not None


def test_transactions_by_ticker(live_client):
    result = live_client.insiders.transactions(ticker="AAPL", limit=5)
    assert result.transactions is not None


def test_buy_sell_ratio(live_client):
    result = live_client.insiders.buy_sell_ratio("AAPL")
    assert result.issuer


def test_statistics(live_client):
    result = live_client.insiders.statistics()
    assert result.transaction_count is not None
