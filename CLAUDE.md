# Project instructions for Claude

Standing context for the Companies House Signal Tracker. Read this before helping.

## About this project

An AI portfolio project: monitors a watchlist of UK companies via the free
Companies House API, detects significant filing events, and uses the Claude API
to generate plain-English commercial briefings. Full context in
`docs/stakeholder-brief.md`.

## About the developer

Phil is a commercial data leader (13 years) transitioning into AI enablement,
not a professional software engineer. He is building this to learn, and needs to
understand every step well enough to explain it at interview.

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
- **Never commit secrets.** The API key lives in `.env`, which is git-ignored.

## Tech stack

- Python 3.12 in a conda environment named `signal-tracker`
- `requests` and `python-dotenv` so far
- SQLite for storage (Phase 3), Streamlit for the UI (Phase 5)