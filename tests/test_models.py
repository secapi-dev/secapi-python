"""Offline tests for response parsing and the ticker->accession convenience."""

from __future__ import annotations

import datetime

import httpx

from secapi.models import Entity, Filing, FilingsListResponse


def test_filing_model_parses_camelcase_to_snake():
    filing = Filing.model_validate(
        {
            "accessionNumber": "0000320193-26-000006",
            "cik": "0000320193",
            "formType": "10-K",
            "ticker": "AAPL",
            "filingDate": "2026-01-15",
            "acceptedDate": "2026-01-15T18:01:02",
            "entityName": "Apple Inc.",
        }
    )
    assert filing.accession_number == "0000320193-26-000006"
    assert filing.form_type == "10-K"
    assert filing.entity_name == "Apple Inc."
    assert filing.filing_date == datetime.date(2026, 1, 15)
    assert isinstance(filing.accepted_date, datetime.datetime)


def test_unknown_fields_preserved():
    entity = Entity.model_validate({"name": "Apple", "ticker": "AAPL", "brandNewField": 42})
    assert entity.ticker == "AAPL"
    # extra="allow" keeps forward-compatible fields (under their API key) so the
    # SDK keeps working when the API adds new fields before we model them.
    assert entity.brandNewField == 42
    assert entity.model_extra["brandNewField"] == 42


def test_to_dict_round_trips_aliases():
    filing = Filing.model_validate({"accessionNumber": "x", "formType": "10-K"})
    assert filing.to_dict() == {"accession_number": "x", "form_type": "10-K"}
    assert filing.to_dict(by_alias=True) == {"accessionNumber": "x", "formType": "10-K"}


def test_list_response_parses_nested(client, mock_api):
    mock_api.route(
        "/v1/filings",
        json={
            "data": [
                {"accessionNumber": "a-1", "ticker": "AAPL", "formType": "10-K", "filingDate": "2026-01-15"},
                {"accessionNumber": "a-2", "ticker": "AAPL", "formType": "8-K", "filingDate": "2026-02-01"},
            ],
            "pagination": {"page": 1, "limit": 20, "hasMoreData": True},
            "filters": {"ticker": "AAPL", "formTypes": ["10-K", "8-K"]},
        },
    )
    result = client.filings.search(ticker="AAPL")
    assert isinstance(result, FilingsListResponse)
    assert len(result.data) == 2
    assert result.data[0].accession_number == "a-1"
    assert result.pagination.has_more_data is True
    assert result.filters.form_types == ["10-K", "8-K"]


def test_get_returns_list_of_models(client, mock_api):
    mock_api.route(
        "/v1/filings/0000320193-26-000006",
        json=[{"accessionNumber": "0000320193-26-000006", "formType": "10-K"}],
    )
    filings = client.filings.get("0000320193-26-000006")
    assert isinstance(filings, list)
    assert filings[0].form_type == "10-K"


def test_income_statement_resolves_latest_filing_by_ticker(make_client):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/v1/financials/companies/search":
            assert request.url.params["ticker"] == "MSFT"
            return httpx.Response(
                200,
                json={
                    "issuer": {"ticker": "MSFT", "cik": "0000789019"},
                    "filings": [
                        {"accessionNumber": "old-filing", "form": "10-K", "filed": "2020-01-01"},
                        {"accessionNumber": "newest-filing", "form": "10-K", "filed": "2026-01-15"},
                    ],
                },
            )
        captured["statement_path"] = path
        return httpx.Response(200, json={"stmt": "IS", "rows": []})

    client = make_client(handler)
    client.financials.income_statement(ticker="MSFT")
    # It should pick the most recently filed accession number.
    assert captured["statement_path"] == (
        "/v1/financials/filings/newest-filing/statements/income-statement"
    )
