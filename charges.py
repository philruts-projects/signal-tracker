"""
charges.py — summarise a company's registered charges (secured borrowing).

Companies House doesn't publish the amount, so we work with what's there: counts,
status (outstanding vs satisfied), creation dates, and the lender name. The useful
signal is fresh secured borrowing and who it's to, as corroboration on an
already-flagged company — not a number, and not a standalone trigger.
"""

from datetime import date, datetime

RECENT_DAYS = 365


def _date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def summarize_charges(items, today=None):
    today = today or date.today()

    outstanding = sum(1 for o in items if o.get("status") in ("outstanding", "part-satisfied"))
    recent = sum(1 for o in items
                 if _date(o.get("created_on"))
                 and 0 <= (today - _date(o.get("created_on"))).days <= RECENT_DAYS)

    rows = []
    for o in items:
        lenders = [p.get("name", "") for p in o.get("persons_entitled", [])]
        rows.append({
            "created_on": o.get("created_on"),
            "satisfied_on": o.get("satisfied_on"),
            "status": o.get("status"),
            "lender": lenders[0] if lenders else "",
        })
    rows.sort(key=lambda r: r.get("created_on") or "", reverse=True)

    return {
        "charges_total": len(items),
        "charges_outstanding": outstanding,
        "charges_recent": recent,
        "charges_rows": rows,
    }
