"""
tracker.py — Phase 3, step 2: poll the watchlist, store filings in SQLite,
and report any NEW filings since the last run.

First run for a company = baseline (record what's there now, no alerts).
Later runs = only genuinely new filings are reported as events.
"""

import os
import csv
import sys
import sqlite3
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CH_API_KEY")
if not API_KEY:
    sys.exit("No CH_API_KEY found. Check your .env file.")

BASE_URL = "https://api.company-information.service.gov.uk"
DB_FILE = "data/signals.db"


def ch_get(path):
    response = requests.get(f"{BASE_URL}{path}", auth=(API_KEY, ""), timeout=15)
    response.raise_for_status()
    return response.json()


def read_watchlist(filename="watchlist.csv"):
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def setup_database():
    """Create the database file and tables if they don't already exist."""
    os.makedirs("data", exist_ok=True)   # make the data/ folder if missing
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_number TEXT PRIMARY KEY,
            company_name   TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS filings (
            transaction_id TEXT PRIMARY KEY,
            company_number TEXT,
            date           TEXT,
            type           TEXT,
            category       TEXT,
            description    TEXT,
            first_seen     TEXT
        )
    """)
    conn.commit()
    return conn


def process_company(conn, company):
    number = company["company_number"].strip()
    name = company["company_name"].strip()

    # Remember the company itself
    conn.execute(
        "INSERT OR REPLACE INTO companies (company_number, company_name) VALUES (?, ?)",
        (number, name),
    )

    # Have we seen this company before?
    already_stored = conn.execute(
        "SELECT COUNT(*) FROM filings WHERE company_number = ?", (number,)
    ).fetchone()[0]

    # Fetch the most recent filings (a page of up to 100)
    data = ch_get(f"/company/{number}/filing-history?items_per_page=100")
    filings = data.get("items", [])

    new_filings = []
    now = datetime.now(timezone.utc).isoformat()
    for f in filings:
        tid = f.get("transaction_id")
        if tid is None:
            continue
        seen = conn.execute(
            "SELECT 1 FROM filings WHERE transaction_id = ?", (tid,)
        ).fetchone()
        if seen is None:                      # not in the database = new to us
            conn.execute(
                """INSERT INTO filings
                   (transaction_id, company_number, date, type, category, description, first_seen)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (tid, number, f.get("date"), f.get("type"),
                 f.get("category"), f.get("description"), now),
            )
            new_filings.append(f)

    conn.commit()

    # Report
    if already_stored == 0:
        print(f"{name} ({number}) — baseline recorded: {len(new_filings)} filings")
    elif new_filings:
        print(f"{name} ({number}) — {len(new_filings)} NEW filing(s):")
        for f in new_filings:
            print(f"    {f.get('date')}  {f.get('type')}  {f.get('description')}")
    else:
        print(f"{name} ({number}) — no new filings")


def main():
    conn = setup_database()
    watchlist = read_watchlist()
    print(f"Polling {len(watchlist)} companies...\n")
    for company in watchlist:
        process_company(conn, company)
    conn.close()


if __name__ == "__main__":
    main()