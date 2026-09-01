"""
severity.py — assign a risk verdict to a single filing.

Rules-based and explainable. The model writes the narrative; these rules set the
verdict, so the tool can't quietly under-call a serious event the way a model can.
Encodes the heuristics from the Phase 6 evaluation and the domain review.

Known blind spots (documented, not hidden): with only a single filing we can't tell
a *finance* director's exit from any other (needs the officers endpoint for roles),
and we can't see that a charge is one of a cluster (needs cross-filing pattern detection).
Those cases sit in the roadmap.
"""

from datetime import datetime

_ORDER = {"Routine": 0, "Watch": 1, "Serious": 2, "Critical": 3}

CAPITAL_WATCH_THRESHOLD = 500_000_000  # GBP; crude size cue pending a %-of-revenue rule


def _date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _is_founder(company_name, officer_name):
    """True when the departing officer's surname is in the company name (eponymous founder)."""
    if not company_name or not officer_name:
        return False
    surname = officer_name.strip().split()[-1].lower()
    return len(surname) > 3 and surname in company_name.lower()


def _largest_capital_figure(values):
    total = 0.0
    for item in (values or {}).get("capital", []) or []:
        try:
            total = max(total, float(str(item.get("figure", "0")).replace(",", "")))
        except (ValueError, TypeError):
            continue
    return total


def rule_severity(f):
    """Return 'Routine' | 'Watch' | 'Serious' | 'Critical' for a filing dict."""
    typ = (f.get("type") or "").upper()
    cat = (f.get("category") or "").lower()
    desc = (f.get("description") or "").lower()
    vals = f.get("description_values") or {}
    company = f.get("company_name") or ""

    # Insolvency: administration, liquidation, receivership, winding-up
    if cat == "insolvency" or any(k in desc for k in
            ("administration", "liquidation", "receiver", "winding-up", "wind-up", "insolvenc")):
        onset = any(k in desc for k in (
            "appointment-of-administrator", "appointment-of-a-receiver", "appointment-of-receiver",
            "winding-up", "wind-up", "resolution-for-winding-up", "compulsory", "moratorium",
            "in-administration-appointment"))
        return "Critical" if onset else "Serious"

    # Gazette strike-off notices
    if cat == "gazette" or "gazette" in desc or "strike-off" in desc or "strike off" in desc:
        return "Critical" if ("final" in desc or "dissolved" in desc) else "Serious"

    # Charges — secured borrowing
    if cat == "mortgage" or typ.startswith("MR"):
        if "satisf" in desc:          # charge satisfied: debt repaid, mildly reassuring
            return "Routine"
        return "Watch"                # new charge: fresh secured borrowing

    # Officer terminations — founder departures elevate
    if typ.startswith("TM"):
        return "Serious" if _is_founder(company, vals.get("officer_name")) else "Routine"

    # Accounting reference date change — can delay/obscure accounts
    if typ == "AA01" or "accounting-reference-date" in desc or "account-reference-date" in desc:
        return "Watch"

    # Capital events — flag on size (placeholder until a %-of-revenue rule exists)
    if cat == "capital" or typ.startswith("SH"):
        return "Watch" if _largest_capital_figure(vals) >= CAPITAL_WATCH_THRESHOLD else "Routine"

    return "Routine"


def _is_charge_create(o):
    t = (o.get("type") or "").upper()
    d = (o.get("description") or "").lower()
    return ((o.get("category") or "").lower() == "mortgage" or t.startswith("MR")) and "satisf" not in d


def _is_ard_change(o):
    return (o.get("type") or "").upper() == "AA01" or "reference-date" in (o.get("description") or "").lower()


def pattern_severity(f, company_filings):
    """Elevate based on cross-filing patterns within the same company.

    Only the distress-leaning patterns: a cluster of new charges, or a repeated
    accounting-reference-date change. Board churn is deliberately excluded — it's
    ambiguous (see company_risk).
    """
    fdate = _date(f.get("date"))
    if fdate is None:
        return "Routine"

    # A burst of new charges: 3+ within a 30-day window around this one.
    if _is_charge_create(f):
        near = sum(1 for o in company_filings
                   if _is_charge_create(o) and _date(o.get("date"))
                   and abs((_date(o.get("date")) - fdate).days) <= 30)
        if near >= 3:
            return "Serious"

    # Repeated accounting-reference-date changes: this one plus 1+ others in ~18 months.
    if _is_ard_change(f):
        prior = sum(1 for o in company_filings
                    if _is_ard_change(o) and _date(o.get("date"))
                    and 0 <= (fdate - _date(o.get("date"))).days <= 18 * 30)
        if prior >= 2:
            return "Serious"

    return "Routine"


def combined_severity(f, company_filings):
    """Single-filing rule severity, escalated by any cross-filing pattern."""
    base = rule_severity(f)
    patt = pattern_severity(f, company_filings)
    return base if _ORDER[base] >= _ORDER[patt] else patt


def company_risk(status, has_insolvency_history=False, accounts_overdue=False, recent_churn=0):
    """Company-level risk from its registered status — the strongest single signal."""
    s = (status or "").lower()
    if any(k in s for k in
            ("liquidation", "administration", "receiver", "insolvency", "voluntary-arrangement")):
        return "Critical"
    if "dissolved" in s or "removed" in s or "converted-closed" in s:
        return "Serious"
    if accounts_overdue:                 # active but not filing accounts on time
        return "Serious"
    # Board churn is a corroborator, not a trigger: mass resignations can just mean an
    # acquisition or a board refresh. Only elevate when other stress is present too.
    if recent_churn and recent_churn >= 3 and (has_insolvency_history or accounts_overdue):
        return "Serious"
    if has_insolvency_history:            # active, but has been in trouble before
        return "Watch"
    return "Routine"
