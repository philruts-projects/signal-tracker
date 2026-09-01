"""
eval_verdict.py — deterministic regression suite for the rules-based risk verdict.

No model, no cost, and no private database: it runs the severity rules over 12 curated
real filings and compares each verdict to a human analyst's ground truth, reading a
COMMITTED fixture (eval/eval_fixtures.json) so anyone can reproduce it from a clean clone.

This is a REGRESSION SUITE, not a population accuracy claim — the 12 cases are hand-picked
(routine changes at healthy insurers through the run-up to Carillion/Greensill/LC&F) and the
labels were set by the builder. It proves the rules still behave as intended after a change;
it does not measure alert prevalence across the whole market. See eval/EVALUATION.md.

Run with:  python eval_verdict.py
"""

import csv
import json

from severity import combined_severity

EVAL_SET = "eval/eval_set.csv"
FIXTURES = "eval/eval_fixtures.json"
RESULTS_MD = "eval/verdict_results.md"


def load_fixtures():
    data = json.load(open(FIXTURES, encoding="utf-8"))
    by_tid, by_company = {}, {}
    for f in data["filings"]:
        by_tid[f["transaction_id"]] = f
        by_company.setdefault(f["company_number"], []).append(f)
    return data["company_names"], by_tid, by_company


def main():
    names, by_tid, by_company = load_fixtures()
    cases = list(csv.DictReader(open(EVAL_SET, encoding="utf-8")))

    rows, correct = [], 0
    for c in cases:
        f = by_tid.get(c["transaction_id"])
        if not f:
            rows.append((c["company_name"], c["type"], c["expected_severity"], "MISSING", False))
            continue
        number = f["company_number"]
        filing = {"company_name": names.get(number, c["company_name"]), "date": f["date"],
                  "type": f["type"], "category": f["category"], "description": f["description"],
                  "description_values": f.get("description_values") or {}}
        verdict = combined_severity(filing, by_company.get(number, []))
        match = verdict == c["expected_severity"]
        correct += 1 if match else 0
        rows.append((filing["company_name"], f["type"], c["expected_severity"], verdict, match))

    print(f"{'company':30} {'type':6} {'expected':9} {'verdict':9} match")
    for name, typ, exp, got, m in rows:
        print(f"{(name or '')[:30]:30} {typ:6} {exp:9} {got:9} {'OK' if m else 'x'}")
    print(f"\nRegression suite: {correct}/{len(cases)} cases match ground truth "
          f"(reproducible; no model, no database).")

    with open(RESULTS_MD, "w", encoding="utf-8") as fh:
        fh.write("# Verdict regression suite (deterministic rules)\n\n")
        fh.write(f"**{correct}/{len(cases)}** curated cases match the analyst's ground truth. "
                 f"No model, no cost, no private database — runs from `eval/eval_fixtures.json`.\n\n")
        fh.write("This is a regression check that the rules still behave as intended, not a "
                 "population accuracy figure. See [EVALUATION.md](EVALUATION.md).\n\n")
        fh.write("| Company | Type | Expected | Verdict | Match |\n|---|---|---|---|---|\n")
        for name, typ, exp, got, m in rows:
            fh.write(f"| {name} | {typ} | {exp} | {got} | {'✓' if m else '✗'} |\n")
    print(f"Wrote {RESULTS_MD}")


if __name__ == "__main__":
    main()
