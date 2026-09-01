"""
severity.py — assign a risk verdict to a single filing, and a review-priority to a company.

Rules-based and explainable. The model writes the narrative; these rules set the
verdict, so the tool can't quietly under-call a serious event the way a model can.
Encodes the heuristics from the Phase 6 evaluation and the domain review.

Known blind spots (documented, not hidden): with only a single filing we can't tell
a *finance* director's exit from any other (Companies House holds no executive title and
the officer occupation field is empty). Charge clusters and repeated accounting-date
changes ARE now detected across filings (see pattern_severity); a lone director's role is
the remaining data ceiling.
"""

import re
from datetime import datetime

_ORDER = {"Routine": 0, "Watch": 1, "Serious": 2, "Critical": 3}

CAPITAL_WATCH_THRESHOLD = 500_000_000  # GBP; crude size cue pending a %-of-revenue rule

# Accounting-reference-date changes: how many changes within the window elevate to Serious.
# This COUNTS THE CURRENT FILING, so a value of 2 means "the second change within the window".
# (Deliberately the second, not the third: two ARD changes inside 18 months is already unusual.)
ARD_CHANGES_TO_ELEVATE = 2
ARD_WINDOW_MONTHS = 18

CHARGE_CLUSTER_COUNT = 3      # charges within the window (incl. this one) that elevate to Serious
CHARGE_CLUSTER_DAYS = 30      # look-back window for the cluster, in days


def _date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _months_between(later, earlier):
    """Whole calendar months from `earlier` to `later` (0 if same month). Negative if later < earlier."""
    return (later.year - earlier.year) * 12 + (later.month - earlier.month)


def _is_eponymous_officer(company_name, officer_name):
    """True when the departing officer's surname appears as a WHOLE WORD in the company name.

    Whole-word match (not substring) so 'King' does not match 'Kingfisher'. This is a
    heuristic for an eponymous / likely-founder departure — a signal to elevate, per the
    domain review that founder departures always warrant a flag — not a claim of fact.
    """
    if not company_name or not officer_name:
        return False
    surname = officer_name.strip().split()[-1].lower()
    if len(surname) <= 3:
        return False
    return re.search(r"\b" + re.escape(surname) + r"\b", company_name.lower()) is not None


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
        if "satisf" in desc:          # charge marked satisfied: security discharged
            return "Routine"
        return "Watch"                # registered charge: fresh security registered

    # Officer terminations — eponymous / likely-founder departures elevate
    if typ.startswith("TM"):
        return "Serious" if _is_eponymous_officer(company, vals.get("officer_name")) else "Routine"

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

    Point-in-time safe: only filings dated ON OR BEFORE this one are counted, so a
    historical verdict can never be helped by a filing that had not happened yet. Only the
    distress-leaning patterns are here (charge cluster, repeated ARD change); board churn is
    deliberately excluded — it's ambiguous (see company_risk).
    """
    fdate = _date(f.get("date"))
    if fdate is None:
        return "Routine"

    # A burst of registered charges: CHARGE_CLUSTER_COUNT+ within the look-back window,
    # counting this one and earlier ones only (never later ones).
    if _is_charge_create(f):
        near = sum(1 for o in company_filings
                   if _is_charge_create(o) and _date(o.get("date"))
                   and 0 <= (fdate - _date(o.get("date"))).days <= CHARGE_CLUSTER_DAYS)
        if near >= CHARGE_CLUSTER_COUNT:
            return "Serious"

    # Repeated accounting-reference-date changes: this one plus earlier ones within the window.
    if _is_ard_change(f):
        count = sum(1 for o in company_filings
                    if _is_ard_change(o) and _date(o.get("date"))
                    and 0 <= _months_between(fdate, _date(o.get("date"))) <= ARD_WINDOW_MONTHS)
        if count >= ARD_CHANGES_TO_ELEVATE:
            return "Serious"

    return "Routine"


def combined_severity(f, company_filings):
    """Single-filing rule severity, escalated by any cross-filing pattern."""
    base = rule_severity(f)
    patt = pattern_severity(f, company_filings)
    return base if _ORDER[base] >= _ORDER[patt] else patt


def company_risk(status, has_insolvency_history=False, accounts_overdue=False, recent_churn=0,
                 profile_ok=True):
    """Company-level risk from its registered status — the strongest single signal.

    `profile_ok=False` means the profile fetch failed, so we DON'T KNOW the status: return
    'Unknown' rather than laundering a failed fetch into a reassuring 'Routine'.
    """
    if not profile_ok:
        return "Unknown"
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


def portfolio_company_risk(status, has_insolvency_history=False, accounts_overdue=False,
                           recent_churn=0, watch_signals=0, serious_signals=0, critical_signals=0,
                           profile_ok=True):
    """Company REVIEW PRIORITY: the status-based risk, escalated by the company's own
    filing-level signals so a freshly-detected Serious filing can't leave the headline at
    Routine (the central workflow bug the external review flagged).

    Returns (level, reason) where reason explains any filing-driven escalation ('' if the
    status-based risk already dominates). This is a review-priority heuristic, NOT a
    probability of insolvency.
    """
    base = company_risk(status, has_insolvency_history, accounts_overdue, recent_churn, profile_ok)

    # Only Serious/Critical filing signals raise a company's REVIEW PRIORITY. Watch signals
    # (a lone new charge, a large buyback, an accounting-date change) are shown on the card and
    # in the timeline, but deliberately do NOT turn a healthy company's headline amber on their
    # own — otherwise any large firm with historical secured borrowing reads as a concern, the
    # false-positive burden the review warned about. A genuine Watch CLUSTER (e.g. a burst of
    # charges) is already promoted to Serious by pattern_severity, so it escalates here as Serious.
    signal, reason = "Routine", ""
    if critical_signals:
        signal, reason = "Critical", f"{critical_signals} Critical filing signal(s) on record"
    elif serious_signals:
        signal, reason = "Serious", f"{serious_signals} Serious filing signal(s) on record"

    # If the profile fetch failed we still surface any filing signals we DO hold, but with
    # no filing signal the honest answer is 'Unknown', not 'Routine'.
    if base == "Unknown":
        return (signal, reason) if signal != "Routine" else ("Unknown", "Data unavailable — last fetch failed")

    if _ORDER[signal] > _ORDER[base]:
        return signal, reason
    return base, ""
