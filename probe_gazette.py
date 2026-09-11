"""
probe_gazette.py — does The Gazette warn earlier than Companies House?

Same idea as probe_charges.py / probe_officers.py / probe_fca.py: call the endpoint,
print what comes back, decide with our own eyes whether it's worth storing. The actual
fetch lives in gazette.py, shared with tracker.py — this script is now just the
"look at it and compare dates" harness.

Run it:
  python probe_gazette.py            # every company in watchlist.csv
  python probe_gazette.py 03782379   # one company

Read-only. Makes no Companies House or Claude calls. If data/signals.db exists it reads
(never writes) the earliest insolvency filing per company so you can compare dates.
"""

import csv
import sqlite3
import sys
import time
from datetime import date
from pathlib import Path

import requests

from gazette import fetch_notices

DB = Path("data/signals.db")


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
            notices = fetch_notices(number)
        except requests.RequestException as e:
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
