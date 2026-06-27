# secapi - Python SDK for the SEC API

The official Python client for [**secapi.dev**](https://secapi.dev) - SEC filings,
financial statements, standardized metrics & ratios, insider transactions, and
13F institutional holdings, all from one clean, typed client.

```python
from secapi import SECClient

client = SECClient(api_key="YOUR_API_KEY")

results = client.filings.search(ticker="AAPL", form="10-K")
print(results)
```

- **Pleasant, resource-oriented API** - `client.filings.search(...)`, `client.financials.income_statement(...)`. No URLs to build.
- **Typed responses** - real objects with autocomplete (`filing.accession_number`, `filing.filing_date`), powered by Pydantic v2. No dictionary spelunking.
- **Helpful errors** - `AuthenticationError`, `RateLimitError`, `NotFoundError`, `ValidationError`, `ServerError` instead of raw HTTP codes.
- **Fast & robust** - built on [httpx](https://www.python-httpx.org/) with HTTP/2, connection pooling, timeouts, and automatic retries with backoff.
- **Stays in sync with the API** - models are generated from the API's OpenAPI spec.

---

## Installation

```bash
pip install secapi
```

Requires Python 3.8+.

## Authentication

Get an API key from [secapi.dev](https://secapi.dev). Keys look like `fs_live_...`
(or `fs_test_...` for test mode). Provide it explicitly:

```python
client = SECClient(api_key="fs_live_...")
```

...or set an environment variable and omit the argument:

```bash
export SECAPI_API_KEY="fs_live_..."
```

```python
client = SECClient()  # reads SECAPI_API_KEY
```

## Quickstart

```python
from secapi import SECClient

client = SECClient(api_key="YOUR_API_KEY")

# Find Apple's annual reports
filings = client.filings.search(ticker="AAPL", form="10-K", limit=5)
for filing in filings.data:
    print(filing.filing_date, filing.form_type, filing.accession_number)

# Pull the latest income statement for Microsoft
income = client.financials.income_statement(ticker="MSFT")
for row in income.rows or []:
    print(row.plabel)
```

## Resources

Every top-level API category is its own namespace on the client.

### `client.filings`

```python
client.filings.search(ticker="AAPL", form=["10-K", "8-K"], start_date="2025-01-01")
client.filings.get("0000320193-26-000006")               # every filing for an accession no.
client.filings.retrieve("0000320193", "0000320193-26-000006")
client.filings.documents("0000320193", "0000320193-26-000006")
client.filings.form_types()
```

### `client.financials`

```python
# As-reported statements - by accession number, or by ticker/CIK (latest filing)
client.financials.income_statement(ticker="MSFT")
client.financials.balance_sheet("0000320193-26-000006")
client.financials.cash_flow(ticker="AAPL", form="10-K")

# Standardized statements, raw XBRL, company & concept search
client.financials.income_statement_standardized(ticker="AAPL")
client.financials.xbrl("0000320193-26-000006")
client.financials.companies(ticker="AAPL")
client.financials.concepts("revenue")

# Cross-period metrics, ratios and rankings
client.financials.metrics(["revenue", "net_income"], ticker="AAPL")
client.financials.ratios(ticker="AAPL", group="profitability")
client.financials.top_metrics("revenue", limit=10)
client.financials.top_ratios("gross_margin")

# Revenue segments
client.financials.segments_geography("AAPL")
client.financials.segments_product_service("AAPL", period="2024")
```

### `client.entities`

```python
client.entities.get("AAPL")              # by ticker or CIK
client.entities.list(q="Apple", limit=20)
client.entities.filings("AAPL", form="10-K")
client.entities.sic_codes()
```

### `client.insiders`

```python
client.insiders.latest(limit=50)                       # newest insider trades
client.insiders.search(ticker="AAPL", acquired_disposed="A")
client.insiders.transactions(person_cik="0001214123")  # one insider
client.insiders.buying(limit=25)
client.insiders.top_buyers()
client.insiders.owners("AAPL")
client.insiders.buy_sell_ratio("AAPL")
client.insiders.person("0001214123")
```

### `client.institutions`

```python
client.institutions.list(q="Berkshire")
client.institutions.holdings("0001067983", sort="value")
client.institutions.buys("0001067983", quarter="2024Q3")
client.institutions.sectors("0001067983")
client.institutions.activity()                          # market-wide smart money
```

## Typed responses

Responses are Pydantic models, so you get attribute access and editor
autocomplete instead of raw dictionaries:

```python
filings = client.filings.search(ticker="AAPL", form="10-K")

first = filings.data[0]
first.company_name      # -> entity_name on the model
first.accession_number  # "0000320193-26-000006"
first.filing_date       # datetime.date(2026, 1, 15)
filings.pagination.has_more_data  # True / False
```

Need a plain dict? Every model has `.to_dict()` (snake_case) and
`.to_dict(by_alias=True)` (the original API keys). Unknown fields the API adds in
the future are preserved automatically, so your code keeps working.

## Error handling

```python
from secapi import SECClient
from secapi.exceptions import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
    SecApiError,
)

client = SECClient(api_key="...")
try:
    client.entities.get("AAPL")
except RateLimitError as exc:
    print("Slow down:", exc.message)
except AuthenticationError:
    print("Check your API key")
except NotFoundError:
    print("No such entity")
except SecApiError as exc:        # base class for everything this SDK raises
    print("Request failed:", exc)
```

Every `APIStatusError` exposes `.status_code`, `.code`, `.message`, `.details`,
and `.request_id` (handy when contacting support).

## Configuration

```python
import httpx
from secapi import SECClient

client = SECClient(
    api_key="...",
    timeout=httpx.Timeout(30.0, connect=10.0),  # or a float
    max_retries=2,         # retries 429/5xx with exponential backoff
    http2=True,            # enabled by default
    base_url="https://api.secapi.dev",
)

# Reuse the client across requests; close it (or use a context manager) when done.
with SECClient(api_key="...") as client:
    client.filings.search(ticker="AAPL")
```

Internals you can reach for if you need them: `client.session` (the underlying
`httpx.Client`), `client.base_url`, and `client.api_key`.

## Development

The response models are generated from the API's OpenAPI document
(`https://api.secapi.dev/api/core/v3/api-docs`), vendored at
`scripts/openapi.json`.

```bash
pip install -e ".[dev]"

# Regenerate models from the spec
python scripts/generate_models.py

# Fail if the committed models drift from the spec (run this in CI)
python scripts/generate_models.py --check

# Unit tests (offline, mocked transport)
pytest

# Integration tests against the live API
export SECAPI_API_KEY="fs_live_..."
pytest -m integration
```

## License

MIT - see [LICENSE](LICENSE).
