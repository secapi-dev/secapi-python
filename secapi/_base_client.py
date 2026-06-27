"""HTTP transport shared by the SEC API client.

Built on :mod:`httpx` so we get connection pooling, timeouts and HTTP/2 for
free. This module keeps all the wire-level concerns (auth headers, query
serialization, retries and error mapping) in one place so the resource classes
stay tiny and readable.
"""

from __future__ import annotations

import datetime
import random
import time
from typing import Any, Dict, List, Mapping, Optional, Type, TypeVar, Union

import httpx

from ._version import __version__
from .auth import auth_headers, resolve_api_key
from .exceptions import APIConnectionError, APITimeoutError, make_status_error
from .models._base import SecBaseModel

ModelT = TypeVar("ModelT", bound=SecBaseModel)

DEFAULT_BASE_URL = "https://api.secapi.dev"
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0)
DEFAULT_MAX_RETRIES = 2
DEFAULT_USER_AGENT = f"secapi-python/{__version__} httpx/{httpx.__version__}"

# Status codes worth retrying (transient) with exponential backoff.
RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


def _serialize_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return str(value)


def build_query(params: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    """Turn a loose params mapping into clean query string values.

    - ``None`` values are dropped.
    - ``date``/``datetime`` become ISO 8601 strings.
    - ``bool`` becomes ``"true"``/``"false"``.
    - lists/tuples become a single comma-joined value (what the API expects).
    """
    out: Dict[str, str] = {}
    if not params:
        return out
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            items = [_serialize_scalar(item) for item in value if item is not None]
            if not items:
                continue
            out[key] = ",".join(items)
        else:
            out[key] = _serialize_scalar(value)
    return out


class BaseSECClient:
    """Shared configuration and HTTP plumbing for the SEC API client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Union[float, httpx.Timeout, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http2: bool = True,
        default_headers: Optional[Mapping[str, str]] = None,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        self.api_key = resolve_api_key(api_key)
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max(0, int(max_retries))

        headers: Dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": DEFAULT_USER_AGENT,
        }
        headers.update(auth_headers(self.api_key))
        if default_headers:
            headers.update(default_headers)

        self._timeout = timeout
        self.session = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
            http2=http2,
            transport=transport,
        )

    # -- lifecycle ---------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self.session.close()

    def __enter__(self) -> "BaseSECClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} base_url={self.base_url!r}>"

    # -- request helpers ---------------------------------------------------

    def _retry_delay(self, attempt: int, response: Optional[httpx.Response]) -> float:
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    return min(float(retry_after), 60.0)
                except ValueError:
                    pass
        # Exponential backoff with jitter: 0.5, 1, 2 ... capped at 8s.
        backoff = min(0.5 * (2 ** attempt), 8.0)
        return backoff + random.uniform(0, 0.25)

    @staticmethod
    def _safe_json(response: httpx.Response) -> Any:
        try:
            return response.json()
        except Exception:
            text = response.text
            return {"raw": text} if text else None

    def _process(
        self,
        response: httpx.Response,
        cast_to: Optional[Type[ModelT]],
        is_list: bool,
    ) -> Any:
        if response.status_code >= 400:
            raise make_status_error(
                response.status_code,
                body=self._safe_json(response),
                request_id=response.headers.get("X-Request-Id"),
            )
        if cast_to is None:
            return self._safe_json(response)
        data = response.json()
        if is_list:
            return [cast_to.model_validate(item) for item in (data or [])]
        return cast_to.model_validate(data)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        cast_to: Optional[Type[ModelT]] = None,
        is_list: bool = False,
    ) -> Any:
        query = build_query(params)
        response: Optional[httpx.Response] = None
        for attempt in range(self.max_retries + 1):
            error: Optional[Exception] = None
            try:
                response = self.session.request(method, path, params=query)
            except httpx.TimeoutException as exc:
                error = APITimeoutError(cause=exc)
            except httpx.TransportError as exc:
                error = APIConnectionError(cause=exc)
            else:
                retryable = response.status_code in RETRY_STATUS_CODES
                if not (retryable and attempt < self.max_retries):
                    return self._process(response, cast_to, is_list)

            if attempt >= self.max_retries:
                if error is not None:
                    raise error
                assert response is not None
                return self._process(response, cast_to, is_list)

            time.sleep(self._retry_delay(attempt, response if error is None else None))

        # Unreachable, but keeps type-checkers happy.
        assert response is not None
        return self._process(response, cast_to, is_list)

    # -- typed convenience wrappers used by resources ----------------------

    def _get_model(self, path: str, params: Optional[Mapping[str, Any]], model: Type[ModelT]) -> ModelT:
        return self._request("GET", path, params=params, cast_to=model)

    def _get_list(self, path: str, params: Optional[Mapping[str, Any]], model: Type[ModelT]) -> List[ModelT]:
        return self._request("GET", path, params=params, cast_to=model, is_list=True)

    def _get_raw(self, path: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)
