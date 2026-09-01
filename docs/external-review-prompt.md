# External review prompt

Paste everything below the line into a capable LLM (Claude, GPT, Gemini) to get an
independent critique of the Signal Tracker's approach, workflow, data sources and UI.

---

You are a senior data/AI product engineer and a credit-risk domain expert. I want a rigorous,
honest critique of a project — not encouragement. Push back hard, name weaknesses plainly, and
be specific. Where you suggest something, say *why* and *how*, and flag anything you think is a
dead end.

## What the project is

A tool called Signal Tracker that monitors a watchlist of UK companies and gives early warning
when one of them is heading for financial trouble, from public filings, in plain English. The
users are credit analysts, account managers and procurement/supplier-risk teams who currently do
this monitoring by hand, if at all. The value proposition: "it watches the companies you're
exposed to and tells you, in plain English, when one is heading for trouble in time to act."

It's a portfolio project built by a commercial data leader (13 years, most recently Head of Data,
Insight & Analytics at an InsurTech) who is moving into AI-enablement roles. He is not a
professional software engineer. The goal is to demonstrate the pattern of: spot a real problem,
build something end-to-end that solves it, and measure honestly whether it works.

Repo: https://github.com/philruts-projects/signal-tracker

## Tech stack

Python 3.12 (conda). `requests` + `python-dotenv` for the API layer, `sqlite3` for storage,
`anthropic` for the LLM briefings, `streamlit` + `pandas` for the UI. Data source so far is
exclusively the free Companies House REST API. LLM calls use Claude Haiku for briefings, with
Sonnet and Opus used only inside the evaluation harness.

## Architecture and workflow

The core design decision: **deterministic rules decide the risk verdict; the LLM only writes the
plain-English explanation.** This keeps the risk decision explainable, auditable and free to
evaluate, and confines the LLM to what it's good at (writing), not what it's unreliable at
(consistent judgement).

The pipeline (`tracker.py`), run per company on each poll:
1. Fetch the company **profile** (`/company/{n}`): registered status (active / administration /
   liquidation / dissolved), `has_insolvency_history`, `has_charges`, accounts-overdue flag.
2. Fetch **officers** (`/company/{n}/officers`): compute board churn (peak director resignations
   in a 90-day window, resignations in the last 180 days) and short-tenure exits.
3. Fetch **charges** (`/company/{n}/charges`): count outstanding vs satisfied secured borrowing,
   recent charges, and the lender names. (Companies House does not publish charge amounts.)
4. Fetch **filing history** (`/company/{n}/filing-history`, latest ~100 items) and detect
   genuinely new filings by diffing transaction IDs against a local SQLite store.
5. Assign a risk verdict to each new filing via the rules layer (see below).
6. For new filings only, and capped per run to control cost, send the filing to Claude Haiku to
   write a briefing (What happened / Why it matters / Suggested action), led by the verdict.

The rules layer (`severity.py`):
- Filing-level: type/category map to a base verdict (insolvency → Serious/Critical, a new charge
  → Watch, a founder's departure → Serious via a surname-in-company-name check, a large capital
  event → Watch on a crude £500m threshold, most else Routine).
- Cross-filing patterns escalate it: 3+ charges in a 30-day window → Serious; a 3rd+ change of
  accounting reference date in ~18 months → Serious.
- Company-level: registered status drives the top-line risk (administration/liquidation →
  Critical, dissolved → Serious). Board churn is treated as a *corroborator*, not a trigger — it
  only elevates when other stress is present — after discovering that a healthy company (Direct
  Line, being acquired) had the highest board churn on the watchlist. The lesson we drew: distress
  is a confluence of signals, not any single dimension.

Storage: SQLite, two tables — `companies` (status and the enrichment fields above) and `filings`
(transaction_id, type, category, description, description_values, severity, briefing).

## Evaluation

Two separate evaluations, because the tool makes two kinds of output:
- **Verdict eval** (`eval_verdict.py`): deterministic. Runs the rules over 12 curated real
  filings (routine changes at healthy insurers through to the run-up to Carillion/Greensill/LC&F
  collapses) and compares each verdict to a human analyst's ground truth. Currently **10/12**. The
  two misses are the Carillion CFO and CEO departures, which the rules call Routine because
  Companies House holds no executive title and the officer occupation field is empty — a genuine
  data ceiling.
- **Briefing-quality eval** (`run_eval.py`): Claude Haiku and Sonnet each write a briefing for
  every test case, and Claude Opus scores the *writing* (factual accuracy, usefulness, clarity,
  hallucination) — deliberately not severity, which the verdict eval owns. Runs clean: no parse
  errors, near-zero hallucinations, Haiku ≈ Sonnet so Haiku is kept for cost (~$0.30 per full run).

## Current UI

A Streamlit dashboard. A "Need attention" count up top, then the watchlist as cards ranked
worst-first: each card shows the company, a coloured risk dot, registered status, the count of
serious/critical signals, the latest signal, and — on already-flagged companies only —
corroborating lines for board churn and outstanding secured borrowing with the lender named. Each
card expands to the company's severity-tagged filing timeline with the briefings folded in.

## Known limitations

- Every source is Companies House. No regulatory, legal-notice, credit or news data yet.
- Role-blindness: can't tell a finance director's exit from any other, so some serious
  early-warning departures read as routine.
- Pattern detection is within-company only, and only for charge clusters and repeated
  accounting-date changes so far.
- The "latest 100 filings" fetch gives an uneven historical look-back per company.
- The demo companies already collapsed, so time-relative signals show historically for them.
- Rules live in code, not an editable config table.

## What I want from you

1. **Critique the approach and architecture.** Is "rules decide, LLM explains" the right split?
   Where is it fragile? What would you do differently, and why?
2. **Critique the workflow and evaluation.** Is the two-eval split sound? Is a 12-case, single-run
   eval good enough to claim anything? How would you make the evaluation more robust and more
   convincing to a hiring manager?
3. **Suggest data sources to integrate**, ranked by value-for-effort, with the specific signal
   each adds and its cost/access model. Be concrete about free vs paid and UK-specific sources.
   Flag any that duplicate what Companies House already gives.
4. **Suggest specific data points** — fields, ratios, derived metrics — that would sharpen the
   risk verdict, especially ones that turn single ambiguous signals into a defensible confluence.
5. **Suggest what this should look like from a UI/UX perspective.** How should a credit analyst
   actually work with it day to day? What's missing? What would you cut? How should severity,
   trend-over-time, and "what changed since I last looked" be presented?
6. **Name the biggest risks and blind spots** — false positives/negatives, the M&A-vs-distress
   ambiguity, over-reliance on the LLM, anything that would embarrass the tool in front of a real
   credit team.
7. **Sketch a credible v2.** If this person had two more weeks, what should they build, in what
   order, to make it genuinely useful and genuinely impressive?

Be specific and commercially grounded. Assume the reader is smart, time-poor, and wants the truth
more than reassurance. Where you're uncertain, say so rather than bluffing.
