"""
eval_verdict.py — deterministic evaluation of the rules-based risk verdict.

No model, no cost. Runs the severity rules over the test set and compares the
verdict to the analyst's ground truth. Reproducible: same result every time.
This is the headline accuracy number — the rules decide risk, so the rules are
what we hold to account.

Run with:  python eval_verdict.py
"""

import csv
import json
import sqlite3

from severity import combined_severity

DB_FILE = "data/signals.db"
EVAL_SET = "eval/eval_set.csv"
RESULTS_MD = "eval/verdict_results.md"


def company_filings(conn, number):
    return [dict(zip(["date", "type", "category", "description"], r)) for r in
            conn.execute("SELECT date, type, category, description FROM filings WHERE company_number = ?",
                         (number,))]


def main():
    conn = sqlite3.connect(DB_FILE)
    cases = list(csv.DictReader(open(EVAL_SET, encoding="utf-8")))

    rows, correct = [], 0
    for c in cases:
        r = conn.execute(
            """SELECT c.company_number, c.company_name, f.date, f.type, f.category,
                      f.description, f.description_values
               FROM filings f JOIN companies c ON c.company_number = f.company_number
               WHERE f.transaction_id = ?""",
            (c["transaction_id"],),
        ).fetchone()
        if not r:
            rows.append((c["company_name"], c["type"], c["expected_severity"], "MISSING", False))
            continue
        number, name, date, typ, cat, desc, vals = r
        f = {"company_name": name, "date": date, "type": typ, "category": cat,
             "description": desc, "description_values": json.loads(vals) if vals else {}}
        verdict = combined_severity(f, company_filings(conn, number))
        match = verdict == c["expected_severity"]
        correct += 1 if match else 0
        rows.append((name, typ, c["expected_severity"], verdict, match))
    conn.close()

    print(f"{'company':30} {'type':6} {'expected':9} {'verdict':9} match")
    for name, typ, exp, got, m in rows:
        print(f"{name[:30]:30} {typ:6} {exp:9} {got:9} {'OK' if m else 'x'}")
    print(f"\nVerdict accuracy: {correct}/{len(cases)}")

    with open(RESULTS_MD, "w", encoding="utf-8") as fh:
        fh.write("# Verdict evaluation (deterministic rules)\n\n")
        fh.write(f"Accuracy: **{correct}/{len(cases)}**. No model, no cost, reproducible.\n\n")
        fh.write("| Company | Type | Expected | Verdict | Match |\n|---|---|---|---|---|\n")
        for name, typ, exp, got, m in rows:
            fh.write(f"| {name} | {typ} | {exp} | {got} | {'✓' if m else '✗'} |\n")
    print(f"Wrote {RESULTS_MD}")


if __name__ == "__main__":
    main()
