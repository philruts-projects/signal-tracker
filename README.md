# Companies House Signal Tracker

Monitors a watchlist of UK companies via the free [Companies House API](https://developer.company-information.service.gov.uk/),
detects significant filing events, and uses the Claude API to generate plain-English
commercial briefings explaining what each event means and what action to take.

Built for credit, account-management and supplier-risk teams who currently do this
monitoring manually.

## Status

- [x] Phase 1 — Stakeholder brief (problem framing)
- [x] Phase 2 — Repo, API key, first working API call  ← *in progress*
- [x] Phase 3 — Data layer (poll API, detect new filings, store in SQLite)
- [ ] Phase 4 — Claude layer (generate plain-English briefings)
- [ ] Phase 5 — Streamlit UI
- [ ] Phase 6 — Evaluation (accuracy and failure modes)
- [ ] Phase 7 — README, LinkedIn post, Loom walkthrough

## Setup

1. Create and activate a virtual environment (`python -m venv .venv`).
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and paste your Companies House API key in.
4. Run the first call: `python first_call.py`.

## How to get an API key

Register at Companies House, create an "application" in the developer hub, and
generate a REST API key. Full guide: <https://developer.company-information.service.gov.uk/get-started>