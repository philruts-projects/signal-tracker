# Phase 6 — Evaluation

How well does the Signal Tracker turn a Companies House filing into a useful, correctly-calibrated
commercial briefing? This evaluates the real product prompt against a curated set of real filings,
scored by an independent model and calibrated against human judgement.

## Method

**Test set (12 real filings, `eval/eval_set.csv`).** Deliberately spanning the severity range and,
crucially, built around the *run-up to failure* rather than the aftermath — because the value of the
tool is early warning, not labelling a company that has already collapsed. The set mixes:

- Routine filings at healthy insurers (director changes, interim accounts, confirmation statement, a share allotment).
- Two contextual "watch" cases (a very large share cancellation; a repeated accounting-reference-date change).
- Genuine pre-collapse warning signals from Carillion (CFO exit, CEO exit, a charge from the Oct-2017 cluster), Greensill (founder removed) and the actual Greensill administration.

**Ground truth** was set by a domain expert (commercial data leader): an expected severity
(Routine / Watch / Serious / Critical) and the key facts a good briefing must get right.

**Models compared.** Every filing was briefed by **Claude Haiku 4.5** and **Claude Sonnet** using the
identical production prompt.

**Scoring (hybrid).** **Claude Opus** acted as an independent LLM-as-judge, scoring each briefing 1–5 on
factual accuracy, interpretation, and action usefulness, plus assigned severity, a severity-match flag,
and a hallucination flag. The human expert then **spot-checked and confirmed** the judge's calls, so the
automated scores are reported with human calibration behind them (mitigating the "AI grading AI" concern).

**Cost** was measured from real token usage. Full run: **$0.30** for 24 briefings + 24 judgements.

## Headline results

Average judge scores (over cases scored cleanly):

| Model | Factual | Interpretation | Action | Overall | Severity match | Hallucinations |
|---|---|---|---|---|---|---|
| Haiku 4.5 | 4.5 | 3.5 | 3.4 | 3.5 | 7/10 | 0/10 |
| Sonnet | 4.9 | 3.8 | 3.4 | 3.8 | 7/10 | 0/10 |

## Key findings

**1. Strong at the extremes.** Routine filings were correctly kept calm (cases 1–4: both models factual,
low-urgency, no false alarms), and the unambiguous crisis — Greensill entering administration — was handled
excellently by both ("freeze new credit, submit claims via the administrator", 4–5/5). As a first-pass triage
that separates noise from genuine crisis, the tool works.

**2. It systematically under-flags the early-warning signals — the highest-value cases.** All three severity
mismatches are *under-calls* on pre-collapse signals:

- Carillion's **finance director** departing (~1 year before collapse) → scored **Watch**, not Serious. Haiku didn't even register that Adam was the finance chief.
- Carillion's **CEO** departing (~6 months before) → **Watch**, both models hedging on whether Howson was CEO.
- LC&F's **third accounting-date change in 15 months** → dismissed by Haiku as "administrative housekeeping", Routine.

**Root cause: single-filing context blindness.** Each briefing sees one filing in isolation, so it cannot
know that Adam was the *finance* director, that this was the *third* date change, or that the charge was
*one of five in a week*. From a one-filing view, "a director resigned" genuinely is routine. The model is
not so much wrong as blind — and this is exactly the **pattern-detection gap**: real distress is a *cluster*
of filings over time, and the current tool reads them one at a time.

**3. Haiku is good enough; Sonnet's 3× cost buys no better risk calibration.** Sonnet is marginally more
polished (factual 4.9 vs 4.5) but identical on severity matching (7/10), and on the Carillion charge it was
actually *worse* — Sonnet called it Watch where Haiku correctly called it Serious. For this task the evidence
supports the cheaper model.

**4. Zero hallucinations across all 24 briefings.** The instruction to base briefings only on the supplied
filing, and to flag ambiguity rather than invent, held completely.

**5. Severity calibration is the weak spot, and it errs in the worst direction — under-calling risk.** A tool
that misses a serious signal is more dangerous than one that over-flags a routine one.

## Failure modes

*Of the product:*

- **No role context** — it can't tell a departing *finance director* from any other director.
- **No history** — it can't see that a filing is the third of its kind (repeated accounting-date changes).
- **No clustering** — it can't see that a charge is one of five filed the same week, or that three board
  departures happened in six months. This is the single most important limitation.

*Of the evaluation method (stated for honesty):*

- The Opus judge returned unparseable JSON on **4 of 24** scoring calls (needs a retry / stricter parse).
- Sonnet's briefings twice exceeded the 300-token output cap and were cut off mid-sentence (raise the cap for verbose models).
- **n = 12, single run.** No repeated runs to measure variance; conclusions are directional, not statistically robust.
- The judge is itself a model; human spot-check calibration mitigates but does not eliminate this.

## Recommendations (roadmap)

The evaluation points directly at the next build, most of it already in `BACKLOG.md`:

1. **Give the model context so it can stop being blind.** Add the filing-type role/label, the company's
   current status (active / in administration — from the company profile endpoint), and a window of the
   company's recent filings. This alone would likely fix most under-calls.
2. **Cluster/pattern detection** — the headline feature. Flag *sequences*: multiple board exits, repeated
   date changes, bursts of charges. This is where the real early-warning value lives.
3. **Encode the human heuristics** surfaced in review: always elevate a founder departure; elevate
   finance-leadership churn; elevate charge clusters and repeated accounting-date changes; apply a
   size threshold to capital events.
4. **Keep Haiku** as the default model; revisit only if the task changes.
5. **Harden the harness**: robust judge parsing with retry, higher output cap, and multiple runs for variance.

## Bottom line

The Signal Tracker is a reliable *first-pass triage*: it separates routine filings from genuine crises,
gives sound, actionable briefings at both ends, and never fabricates. Its weakness is the valuable middle —
the subtle, early warnings that only make sense across *several* filings — because it currently reads each
filing alone. That is not a flaw to paper over; it is the clearly-evidenced case for the next phase of work.
