"""
simulate_new_filing.py — a throwaway helper to prove the alert path works.

Deletes the single most recent filing we've stored for one company, so the
next `python tracker.py` run re-discovers it and reports it as NEW — exactly
as if the company had just filed something.
"""
import sqlite3

COMPANY = "02280426"  # Direct Line

conn = sqlite3.connect("data/signals.db")
row = conn.execute(
    "SELECT transaction_id, date, type, description FROM filings "
    "WHERE company_number = ? ORDER BY date DESC LIMIT 1",
    (COMPANY,),
).fetchone()

if row is None:
    print("Nothing stored for that company yet — run tracker.py first.")
else:
    conn.execute("DELETE FROM filings WHERE transaction_id = ?", (row[0],))
    conn.commit()
    print(f"Deleted stored filing: {row[1]} {row[2]} {row[3]}")
    print("Now run: python tracker.py  — it should report this as NEW.")

conn.close()