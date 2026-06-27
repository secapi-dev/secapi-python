"""Offline tests that pin each resource to the exact URL + query it builds.

These guard against camelCase parameter typos in the resource layer.
"""

from __future__ import annotations


def _params(request):
    return dict(request.url.params)


def test_entities_filings(client, mock_api):
    client.entities.filings("AAPL", form="10-K", start_date="2025-01-01", limit=5)
    assert mock_api.last.url.path == "/v1/entities/AAPL/filings"
    assert _params(mock_api.last) == {"formTypes": "10-K", "startDate": "2025-01-01", "page": "1", "limit": "5"}


def test_financials_companies(client, mock_api):
    client.financials.companies(ticker="AAPL")
    assert mock_api.last.url.path == "/v1/financials/companies/search"
    assert _params(mock_api.last) == {"ticker": "AAPL", "limit": "25", "page": "1"}


def test_financials_metrics_joins_symbols(client, mock_api):
    client.financials.metrics(["revenue", "net_income"], ticker="AAPL", qtrs=4)
    assert mock_api.last.url.path == "/v1/financials/metrics"
    params = _params(mock_api.last)
    assert params["symbols"] == "revenue,net_income"
    assert params["ticker"] == "AAPL"
    assert params["source"] == "all"
    assert params["qtrs"] == "4"


def test_financials_balance_sheet_by_accession(client, mock_api):
    client.financials.balance_sheet("0000320193-26-000006")
    assert mock_api.last.url.path == (
        "/v1/financials/filings/0000320193-26-000006/statements/balance-sheet"
    )


def test_insiders_transactions_routing(client, mock_api):
    client.insiders.transactions()
    assert mock_api.last.url.path == "/v1/insiders/transactions"

    client.insiders.transactions(ticker="AAPL", min_value=100000)
    assert mock_api.last.url.path == "/v1/insiders/AAPL/transactions"
    assert _params(mock_api.last)["minValue"] == "100000"

    client.insiders.transactions(person_cik="0001214123")
    assert mock_api.last.url.path == "/v1/insiders/person/0001214123/transactions"


def test_insiders_buying_uses_from_param(client, mock_api):
    client.insiders.buying(limit=10, start="2024-01-01", end="2024-03-31")
    assert mock_api.last.url.path == "/v1/insiders/activity/buying"
    params = _params(mock_api.last)
    assert params["from"] == "2024-01-01"
    assert params["end"] == "2024-03-31"


def test_institutions_holdings(client, mock_api):
    client.institutions.holdings("0001067983", sort="value", limit=10)
    assert mock_api.last.url.path == "/v1/institutions/0001067983/holdings"
    assert _params(mock_api.last) == {"sort": "value", "limit": "10"}


def test_institutions_buys(client, mock_api):
    client.institutions.buys("0001067983", quarter="2024Q3", new_only=True)
    assert mock_api.last.url.path == "/v1/institutions/0001067983/buys"
    params = _params(mock_api.last)
    assert params["quarter"] == "2024Q3"
    assert params["newOnly"] == "true"


def test_search_is_alias_for_transactions(client, mock_api):
    client.insiders.search(ticker="AAPL")
    assert mock_api.last.url.path == "/v1/insiders/AAPL/transactions"
