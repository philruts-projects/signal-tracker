# Signal Tracker

Most firms find out a customer or supplier is in trouble when the invoice bounces. The
warning signs were usually sitting on the Companies House register for months beforehand,
free to read, and nobody was watching. This watches them for you.

Signal Tracker monitors a watchlist of UK companies, picks out the filings that matter,
flags how much attention each company needs, and writes a plain-English briefing on each one. It's
built for the credit, account-management and supplier-risk teams who do this by hand today,
when they do it at all.

It's also a portfolio project: the point was to take a real commercial problem, build
something end to end that solves it, and then measure honestly whether it works. The
[evaluation](eval/EVALUATION.md) is the part I'm most pleased with, including where it
comes up short.

## What it does

You give it a watchlist (a list of company numbers in `watchlist.csv`). On each run it:

1. Pulls every company's recent filing history from the free Companies House API and its
   registered status (active, in administration, dissolved).
2. Works out which filings are new since it last looked, by keeping a record in a local
   SQLite database and comparing against it. Nothing gets flagged twice.
3. Puts a risk verdict on each new filing (Routine, Watch, Serious, Critical) using
   explainable rules that encode a few hard-won heuristics: a likely-founder departure elevates
   the flag, a registered charge is a secured-borrowing signal, anything insolvency-related is
   Serious or Critical. Cross-filing patterns escalate too — a burst of charges or a repeated
   accounting-date change reads as Serious, because distress is a cluster, not one filing.
4. Sends the genuinely new filings to the Claude API, which turns a code like
   `TM01 termination-director` into a short briefing: what happened, why it matters, what to
   do. There's a hard cap on briefings per run so a surge of filings can't run up a bill.

The dashboard (`app.py`) then leads with risk: your companies ranked worst-first, each with
its registered status up top, its filing-level signals folded in (so a Serious filing lifts the
headline, not just the sort order), and the briefings a click below. A company whose latest data
fetch failed shows as *Unknown* rather than being assumed healthy. Healthy companies stay quiet
at the bottom. If nothing needs you, it says so.

Risk here is a *review priority* — how much attention a company warrants — not a probability of
insolvency.

## How well does it work

Twelve real filings, from routine director changes at healthy insurers through to Carillion's
board walking out and Greensill entering administration, scored by an independent model (Opus)
and calibrated against a human analyst. The short version:

- Reliable at the extremes. Routine filings stay calm, genuine crises get the right alarm and
  sensible actions. Zero hallucinations across 24 briefings.
- Weak in the valuable middle. Its remaining blind spot is a departing director's *role*:
  Companies House holds no executive title, so it can't tell a finance chief's exit from any
  other. It now *does* detect clusters in the verdict — a burst of charges, repeated
  accounting-date changes read as Serious — though the written briefing still describes one
  filing at a time. Role-blindness is the genuine data ceiling and the case for the next build.
- Haiku is good enough. It matched Sonnet on risk calls at a third of the cost, so Haiku is the
  default.

Full write-up, method and failure modes: [eval/EVALUATION.md](eval/EVALUATION.md).

## Running it

Needs Python 3.12, a free Companies House API key, and an Anthropic API key.

```bash
# environment (conda; a plain venv works too)
conda create -n signal-tracker python=3.12 -y
conda activate signal-tracker
pip install -r requirements.txt

# keys
cp .env.example .env      # then paste both keys into .env

# poll the watchlist, detect new filings, brief them
python tracker.py

# open the dashboard
streamlit run app.py
```

`.env` holds `CH_API_KEY` and `ANTHROPIC_API_KEY` and is git-ignored, so keys never leave your
machine. One gotcha: the Anthropic key must be scoped to a specific workspace, not an
identity-linked "all workspaces" key, or the API rejects it.

Companies House key: register at the [developer hub](https://developer.company-information.service.gov.uk/get-started),
create an application, generate a REST key.

## Project layout

- `watchlist.csv` — the companies being watched (edit by hand for now)
- `tracker.py` — the main loop: poll, detect, score, brief, store
- `severity.py` — the rules that assign a risk verdict
- `briefing.py` — the Claude prompt and call
- `lookups.py` — plain-English labels for filing-type codes
- `app.py` — the Streamlit dashboard
- `run_eval.py` + `eval/` — the evaluation harness, test set and results
- `BACKLOG.md` — what's deliberately parked, and why

## What's next

The evaluation points straight at it: give the model cross-filing context so it can spot
patterns rather than react to one filing at a time. Officer roles (to know a departing
director was the CFO), clustering (multiple exits, a burst of charges), and the other data
sources parked in [BACKLOG.md](BACKLOG.md) — the Gazette, the FCA register. Search-to-add so
users aren't editing a CSV. None of it changes the core; it sharpens the middle, which is
where the value is.

## About

Built by Phil Rutter, a commercial data leader moving into AI enablement. Companies House data
is Crown copyright, used under the [Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/).
Briefings are advisory and always cite the underlying filing; this is not financial or legal advice.
