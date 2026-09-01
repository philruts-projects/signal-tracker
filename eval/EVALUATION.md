# Evaluation

The tool makes two kinds of output, so it gets two kinds of test. The **risk verdict**
(Routine, Watch, Serious, Critical) is decided by deterministic rules, so it's checked
deterministically against a human analyst's ground truth. The **briefing** is written by
Claude, so its writing quality is judged separately. Keeping them apart matters: an earlier
version scored the verdict by reading the briefing's tone, which was noisy and, worse, measured
the wrong thing. The rules decide risk; the rules are what we hold to account.

Test set: 12 real filings (`eval/eval_set.csv`), spanning routine changes at healthy insurers
through to Carillion and Greensill in the run-up to collapse. Ground truth (expected severity
plus the key facts a briefing must get right) set by a commercial data leader.

## Eval 1 — the verdict (deterministic)

`eval_verdict.py` runs the rules over the test set and compares each verdict to ground truth.
No model, no cost, same answer every run.

**Accuracy: 10/12.** Full detail in [verdict_results.md](verdict_results.md).

Every routine filing is called correctly, Aviva's large buyback lands at Watch, Greensill's
founder departure and its administration are right, and the two pattern fixes hold: Carillion's
charge reads Serious because the rules see it's one of a cluster of five in a week, and London
Capital & Finance's accounting-date change reads Serious because the rules see it's the third in
fifteen months. Pattern detection moved this from 9 to 10.

The two misses are both Carillion director exits, the finance director and the CEO, which the
rules call Routine. There is no fix for these in the data: Companies House holds no executive
title and the officer `occupation` field is empty, so nothing in the record says one of these
people ran the finances. It's a genuine ceiling, and it stays in the report as one.

## Eval 2 — the briefing (writing quality)

`run_eval.py` has Claude Haiku and Claude Sonnet each write a briefing for every test filing,
then Opus scores the *writing* — factual accuracy, usefulness, clarity, and whether it invents
anything — deliberately **not** severity, which Eval 1 owns. Scores and side-by-side briefings
land in [results.md](results.md). Cost is about $0.30 a run.

What holds across runs: the briefings are factually accurate and don't hallucinate — the
instruction to stick to the supplied filing works. Haiku and Sonnet come out close, so Haiku
stays the default at a third of the cost. The one weakness the split exposed: a model would
occasionally write a flat, purely descriptive briefing for a serious event (Sonnet did exactly
this on the Greensill founder departure, stating the fact and stopping). The fix was to feed the
rules verdict into the briefing and make it lead with an explicit "Risk:" line, so a Serious
filing can't be written up as a shrug.

Two honest limits of the harness: the Opus judge occasionally returned malformed JSON, now
handled with a retry; and with 12 cases on a single run these numbers are directional, not
statistically robust.

## What this says about the product

It's a reliable first-pass triage. Routine filings stay quiet, real crises get the right verdict
and a sound, plainly-written action, and it doesn't fabricate. Its ceiling is knowledge the public
record doesn't contain — a director's actual role — and its remaining risk is the same one every
version has had: a single filing read alone can't see everything, which is why the charge-cluster
and repeated-date-change patterns matter and why more of that work is the road ahead.

## Recommendations

The rules layer earns most of the next investment, because it's where accuracy actually lives.
Lift the thresholds and mappings out of code into an editable rules table so a domain expert tunes
them directly. Keep widening the cross-filing patterns. Bring in the sources that add a
*different* dimension rather than more of the same — the FCA register for regulatory status, the
Gazette for the earliest formal notices — since the churn work taught us distress is a confluence,
not any single signal. Keep Haiku. And re-run both evals after each change: the verdict eval is
free and instant, so there's no excuse not to.
