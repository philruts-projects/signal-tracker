# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose and priorities

This is a learning-and-exploration project first, a product second. Phil is developing his
data/AI build skills and enjoying making something real. A working product is a welcome
outcome, not the point, and may never ship.

**Priority order — use it to settle any fuzzy call:**
1. Learning and developing skills.
2. Staying engaged and enjoying the process.
3. A working product.

When a choice is unclear (polish this or move on, add a source or tidy the last one), pick
whatever teaches more and keeps momentum. "Good enough to learn from and move on" beats
commercial polish. Do not gold-plate. Build the smallest useful thing, look at the real data,
then decide what's next. We change direction when the data tells us to — that's expected.

**What it is.** Signal Tracker watches a watchlist of UK companies via the free Companies House
API, detects material change in each, scores how much attention it warrants, and uses the Claude
API to explain the change in plain English. The output is a prioritised review queue for a credit
manager — not a score, not a prediction of collapse. Working bet: value comes from combining
several sources against the user's own exposure, not any single register, so we widen it one
source at a time and see if the bet holds.

There is background from an earlier, more "commercial product" framing in `docs/product-brief.md`
and `docs/discovery-plan.md`. Treat those as reference, not marching orders — the priority order
above wins. Do not gate work behind a "discovery phase"; we build, look, and learn.

## About the developer

Phil is a commercial data leader (13 years, ex-Head of Data, Insight & Analytics) and the
product owner — not a professional software engineer. He makes the product and technical
calls and needs to understand every step well enough to own and explain it, so define
jargon and stage the work accordingly.

## How to work with me

- **Use VS Code wherever possible.** Prefer VS Code's integrated terminal and
  Source Control panel for all dev steps. When there's a VS Code way to do
  something, show that first.
- **Explain the jargon.** Define technical terms inline the first time they come
  up (e.g. scaffold, harness, remote, branch). Assume no prior software
  engineering background.
- **Stage the work.** Break tasks into clear, ordered steps with checkpoints, so
  I can do each step myself and understand it.
- **Vertical slice first.** Build the smallest end-to-end working path before
  widening scope. The watchlist is the product, the briefing is the value,
  everything else is enrichment (see `BACKLOG.md`).
- **Keep it simple; don't over-build.** Smallest useful step, then stop and show me. No layers I didn't ask for. This is the guardrail against the over-engineering that crept in before.
- **Ask "so what".** If a feature or a number doesn't help a user decide, say so.
- **Write like a person, not a chatbot.** Plain English. Avoid AI-speak (leverage, robust, seamless, delve, navigate, showcase, foster, nuanced, and similar).
- **Be honest.** Flag concerns and dead ends. Don't just cheer.
- **Never commit secrets.** The keys live in `.env`, which is git-ignored.
- Never run tracker.py or run_eval.py without asking first — they call external APIs, cost money, and change the database.

**Output style — i-have-adhd is ON for every reply.** Follow `skills/i-have-adhd/SKILL.md`
in full (move it to `.claude/skills/i-have-adhd/SKILL.md` if you want Claude Code to auto-load it as `/i-have-adhd`). In short: lead with the next action (a command, path or step — not preamble); number
multi-step work; restate where we are each turn ("step 3 of 5 done, next is…"); give specific time
estimates; make finished work visible; no preamble, no recap, no closing pleasantries. It stays on
until Phil says "stop adhd mode". The "explain the jargon" and "stage the work" rules above still
apply — when Phil asks to be walked through something, explain fully but keep the shape.

## Model choice — recommend a switch, then ask

Phil pays per model tier, so the cost of a session depends on which model is running it. At
the start of every chat, and whenever the kind of work changes mid-chat, say which tier fits
the next stretch of work and ask a yes/no question: *"This is build work; Sonnet would do it
for less. Switch? (yes/no)"* or *"This is a planning call; worth a stronger model. Switch?
(yes/no)"*. One line, then carry on with whatever he answers. Never switch silently and never
nag — one recommendation per change of work type.

**Cheaper tier (Sonnet) is the default** for build sessions: writing or editing scripts
against a pattern that already exists in the repo, staged VS Code steps, reading tracebacks,
paste and indentation fixes, doc updates, commits. `CLAUDE.md` and the primer carry the
context, so the model doesn't need to be clever, it needs to be careful.

**Stronger tier (Opus / Fable) for judgement moments**, which are rarer and shorter:
- a planning session — choosing the next slice, deciding whether a data source earns its place
- interpreting real data against the product's purpose (e.g. "is this early warning or
  aftermath?"), where a weaker model tends to say "great, add it"
- anything shaped like the external review: critique, finding what the code claims but
  doesn't do
- working out an undocumented API from thin evidence
- the last read of a doc or post before it goes public

The known failure mode of a cheaper model on this project isn't wrong code, it's
over-building and cheerleading, which the priorities above exist to prevent. If a session
on the cheaper tier starts adding layers nobody asked for, that's the signal to switch up.

## Tech stack

- Python 3.12 in a conda environment named `signal-tracker`
- `requests`, `python-dotenv`, `anthropic`, `streamlit`, `pandas` (see `requirements.txt`)
- SQLite (`data/signals.db`, git-ignored) for storage, Streamlit (`app.py`) for the dashboard —
  both already built, not future phases

## Commands

```bash
# one-time setup
conda create -n signal-tracker python=3.12 -y
conda activate signal-tracker
pip install -r requirements.txt
cp .env.example .env      # then paste CH_API_KEY and ANTHROPIC_API_KEY into .env

# the pipeline: poll the watchlist, detect new filings, brief them, store in SQLite
python tracker.py

# the dashboard — read-only over data/signals.db, makes no API calls
streamlit run app.py

# add a company to the watchlist by name (one free Companies House search call)
python add_company.py "Marks and Spencer"

# tests
python tests/test_rules.py     # offline rule tests, stdlib only, no API key needed
python eval_verdict.py         # deterministic verdict regression suite, no API key needed

# full model evaluation — calls the real Claude API (Haiku, Sonnet, Opus-as-judge), costs money
python run_eval.py
```

Other top-level scripts (`probe_charges.py`, `probe_officers.py`, `probe_fca.py`, `probe_gazette.py`,
`first_call.py`, `first_briefing.py`, `fetch_filings.py`, `simulate_new_filing.py`) are
one-off exploration/scratch scripts used while building a feature, not part of the pipeline.

## Architecture

**Pipeline (`tracker.py`), run on each poll:**

1. For each row in `watchlist.csv`, fetch the company profile, officers list, and charges
   list from the Companies House API (`ch_get`). Each fetch is wrapped independently — if
   one fails, that source is recorded as unavailable (`profile_ok` / `officers_ok` /
   `charges_ok` = 0) rather than silently defaulting to a healthy-looking zero.
2. `officers.py` (`compute_churn`) and `charges.py` (`summarize_charges`) reduce the raw
   officer/charge lists to board-churn and secured-borrowing signals stored on the
   `companies` row.
3. Fetch filing history and diff it against the `filings` table by `transaction_id` (the
   permanent Companies House key) to find genuinely new filings. A company's first-ever poll
   is stored as `baseline` history and never briefed.
4. Each new filing gets a verdict from `severity.py`'s `combined_severity` (thresholds are read
   from `rules.csv` at import, so tuning is a data edit, not a code edit): a single-filing
   rule (`rule_severity` — insolvency, strike-off, charges, founder-departure terminations,
   ARD changes, capital events) escalated by a cross-filing pattern check
   (`pattern_severity` — charge clusters, repeated ARD changes). `pattern_severity` is
   **point-in-time safe**: it only looks at filings dated on or before the one being scored,
   so a later event can never retroactively change an earlier verdict (see
   `tests/test_rules.py`).
5. New filings queue as `briefing_status='pending'`. A separate pass (`brief_pending`) pulls
   from this **persistent, worst-first queue** — ordered Critical > Serious > Watch > Routine,
   not insertion order — capped at `MAX_BRIEFINGS_PER_RUN` Claude calls per run, so a surge of
   filings can't run up a bill; anything past the cap simply waits for the next run instead of
   being dropped. `briefing.py` builds the prompt (using `lookups.py` for a plain-English
   filing-type label) and calls the Claude API.

**Dashboard (`app.py`):** read-only over SQLite, no network calls. For each company it
combines the status-based risk (`severity.py`'s `company_risk` — Unknown if the profile fetch
failed, else derived from registered status / insolvency history / accounts-overdue / churn)
with that company's own filing-level signal counts via `portfolio_company_risk`, so a freshly
detected Serious filing can escalate the headline even when the registered status alone still
looks fine. Board churn and secured-charge counts are shown only as corroboration on an
already-flagged company, never as a standalone trigger. `cluster_summaries` groups
same-pattern filings (a charge burst, repeated ARD changes) into one line rather than listing
each filing separately, since the cluster is the actual signal.

**Evaluation (two separate, non-overlapping harnesses — see `eval/EVALUATION.md`):**
- `eval_verdict.py` — deterministic regression check that `severity.py`'s rules still produce
  the expected verdict on 12 curated real filings (`eval/eval_fixtures.json`,
  `eval/eval_set.csv`). No API key, no cost, no database needed; reproducible from a clean
  clone.
- `run_eval.py` — judges the *briefing prose* (not the verdict) by generating a briefing with
  Haiku and Sonnet for each case and scoring it with Opus as judge. Requires an API key and
  spends real money; reads filings from the local `data/signals.db`, so it needs `tracker.py`
  to have populated that database first.

**Data model (`data/signals.db`, created by `tracker.py`):**
- `companies` — one row per watchlist company: registered status, insolvency/overdue flags,
  churn and charges summaries, and the three `*_ok` fetch-health flags.
- `filings` — one row per filing, keyed on the immutable `transaction_id`; carries the
  assigned `severity`, the generated `briefing` text, and `briefing_status`
  (`baseline` / `pending` / `done` / `failed`) that drives the queue.
- Always key on company **number**, never name — names aren't unique over time and
  subsidiaries have their own numbers (see `BACKLOG.md` for examples).
