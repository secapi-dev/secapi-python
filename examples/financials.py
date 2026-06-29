"""Pull financial statements, metrics and ratios.

Run with::

    export SECAPI_API_KEY="YOUR_API_KEY"
    python examples/financials.py
"""

from __future__ import annotations

from secapi import SECClient


def main() -> None:
    client = SECClient()

    print("Microsoft - latest as-reported income statement")
    print("-" * 60)
    income = client.financials.income_statement(ticker="MSFT")
    if income.filing:
        print(f"Filing: {income.filing.form} {income.filing.fiscal_year} ({income.filing.adsh})")
    for row in (income.rows or [])[:12]:
        ctx = row.value_context
        value = ctx.value if ctx else None
        print(f"  {(row.plabel or row.tag or ''):<45} {value}")

    print("\nApple - revenue & net income time series")
    print("-" * 60)
    series = client.financials.metrics(["revenue", "net_income"], ticker="AAPL", limit=4)
    for metric in series.series or []:
        print(f"\n{metric.label or metric.symbol}:")
        for point in metric.points or []:
            print(f"  {point.fiscal_year} {point.fiscal_period}: {point.value:,.0f} {point.unit or ''}")

    print("\nApple - profitability ratios")
    print("-" * 60)
    ratios = client.financials.ratios(ticker="AAPL", group="profitability", limit=1)
    for ratio in ratios.series or []:
        latest = (ratio.points or [None])[0]
        if latest:
            print(f"  {ratio.label or ratio.ratio:<30} {latest.value}")


if __name__ == "__main__":
    main()
