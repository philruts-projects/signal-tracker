"""
fetch_filings.py — Phase 3, step 1: read the watchlist and fetch each
company's filing history from Companies House.

No database yet — this step just proves we can pull filings for every
company on the watchlist and see the latest one.
"""

import os
import csv
import sys

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CH_API_KEY")
if not API_KEY:
    sys.exit("No CH_API_KEY found. Check your .env file.")

BASE_URL = "https://api.company-information.service.gov.uk"


def ch_get(path):
    """Make an authenticated GET request to Companies House and return the
    parsed JSON. `path` is everything after the base URL."""
    response = requests.get(f"{BASE_URL}{path}", auth=(API_KEY, ""), timeout=15)
    response.raise_for_status()   # turn a bad status code into a clear error
    return response.json()


def read_watchlist(filename="watchlist.csv"):
    """Read the watchlist CSV into a list of {company_number, company_name} rows."""
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    watchlist = read_watchlist()
    print(f"Watching {len(watchlist)} companies.\n")

    for company in watchlist:
        number = company["company_number"].strip()
        name = company["company_name"].strip()

        data = ch_get(f"/company/{number}/filing-history")
        filings = data.get("items", [])
        total = data.get("total_count", len(filings))

        print(f"{name} ({number}) — {total} filings on record")
        if filings:
            latest = filings[0]   # Companies House returns newest first
            print(f"    Latest: {latest.get('date')}  "
                  f"{latest.get('type')}  {latest.get('description')}")
        print()


if __name__ == "__main__":
    main()