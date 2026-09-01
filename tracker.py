"""
tracker.py — Phase 4: poll the watchlist, store filings in SQLite, detect NEW
filings, and generate a plain-English Claude briefing for each new one.

Safety: at most MAX_BRIEFINGS_PER_RUN briefings are generated per run, so a
surge of new filings can never run up a surprise API bill.
"""

import os
import csv
import sys
import json
import sqlite3
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from briefing import generate_briefing
from severity import rule_severity
from officers import compute_churn

load_dotenv()
API_KEY = os.getenv("CH_API_KEY")
if not API_KEY:
    sys.exit("No CH_API_KEY found. Check your .env file.")

BASE_URL = "https://api.company-information.service.gov.uk"
DB_FILE = "data/signals.db"
MAX_BRIEFINGS_PER_RUN = 5     # hard cap on Claude calls per run


def ch_get(path):
    response = requests.get(f"{BASE_URL}{path}", auth=(API_KEY, ""), timeout=15)
    response.raise_for_status()
    return response.json()


def read_watchlist(filename="watchlist.csv"):
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def setup_database():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_number         TEXT PRIMARY KEY,
            company_name           TEXT,
            status                 TEXT,
            status_detail          TEXT,
            has_insolvency_history INTEGER,
            has_charges            INTEGER,
            accounts_overdue       INTEGER,
            peak_churn             INTEGER,
            peak_churn_date        TEXT,
            recent_churn           INTEGER,
            short_tenure_exits     INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS filings (
            transaction_id     TEXT PRIMARY KEY,
            company_number     TEXT,
            date               TEXT,
            type               TEXT,
            category           TEXT,
            description        TEXT,
            description_values TEXT,
            severity           TEXT,
            first_seen         TEXT,
            briefing           TEXT
        )
    """)
    conn.commit()
    return conn


def process_company(conn, company):
    """Fetch a company's filings, store any new ones, return the new filings."""
    number = company["company_number"].strip()
    name = company["company_name"].strip()

    # Pull the company profile for its registered status — the strongest single signal.
    try:
        profile = ch_get(f"/company/{number}")
    except Exception:
        profile = {}
    status = profile.get("company_status")
    status_detail = profile.get("company_status_detail")
    has_insolvency = 1 if profile.get("has_insolvency_history") else 0
    has_charges = 1 if profile.get("has_charges") else 0
    accounts_overdue = 1 if (profile.get("accounts") or {}).get("overdue") else 0

    # Board churn and tenure from the officers list.
    try:
        officers = ch_get(f"/company/{number}/officers?items_per_page=100").get("items", [])
        churn = compute_churn(officers)
    except Exception:
        churn = {"peak_churn": 0, "peak_churn_date": None, "recent_churn": 0, "short_tenure_exits": 0}

    conn.execute(
        """INSERT OR REPLACE INTO companies
           (company_number, company_name, status, status_detail,
            has_insolvency_history, has_charges, accounts_overdue,
            peak_churn, peak_churn_date, recent_churn, short_tenure_exits)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (number, name, status, status_detail, has_insolvency, has_charges, accounts_overdue,
         churn["peak_churn"], churn["peak_churn_date"], churn["recent_churn"],
         churn["short_tenure_exits"]),
    )

    already_stored = conn.execute(
        "SELECT COUNT(*) FROM filings WHERE company_number = ?", (number,)
    ).fetchone()[0]

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
        if seen is None:
            # Keep the officer names / dates / share figures the API gives us,
            # stored as JSON text so we can use them later.
            values_json = json.dumps(f.get("description_values") or {})
            # Rules-based risk verdict, computed once and stored.
            f["severity"] = rule_severity({
                "company_name": name,
                "type": f.get("type"),
                "category": f.get("category"),
                "description": f.get("description"),
                "description_values": f.get("description_values") or {},
            })
            conn.execute(
                """INSERT INTO filings
                   (transaction_id, company_number, date, type, category,
                    description, description_values, severity, first_seen, briefing)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
                (tid, number, f.get("date"), f.get("type"), f.get("category"),
                 f.get("description"), values_json, f["severity"], now),
            )
            new_filings.append(f)

    conn.commit()
    return name, number, already_stored, new_filings


def main():
    conn = setup_database()
    watchlist = read_watchlist()
    print(f"Polling {len(watchlist)} companies...\n")

    briefings_left = MAX_BRIEFINGS_PER_RUN

    for company in watchlist:
        name, number, already_stored, new_filings = process_company(conn, company)

        if already_stored == 0:
            print(f"{name} ({number}) — baseline recorded: {len(new_filings)} filings\n")
            continue

        if not new_filings:
            print(f"{name} ({number}) — no new filings\n")
            continue

        print(f"{name} ({number}) — {len(new_filings)} NEW filing(s):")
        for f in new_filings:
            print(f"    [{f.get('severity')}]  {f.get('date')}  {f.get('type')}  {f.get('description')}")

            if briefings_left > 0:
                brief_input = {
                    "company_name": name,
                    "company_number": number,
                    "date": f.get("date"),
                    "type": f.get("type"),
                    "category": f.get("category"),
                    "description": f.get("description"),
                    "description_values": f.get("description_values") or {},
                    "severity": f.get("severity"),
                }
                text = generate_briefing(brief_input)
                conn.execute(
                    "UPDATE filings SET briefing = ? WHERE transaction_id = ?",
                    (text, f.get("transaction_id")),
                )
                conn.commit()
                briefings_left -= 1
                print("\n" + text + "\n")
            else:
                print("    (briefing skipped — per-run cap reached)\n")

    conn.close()


if __name__ == "__main__":
    main()