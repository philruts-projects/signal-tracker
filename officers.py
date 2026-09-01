"""
officers.py — board-churn and tenure signals from a company's /officers list.

Companies House doesn't hold executive titles, so we can't tell a finance director
from any other. What the officer records do carry is appointment and resignation
dates, and those expose the real early-warning signal: directors leaving in a cluster,
or a director who appears and vanishes. Both preceded Greensill and Carillion.
"""

from datetime import date, datetime, timedelta

CLUSTER_WINDOW_DAYS = 90     # a "short window" for a resignation cluster
RECENT_DAYS = 180            # what counts as churn happening "now"
SHORT_TENURE_DAYS = 18 * 30  # a director gone within ~18 months


def _parse(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def compute_churn(officers, today=None):
    """Return board-churn signals from a list of officer records."""
    today = today or date.today()

    resignations = sorted(
        d for d in (_parse(o.get("resigned_on")) for o in officers
                    if o.get("officer_role") == "director")
        if d
    )

    # Largest cluster of resignations inside any CLUSTER_WINDOW_DAYS window.
    peak, peak_date = 0, None
    for i, start in enumerate(resignations):
        window = [d for d in resignations[i:] if (d - start).days <= CLUSTER_WINDOW_DAYS]
        if len(window) > peak:
            peak, peak_date = len(window), window[-1]

    recent = sum(1 for d in resignations if 0 <= (today - d).days <= RECENT_DAYS)

    short_tenure = 0
    for o in officers:
        if o.get("officer_role") != "director":
            continue
        appointed, resigned = _parse(o.get("appointed_on")), _parse(o.get("resigned_on"))
        if appointed and resigned and 0 <= (resigned - appointed).days <= SHORT_TENURE_DAYS:
            short_tenure += 1

    return {
        "peak_churn": peak,
        "peak_churn_date": peak_date.isoformat() if peak_date else None,
        "recent_churn": recent,
        "short_tenure_exits": short_tenure,
    }
