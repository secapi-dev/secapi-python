"""Shared test fixtures.

Two flavors of tests live here:

* **Unit tests** drive the client through an ``httpx.MockTransport`` so they run
  offline and assert on exactly which URL/params/headers the SDK produced and
  how it parses responses.
* **Integration tests** (marked ``@pytest.mark.integration``) hit the live SEC
  API and are skipped automatically unless ``SECAPI_API_KEY`` is set.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Optional

import httpx
import pytest

from secapi import SECClient


class MockAPI:
    """A recording ``httpx`` handler with simple path-based routing."""

    def __init__(self) -> None:
        self.requests: List[httpx.Request] = []
        self._routes: Dict[str, Dict[str, Any]] = {}
        self._default: Dict[str, Any] = {"status": 200, "json": {}}

    def route(self, path: str, *, status: int = 200, json: Any = None, headers: Optional[dict] = None) -> "MockAPI":
        self._routes[path] = {"status": status, "json": json if json is not None else {}, "headers": headers or {}}
        return self

    def default(self, *, status: int = 200, json: Any = None, headers: Optional[dict] = None) -> "MockAPI":
        self._default = {"status": status, "json": json if json is not None else {}, "headers": headers or {}}
        return self

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        spec = self._routes.get(request.url.path, self._default)
        return httpx.Response(spec["status"], json=spec["json"], headers=spec.get("headers", {}))

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]


@pytest.fixture
def mock_api() -> MockAPI:
    return MockAPI()


@pytest.fixture
def make_client() -> Callable[..., SECClient]:
    """Factory: build a SECClient wired to a MockAPI handler."""

    def _make(handler: Callable[[httpx.Request], httpx.Response], *, api_key: str = "test_api_key", max_retries: int = 0) -> SECClient:
        return SECClient(
            api_key=api_key,
            base_url="https://api.secapi.dev",
            http2=False,
            max_retries=max_retries,
            transport=httpx.MockTransport(handler),
        )

    return _make


@pytest.fixture
def client(make_client, mock_api) -> SECClient:
    return make_client(mock_api)


def _has_live_key() -> bool:
    return bool(os.environ.get("SECAPI_API_KEY") or os.environ.get("SEC_API_KEY"))


@pytest.fixture(scope="session")
def live_client() -> SECClient:
    if not _has_live_key():
        pytest.skip("Set SECAPI_API_KEY to run integration tests against the live API.")
    return SECClient()


def pytest_collection_modifyitems(config, items) -> None:
    if _has_live_key():
        return
    skip = pytest.mark.skip(reason="integration test: set SECAPI_API_KEY to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)
