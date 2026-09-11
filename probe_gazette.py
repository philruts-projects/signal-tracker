"""
probe_gazette.py — does The Gazette warn earlier than Companies House?

Same idea as probe_charges.py / probe_officers.py / probe_fca.py: call the endpoint once,
print what comes back, decide with our own eyes whether it's worth storing.

The Gazette is the UK's official public record. Insolvency practitioners must publish
notices there (administrator appointed, winding-up petition, etc), often before the
matching form reaches Companies House. Category 24 = "Corporate Insolvency".

No key, no registration: the notice feed is open data. Every notice quotes the company
number in its text, so we search on the number, not the name (see BACKLOG.md: always key
on number).

Run it:
  python probe_gazette.py            # every company in watchlist.csv
  python probe_gazette.py 03782379   # one company

Read-only. Makes no Companies House or Claude calls. If data/signals.db exists it reads
(never writes) the earliest insolvency filing per company so you can compare dates.

Lessons learned getting this to run (all real, all in one afternoon):
  - the Gazette answers the default "python-requests" User-Agent with HTTP 403
  - adding an "Accept: application/json" header alongside data.json gives HTTP 500
  - some queries take well over 20 seconds; it's a free service with no SLA
"""

import csv
import sqlite3
import sys
import time
from datetime import date
from pathlib import Path

import requests

BASE = "https://www.thegazette.co.uk/all-notices/notice/data.json"
CORPORATE_INSOLVENCY = "24"
DB = Path("data/signals.db")

# Identify ourselves the way a browser would. Companies House never cared; this one does.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    ),
}
TIMEOUT_SECONDS = 60


def gazette_notices(company_number):
    """All corporate-insolvency notices mentioning this company number, oldest first."""
    params = {
        "text": company_number,
        "categorycode": CORPORATE_INSOLVENCY,
        "sort-by": "oldest-date",
        "results-page-size": 50,
    }
    response = requests.get(BASE, params=params, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    print(f"GET {response.url}  ->  HTTP {response.status_code}")
    response.raise_for_status()
    payload = response.json()
    # The feed is Atom XML re-expressed as JSON, so field names carry their "f:" prefix
    # and a single result still arrives as a one-item list. No matches = no "entry" key.
    return payload.get("entry") or []


def first_ch_insolvency_filing(company_number):
    """Earliest Companies House filing in the 'insolvency' category, from our local DB."""
    if not DB.exists():
        return None
    conn = sqlite3.connect(DB)
    row = conn.execute(
        "SELECT MIN(date), description FROM filings "
        "WHERE company_number = ? AND category = 'insolvency'",
        (company_number,),
    ).fetchone()
    conn.close()
    return row if row and row[0] else None


def main():
    if len(sys.argv) > 1:
        numbers = [sys.argv[1]]
    else:
        with open("watchlist.csv", newline="") as f:
            numbers = [r["company_number"] for r in csv.DictReader(f)]

    for number in numbers:
        print(f"\n=============== {number} ===============")
        try:
            notices = gazette_notices(number)
        except requests.RequestException as e:
            # Same lesson as the tracker's Unknown state: a failed fetch is "don't know",
            # not "no notices". Say so and move on to the next company.
            print(f"Gazette: request failed ({type(e).__name__}) - skipped, NOT clean.")
            continue

        if not notices:
            print("Gazette: no corporate-insolvency notices.")
            continue

        for n in notices:
            published = n["published"][:10]
            kind = (n.get("category") or {}).get("@term", "?")
            print(f"  {published}  [{n.get('f:notice-code')}] {kind:<40} {n.get('title')}")
            print(f"              {n['link'][1]['@href']}")

        ch = first_ch_insolvency_filing(number)
        if ch:
            gazette_first = date.fromisoformat(notices[0]["published"][:10])
            ch_first = date.fromisoformat(ch[0])
            lead = (ch_first - gazette_first).days
            print(f"  Companies House first insolvency filing: {ch_first}  ({ch[1]})")
            print(f"  >>> Gazette lead over Companies House: {lead} days")
        time.sleep(0.5)  # be polite to a free service


if __name__ == "__main__":
    main()
