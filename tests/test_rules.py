"""
test_rules.py — offline tests for the deterministic rules layer.

Stdlib only (plain asserts, no pytest) so it runs anywhere with no extra install:
    python tests/test_rules.py

Covers the behaviours the external review asked us to pin down: point-in-time safety,
the explicit accounting-date threshold, the whole-word founder match, the Unknown state,
and company-level escalation by filing signals.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import severity as s


def check(name, cond):
    if not cond:
        raise AssertionError(f"FAILED: {name}")
    print(f"  ok  {name}")


def run():
    # --- Whole-word founder / eponymous-officer match -------------------------
    check("Greensill matches Greensill Capital",
          s._is_eponymous_officer("Greensill Capital (UK) Ltd", "Alexander David Greensill"))
    check("King does NOT match Kingfisher (substring bug fixed)",
          not s._is_eponymous_officer("Kingfisher plc", "Robert King"))
    check("short surname ignored",
          not s._is_eponymous_officer("Sky plc", "Jo Sky"))

    # --- Unknown vs Routine ---------------------------------------------------
    check("failed profile -> Unknown", s.company_risk(None, profile_ok=False) == "Unknown")
    check("active -> Routine", s.company_risk("active") == "Routine")
    check("liquidation -> Critical", s.company_risk("liquidation") == "Critical")

    # --- Company escalation by filing signals ---------------------------------
    check("Serious filing lifts an active company to Serious",
          s.portfolio_company_risk("active", serious_signals=1)[0] == "Serious")
    check("Watch filing alone does NOT lift a healthy company (avoids false positives)",
          s.portfolio_company_risk("active", watch_signals=5)[0] == "Routine")
    check("no signals stays Routine",
          s.portfolio_company_risk("active")[0] == "Routine")
    check("status risk still dominates when higher",
          s.portfolio_company_risk("liquidation", watch_signals=1)[0] == "Critical")
    check("Unknown with a Critical filing still surfaces Critical",
          s.portfolio_company_risk(None, profile_ok=False, critical_signals=1)[0] == "Critical")
    check("Unknown with no signals stays Unknown",
          s.portfolio_company_risk(None, profile_ok=False)[0] == "Unknown")

    # --- Accounting-reference-date threshold (explicit: the SECOND change) -----
    def ard(date):  # a minimal AA01 filing dict
        return {"date": date, "type": "AA01", "category": "", "description": "change-account-reference-date"}
    one = [ard("2018-01-01")]
    two = [ard("2018-01-01"), ard("2018-06-01")]
    check("first ARD change is not elevated",
          s.pattern_severity(ard("2018-01-01"), one) == "Routine")
    check("second ARD change within window is Serious",
          s.pattern_severity(ard("2018-06-01"), two) == "Serious")
    check("second ARD change OUTSIDE 18m window is not elevated",
          s.pattern_severity(ard("2020-01-01"), [ard("2018-01-01"), ard("2020-01-01")]) == "Routine")

    # --- Charge cluster is point-in-time safe (no look-ahead) -----------------
    def mr(date):
        return {"date": date, "type": "MR01", "category": "mortgage", "description": "mortgage-create"}
    # Three charges over three days; evaluate the FIRST one. A point-in-time-safe rule must
    # NOT see the two that come AFTER it, so the first charge is only a Watch, not Serious.
    cluster = [mr("2017-10-01"), mr("2017-10-02"), mr("2017-10-03")]
    check("first charge of a cluster is not retro-elevated by later charges",
          s.pattern_severity(mr("2017-10-01"), cluster) == "Routine")
    check("last charge of a 3-cluster within 30d is Serious",
          s.pattern_severity(mr("2017-10-03"), cluster) == "Serious")
    # Adding a LATER charge cannot change an EARLIER filing's verdict.
    before = s.combined_severity(mr("2017-10-02"), [mr("2017-10-01"), mr("2017-10-02")])
    after = s.combined_severity(mr("2017-10-02"), [mr("2017-10-01"), mr("2017-10-02"), mr("2099-01-01")])
    check("a future filing does not alter an earlier verdict", before == after)

    print("\nAll rule tests passed.")


if __name__ == "__main__":
    run()
