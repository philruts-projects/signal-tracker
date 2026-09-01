"""
run_eval.py — Phase 6 evaluation harness.

For each filing in eval/eval_set.csv:
  1. Generate a briefing with Haiku AND with Sonnet (reusing the real product prompt).
  2. Have Opus score each briefing against the analyst's ground truth (severity + key facts).
  3. Track real token cost from the API usage.

Outputs:
  eval/results.json  — full machine-readable results
  eval/results.md    — readable side-by-side report with score summary

Run with:  python run_eval.py
"""

import os
import csv
import sys
import json
import sqlite3

import anthropic
from dotenv import load_dotenv

from briefing import SYSTEM_PROMPT, build_user_prompt, extract_text

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("No ANTHROPIC_API_KEY found. Check your .env file.")

DB_FILE = "data/signals.db"
EVAL_SET = "eval/eval_set.csv"
RESULTS_JSON = "eval/results.json"
RESULTS_MD = "eval/results.md"

# Model IDs — if any string errors when you run this, adjust it here.
HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-5"
JUDGE = "claude-opus-5"

# $ per million tokens: (input, output)
PRICES = {HAIKU: (1.0, 5.0), SONNET: (3.0, 15.0), JUDGE: (5.0, 25.0)}

client = anthropic.Anthropic()
cost_total = 0.0


def add_cost(model, usage):
    global cost_total
    p_in, p_out = PRICES.get(model, (0.0, 0.0))
    c = usage.input_tokens / 1e6 * p_in + usage.output_tokens / 1e6 * p_out
    cost_total += c
    return c


def load_filing(conn, tid):
    row = conn.execute(
        """SELECT c.company_name, c.company_number, f.date, f.type, f.category,
                  f.description, f.description_values, f.severity
           FROM filings f JOIN companies c ON c.company_number = f.company_number
           WHERE f.transaction_id = ?""",
        (tid,),
    ).fetchone()
    if not row:
        return None
    name, num, date, typ, cat, desc, vals, severity = row
    return {
        "company_name": name,
        "company_number": num,
        "date": date,
        "type": typ,
        "category": cat,
        "description": desc,
        "description_values": json.loads(vals) if vals else {},
        "severity": severity,
    }


def make_briefing(f, model):
    msg = client.messages.create(
        model=model,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(f)}],
    )
    add_cost(model, msg.usage)
    return extract_text(msg)


JUDGE_SYSTEM = (
    "You are a strict, fair evaluator of commercial filing briefings written for credit and "
    "risk teams. Score objectively against the analyst's ground truth. Reply with ONLY a JSON "
    "object, no prose, no code fences."
)


def judge(f, expected_severity, key_facts, briefing_text):
    prompt = (
        "FILING FACTS:\n"
        f"  company: {f['company_name']}\n"
        f"  date: {f['date']}   type: {f['type']}   description: {f['description']}\n"
        f"  values: {json.dumps(f['description_values'])}\n\n"
        "GROUND TRUTH (from a human analyst):\n"
        f"  expected_severity: {expected_severity}\n"
        f"  key_facts: {key_facts}\n\n"
        "BRIEFING TO SCORE:\n"
        f"{briefing_text}\n\n"
        "Score the briefing on 1-5 scales (5 = best). 'severity_matches_expected' is whether the "
        "briefing's implied urgency matches expected_severity. Return ONLY this JSON:\n"
        '{"factual_accuracy":0,"interpretation":0,"action_usefulness":0,'
        '"assigned_severity":"Routine|Watch|Serious|Critical",'
        '"severity_matches_expected":true,"hallucination":false,"overall":0,'
        '"comment":"one short sentence"}'
    )
    msg = client.messages.create(
        model=JUDGE,
        max_tokens=350,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    add_cost(JUDGE, msg.usage)
    text = extract_text(msg).strip()
    start, end = text.find("{"), text.rfind("}")
    try:
        return json.loads(text[start:end + 1])
    except Exception as e:
        return {"error": f"could not parse judge output: {e}", "raw": text}


def _avg(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return round(sum(values) / len(values), 2) if values else None


def write_markdown(results):
    lines = ["# Phase 6 — Evaluation results\n"]
    lines.append(f"Test cases: {len(results)}  ·  Models: Haiku vs Sonnet  ·  Judge: Opus\n")

    # --- Summary table ---
    lines.append("## Summary (average judge scores)\n")
    lines.append("| Model | Factual | Interpretation | Action | Overall | Severity match | Hallucinations |")
    lines.append("|---|---|---|---|---|---|---|")
    for label in ("haiku", "sonnet"):
        fa, interp, act, overall, matches, halluc, n = [], [], [], [], 0, 0, 0
        for r in results:
            s = r["models"].get(label, {}).get("scores", {})
            if "error" in s:
                continue
            n += 1
            fa.append(s.get("factual_accuracy"))
            interp.append(s.get("interpretation"))
            act.append(s.get("action_usefulness"))
            overall.append(s.get("overall"))
            matches += 1 if s.get("severity_matches_expected") else 0
            halluc += 1 if s.get("hallucination") else 0
        lines.append(
            f"| {label.capitalize()} | {_avg(fa)} | {_avg(interp)} | {_avg(act)} | "
            f"{_avg(overall)} | {matches}/{n} | {halluc}/{n} |"
        )
    lines.append("")

    # --- Per-case detail ---
    lines.append("## Case-by-case\n")
    for i, r in enumerate(results, 1):
        f = r["filing"]
        case = r["case"]
        lines.append(f"### {i}. {f['company_name']} — {f['type']} ({f['date']})")
        lines.append(f"*Expected severity:* **{case['expected_severity']}**  ")
        lines.append(f"*Ground truth:* {case['key_facts']}\n")
        for label in ("haiku", "sonnet"):
            m = r["models"].get(label, {})
            s = m.get("scores", {})
            lines.append(f"**{label.capitalize()}**")
            lines.append("")
            lines.append("> " + m.get("briefing", "").replace("\n", "\n> "))
            lines.append("")
            if "error" in s:
                lines.append(f"*Judge:* error — {s['error']}\n")
            else:
                lines.append(
                    f"*Judge:* overall **{s.get('overall')}/5** · "
                    f"factual {s.get('factual_accuracy')} · interp {s.get('interpretation')} · "
                    f"action {s.get('action_usefulness')} · "
                    f"assigned **{s.get('assigned_severity')}** "
                    f"({'match' if s.get('severity_matches_expected') else 'MISMATCH'}) · "
                    f"hallucination: {s.get('hallucination')}  \n"
                    f"> _{s.get('comment','')}_\n"
                )
        lines.append("---\n")

    with open(RESULTS_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    conn = sqlite3.connect(DB_FILE)
    with open(EVAL_SET, newline="", encoding="utf-8") as fh:
        cases = list(csv.DictReader(fh))

    results = []
    for i, case in enumerate(cases, 1):
        tid = case["transaction_id"]
        f = load_filing(conn, tid)
        if not f:
            print(f"[{i}] MISSING filing {tid} — skipping")
            continue
        print(f"[{i}/{len(cases)}] {f['company_name']} {f['type']} — Haiku + Sonnet + judging...")
        entry = {"case": case, "filing": f, "models": {}}
        for label, model in (("haiku", HAIKU), ("sonnet", SONNET)):
            try:
                text = make_briefing(f, model)
                scores = judge(f, case["expected_severity"], case["key_facts"], text)
            except Exception as e:
                text, scores = f"(error: {e})", {"error": str(e)}
            entry["models"][label] = {"briefing": text, "scores": scores}
        results.append(entry)
        print(f"      running cost: ${cost_total:.3f}")

    conn.close()

    with open(RESULTS_JSON, "w", encoding="utf-8") as fh:
        json.dump({"total_cost_usd": round(cost_total, 4), "results": results}, fh, indent=2)
    write_markdown(results)

    print(f"\nDONE. Total cost: ${cost_total:.3f}")
    print(f"Wrote {RESULTS_JSON} and {RESULTS_MD}")


if __name__ == "__main__":
    main()
