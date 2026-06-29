"""Offline unit tests for the transport: auth, query building, errors, retries."""

from __future__ import annotations

import datetime

import httpx
import pytest

import secapi._base_client as base_client
from secapi import SECClient
from secapi.auth import MissingAPIKeyError
from secapi.exceptions import (
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)


def test_api_key_required_without_env(monkeypatch):
    monkeypatch.delenv("SECAPI_API_KEY", raising=False)
    monkeypatch.delenv("SEC_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyError):
        SECClient()


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("SECAPI_API_KEY", "abcd1234_from_env")
    client = SECClient(http2=False)
    assert client.api_key == "abcd1234_from_env"
    client.close()


def test_auth_header_sent(client, mock_api):
    client.entities.list()
    assert mock_api.last.headers["x-api-key"] == "test_api_key"
    assert mock_api.last.url.path == "/v1/entities"


def test_query_serialization(client, mock_api):
    client.filings.search(
        ticker="AAPL",
        form=["10-K", "8-K"],
        start_date=datetime.date(2025, 1, 1),
        cik=None,  # should be dropped
        page=2,
    )
    params = mock_api.last.url.params
    assert params["ticker"] == "AAPL"
    assert params["formTypes"] == "10-K,8-K"  # list joined with commas
    assert params["startDate"] == "2025-01-01"  # date -> ISO
    assert params["page"] == "2"
    assert "cik" not in params  # None dropped


def test_bool_serialization(client, mock_api):
    client.insiders.owners("AAPL", include_derivative=True, include_non_derivative=False)
    params = mock_api.last.url.params
    assert params["includeDerivative"] == "true"
    assert params["includeNonDerivative"] == "false"


def test_path_building_with_ids(client, mock_api):
    client.filings.documents("0001065280", "0001065280-25-000033")
    assert mock_api.last.url.path == "/v1/filings/0001065280/0001065280-25-000033/documents"


@pytest.mark.parametrize(
    "status,exc",
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, ServerError),
        (503, ServerError),
    ],
)
def test_error_mapping(make_client, status, exc):
    body = {"error": {"code": "x", "message": "boom", "details": {"reason": "y"}, "request_id": "req-123"}}

    def handler(request):
        return httpx.Response(status, json=body)

    client = make_client(handler)
    with pytest.raises(exc) as info:
        client.entities.get("AAPL")
    err = info.value
    assert err.status_code == status
    assert err.message == "boom"
    assert err.request_id == "req-123"
    assert err.details == {"reason": "y"}


def test_validation_error_is_bad_request():
    assert ValidationError is BadRequestError


def test_retry_then_success(make_client, monkeypatch):
    monkeypatch.setattr(base_client.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503, json={"error": {"message": "transient"}})
        return httpx.Response(200, json={"data": [], "pagination": {"page": 1, "limit": 20, "hasMoreData": False}})

    client = make_client(handler, max_retries=2)
    result = client.entities.list()
    assert calls["n"] == 3  # 1 try + 2 retries
    assert result.pagination.has_more_data is False


def test_retry_exhausted_raises(make_client, monkeypatch):
    monkeypatch.setattr(base_client.time, "sleep", lambda *_: None)

    def handler(request):
        return httpx.Response(500, json={"error": {"message": "down"}})

    client = make_client(handler, max_retries=1)
    with pytest.raises(ServerError):
        client.entities.list()


def test_context_manager_closes(make_client):
    def handler(request):
        return httpx.Response(200, json={})

    with make_client(handler) as client:
        assert isinstance(client.session, httpx.Client)
    assert client.session.is_closed
