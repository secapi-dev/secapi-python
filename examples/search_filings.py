"""Search SEC filings and list a company's filing documents.

Run with::

    export SECAPI_API_KEY="YOUR_API_KEY"
    python examples/search_filings.py
"""

from __future__ import annotations

from secapi import SECClient


def main() -> None:
    client = SECClient()  # reads SECAPI_API_KEY from the environment

    print("Latest Apple 10-K / 8-K filings")
    print("-" * 60)
    filings = client.filings.search(ticker="AAPL", form=["10-K", "8-K"], limit=5)
    for filing in filings.data or []:
        print(f"{filing.filing_date}  {filing.form_type:<6}  {filing.accession_number}")

    if filings.data:
        latest = filings.data[0]
        print(f"\nDocuments in {latest.accession_number}")
        print("-" * 60)
        documents = client.filings.documents(latest.cik, latest.accession_number)
        for doc in documents[:10]:
            print(f"{(doc.document_type or '?'):<12}  {doc.filename}")


if __name__ == "__main__":
    main()
