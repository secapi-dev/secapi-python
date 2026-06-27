"""Integration tests for financials (live API; needs SECAPI_API_KEY)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_companies_search(live_client):
    result = live_client.financials.companies(ticker="AAPL")
    assert result.issuer
    assert result.issuer.cik


def test_income_statement_by_ticker(live_client):
    statement = live_client.financials.income_statement(ticker="AAPL")
    assert statement.stmt == "IS"
    assert statement.rows is not None


def test_metrics_time_series(live_client):
    result = live_client.financials.metrics("revenue", ticker="AAPL", limit=4)
    assert result.series is not None


def test_ratios(live_client):
    result = live_client.financials.ratios(ticker="AAPL", group="profitability")
    assert result.series is not None


def test_top_metrics(live_client):
    result = live_client.financials.top_metrics("revenue", limit=5)
    assert result.companies is not None
