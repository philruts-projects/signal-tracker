"""
gazette.py — check The Gazette for corporate-insolvency notices on a company.

Shared by tracker.py (the live pipeline) and probe_gazette.py (the exploration script),
so there is one place that knows how to talk to this API, not two.

Findings from probing it (11 Sept 2026, see BACKLOG.md): notices arrive 4-14 days ahead
of the matching Companies House filing on real collapses, with zero false positives on
healthy companies — but every first notice IS the formal event (administrator appointed,
winding-up order). It's a faster Critical, not an earlier Watch.

Quirks this module works around:
  - the default python-requests User-Agent gets HTTP 403
  - adding an Accept header alongside data.json gets HTTP 500
  - some queries take well over 20 seconds; it's a free service with no SLA
"""

from datetime import date

import requests

BASE = "https://www.thegazette.co.uk/all-notices/notice/data.json"
CORPORATE_INSOLVENCY = "24"
TIMEOUT_SECONDS = 60

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    ),
}


def fetch_notices(company_number):
    """All corporate-insolvency notices mentioning this company number, oldest first.

    Raises requests.RequestException on failure — the caller decides how to record that
    (see tracker.py: a failed fetch is Unknown, never a clean 'no notices').
    """
    params = {
        "text": company_number,
        "categorycode": CORPORATE_INSOLVENCY,
        "sort-by": "oldest-date",
        "results-page-size": 50,
    }
    response = requests.get(BASE, params=params, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    payload = response.json()
    # The feed is Atom XML re-expressed as JSON, so a single result still arrives as a
    # one-item list, and no matches means no "entry" key at all.
    return payload.get("entry") or []


def earliest_notice(notices):
    """The oldest notice as a small plain dict, or None. `notices` must already be sorted
    oldest-first (fetch_notices does this), so this is just "the first one, tidied up"."""
    if not notices:
        return None
    n = notices[0]
    return {
        "date": n["published"][:10],
        "notice_code": n.get("f:notice-code"),
        "title": n.get("title"),
        "category": (n.get("category") or {}).get("@term"),
        "url": n["link"][1]["@href"] if len(n.get("link", [])) > 1 else None,
    }
