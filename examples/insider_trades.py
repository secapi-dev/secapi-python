"""Explore insider (Form 4) trading activity.

Run with::

    export SECAPI_API_KEY="fs_live_..."
    python examples/insider_trades.py
"""

from __future__ import annotations

from secapi import SECClient


def main() -> None:
    client = SECClient()

    print("Most recent insider transactions for AAPL")
    print("-" * 72)
    response = client.insiders.transactions(ticker="AAPL", limit=10)
    for tx in response.transactions or []:
        reporter = tx.reporter.name if tx.reporter else "?"
        side = tx.acquired_disposed or "?"
        print(
            f"{tx.transaction_date}  {side}  {(tx.transaction_code or ''):<3} "
            f"{(tx.shares or 0):>12,.0f} sh  @ {tx.price_per_share or 0:>8}  {reporter}"
        )

    print("\nBuy vs sell ratio (lifetime)")
    print("-" * 72)
    ratio = client.insiders.buy_sell_ratio("AAPL")
    print(f"buys={ratio.buy_transaction_count}  sells={ratio.sell_transaction_count}  ratio={ratio.buy_sell_ratio}")

    print("\nToday's top insider buyers (market-wide)")
    print("-" * 72)
    leaders = client.insiders.top_buyers(limit=5)
    for leader in leaders.data or []:
        issuer = leader.issuer.ticker if leader.issuer else "?"
        print(f"#{leader.rank}  {issuer:<8}  net ${leader.net_value or 0:,.0f}")


if __name__ == "__main__":
    main()
