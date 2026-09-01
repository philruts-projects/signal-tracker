"""
tracker.py — Phase 4: poll the watchlist, store filings in SQLite, detect NEW
filings, and generate a plain-English Claude briefing for each new one.

Two design points hardened after the external review:
- Failed API fetches are recorded as failures (profile_ok/officers_ok/charges_ok = 0),
  NOT laundered into reassuring zeros — so an outage can't make a company look healthy.
- Briefings run from a PERSISTENT, WORST-FIRST QUEUE (any filing with briefing_status
  'pending'), so a new filing past the per-run cap is briefed on a later run rather than
  lost, and Critical/Serious filings are briefed before Routine ones.
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
from severity import combined_severity
from officers import compute_churn
from charges import summarize_charges

load_dotenv()
API_KEY = os.getenv("CH_API_KEY")
if not API_KEY:
    sys.exit("No CH_API_KEY found. Check your .env file.")

BASE_URL = "https://api.company-information.service.gov.uk"
DB_FILE = "data/signals.db"
MAX_BRIEFINGS_PER_RUN = 5     # hard cap on Claude calls per run
MAX_BRIEFING_ATTEMPTS = 3     # give up on a filing after this many failed briefing attempts

# Worst-first ordering for the briefing queue.
_SEVERITY_RANK_SQL = ("CASE severity WHEN 'Critical' THEN 3 WHEN 'Serious' THEN 2 "
                      "WHEN 'Watch' THEN 1 ELSE 0 END")


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
            short_tenure_exits     INTEGER,
            charges_total          INTEGER,
            charges_outstanding    INTEGER,
            charges_recent         INTEGER,
            charges_json           TEXT,
            profile_ok             INTEGER DEFAULT 1,
            officers_ok            INTEGER DEFAULT 1,
            charges_ok             INTEGER DEFAULT 1,
            last_polled            TEXT
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
            briefing           TEXT,
            briefing_status    TEXT,
            briefing_attempts  INTEGER DEFAULT 0
        )
    """)
    # Idempotent migrations so an existing DB gains the new columns without a rebuild.
    _add_columns(conn, "companies", {
        "profile_ok": "INTEGER DEFAULT 1", "officers_ok": "INTEGER DEFAULT 1",
        "charges_ok": "INTEGER DEFAULT 1", "last_polled": "TEXT"})
    _add_columns(conn, "filings", {
        "briefing_status": "TEXT", "briefing_attempts": "INTEGER DEFAULT 0"})
    # Backfill briefing_status for rows that predate the column: anything already briefed is
    # 'done'; the rest is treated as 'baseline' (historical backfill we never meant to brief),
    # so switching to the queue doesn't suddenly brief a company's entire filing history.
    conn.execute("UPDATE filings SET briefing_status='done' WHERE briefing IS NOT NULL AND briefing_status IS NULL")
    conn.execute("UPDATE filings SET briefing_status='baseline' WHERE briefing IS NULL AND briefing_status IS NULL")
    conn.commit()
    return conn


def _add_columns(conn, table, cols):
    for name, decl in cols.items():
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {decl}")
        except sqlite3.OperationalError:
            pass  # column already exists


def process_company(conn, company):
    """Fetch a company's filings, store any new ones, return the new filings."""
    number = company["company_number"].strip()
    name = company["company_name"].strip()

    # Pull the company profile for its registered status — the strongest single signal.
    # On failure, record profile_ok=0 and leave status NULL: 'don't know', not 'fine'.
    profile_ok = 1
    try:
        profile = ch_get(f"/company/{number}")
    except Exception:
        profile, profile_ok = {}, 0
    status = profile.get("company_status")
    status_detail = profile.get("company_status_detail")
    has_insolvency = 1 if profile.get("has_insolvency_history") else 0
    has_charges = 1 if profile.get("has_charges") else 0
    accounts_overdue = 1 if (profile.get("accounts") or {}).get("overdue") else 0

    # Board churn and tenure from the officers list.
    officers_ok = 1
    try:
        officers = ch_get(f"/company/{number}/officers?items_per_page=100").get("items", [])
        churn = compute_churn(officers)
    except Exception:
        churn = {"peak_churn": 0, "peak_churn_date": None, "recent_churn": 0, "short_tenure_exits": 0}
        officers_ok = 0

    # Secured borrowing from the charges list.
    charges_ok = 1
    try:
        charge_items = ch_get(f"/company/{number}/charges?items_per_page=100").get("items", [])
        ch = summarize_charges(charge_items)
    except Exception:
        ch = {"charges_total": 0, "charges_outstanding": 0, "charges_recent": 0, "charges_rows": []}
        charges_ok = 0

    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT OR REPLACE INTO companies
           (company_number, company_name, status, status_detail,
            has_insolvency_history, has_charges, accounts_overdue,
            peak_churn, peak_churn_date, recent_churn, short_tenure_exits,
            charges_total, charges_outstanding, charges_recent, charges_json,
            profile_ok, officers_ok, charges_ok, last_polled)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (number, name, status, status_detail, has_insolvency, has_charges, accounts_overdue,
         churn["peak_churn"], churn["peak_churn_date"], churn["recent_churn"],
         churn["short_tenure_exits"],
         ch["charges_total"], ch["charges_outstanding"], ch["charges_recent"],
         json.dumps(ch["charges_rows"]), profile_ok, officers_ok, charges_ok, now),
    )

    already_stored = conn.execute(
        "SELECT COUNT(*) FROM filings WHERE company_number = ?", (number,)
    ).fetchone()[0]
    is_baseline = already_stored == 0

    data = ch_get(f"/company/{number}/filing-history?items_per_page=100")
    filings = data.get("items", [])

    new_filings = []
    for f in filings:
        tid = f.get("transaction_id")
        if tid is None:
            continue
        seen = conn.execute(
            "SELECT 1 FROM filings WHERE transaction_id = ?", (tid,)
        ).fetchone()
        if seen is None:
            values_json = json.dumps(f.get("description_values") or {})
            f["severity"] = combined_severity({
                "company_name": name,
                "date": f.get("date"),
                "type": f.get("type"),
                "category": f.get("category"),
                "description": f.get("description"),
                "description_values": f.get("description_values") or {},
            }, filings)
            # Baseline filings are history — don't brief them. Genuinely new filings queue as 'pending'.
            status_flag = "baseline" if is_baseline else "pending"
            conn.execute(
                """INSERT INTO filings
                   (transaction_id, company_number, date, type, category,
                    description, description_values, severity, first_seen, briefing,
                    briefing_status, briefing_attempts)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, 0)""",
                (tid, number, f.get("date"), f.get("type"), f.get("category"),
                 f.get("description"), values_json, f["severity"], now, status_flag),
            )
            new_filings.append(f)

    conn.commit()
    return name, number, already_stored, new_filings


def pending_briefings(conn, cap):
    """Rows awaiting a briefing, WORST-FIRST, capped. Picks up leftovers from prior runs
    (still 'pending') as well as this run's new filings — nothing is stranded by the cap."""
    return conn.execute(
        f"""SELECT f.transaction_id, f.company_number, c.company_name, f.date, f.type,
                   f.category, f.description, f.description_values, f.severity, f.briefing_attempts
            FROM filings f JOIN companies c ON c.company_number = f.company_number
            WHERE f.briefing_status = 'pending'
            ORDER BY {_SEVERITY_RANK_SQL} DESC, f.date DESC
            LIMIT ?""",
        (cap,),
    ).fetchall()


def brief_pending(conn, cap):
    """Generate briefings for up to `cap` pending filings, worst-first."""
    rows = pending_briefings(conn, cap)
    for (tid, number, name, date, typ, cat, desc, vals, sev, attempts) in rows:
        brief_input = {
            "company_name": name, "company_number": number, "date": date, "type": typ,
            "category": cat, "description": desc,
            "description_values": json.loads(vals) if vals else {}, "severity": sev,
        }
        try:
            text = generate_briefing(brief_input)
            conn.execute(
                "UPDATE filings SET briefing = ?, briefing_status = 'done' WHERE transaction_id = ?",
                (text, tid))
            print(f"    briefed [{sev}] {name} — {typ} {date}")
        except Exception as e:
            attempts = (attempts or 0) + 1
            new_status = "failed" if attempts >= MAX_BRIEFING_ATTEMPTS else "pending"
            conn.execute(
                "UPDATE filings SET briefing_attempts = ?, briefing_status = ? WHERE transaction_id = ?",
                (attempts, new_status, tid))
            print(f"    briefing FAILED ({new_status}, attempt {attempts}) {name} {typ}: {e}")
        conn.commit()


def main():
    conn = setup_database()
    watchlist = read_watchlist()
    print(f"Polling {len(watchlist)} companies...\n")

    for company in watchlist:
        name, number, already_stored, new_filings = process_company(conn, company)
        if already_stored == 0:
            print(f"{name} ({number}) — baseline recorded: {len(new_filings)} filings\n")
        elif not new_filings:
            print(f"{name} ({number}) — no new filings\n")
        else:
            print(f"{name} ({number}) — {len(new_filings)} NEW filing(s):")
            for f in new_filings:
                print(f"    [{f.get('severity')}]  {f.get('date')}  {f.get('type')}  {f.get('description')}")
            print()

    # Briefing pass: worst-first, from the persistent queue, capped per run.
    pending_total = conn.execute("SELECT COUNT(*) FROM filings WHERE briefing_status='pending'").fetchone()[0]
    if pending_total:
        print(f"Briefing up to {MAX_BRIEFINGS_PER_RUN} of {pending_total} pending filing(s), worst-first:")
        brief_pending(conn, MAX_BRIEFINGS_PER_RUN)
        left = conn.execute("SELECT COUNT(*) FROM filings WHERE briefing_status='pending'").fetchone()[0]
        if left:
            print(f"\n{left} filing(s) still queued — they'll be briefed on the next run.")
    else:
        print("No filings awaiting a briefing.")

    conn.close()


if __name__ == "__main__":
    main()
