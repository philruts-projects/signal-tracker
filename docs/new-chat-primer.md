# New-chat primer

Paste everything below the line into a fresh chat to start clean and aligned.

---

We're continuing my Signal Tracker project. Before anything else:

1. Read `CLAUDE.md` (project purpose, priorities, how I work, architecture).
2. Read `BACKLOG.md` and `eval/EVALUATION.md` to get current.
3. Turn on the ADHD output style in `skills/i-have-adhd/SKILL.md` and keep it on for the whole chat — lead with the next action, number multi-step work, restate where we are each turn, give specific time estimates, no preamble or closing pleasantries.

**Priorities, in order:** (1) my learning and skill development, (2) staying engaged and enjoying it, (3) a working product — which may never ship. When a call is fuzzy, pick what teaches more and keeps momentum. Don't over-build or gold-plate. Build the smallest useful thing, look at the real data, then decide. I'm a commercial data leader, not a software engineer, so explain jargon and stage the work so I can do each step myself in VS Code.

**Where things stand:**
- Repo cloned at `C:\Users\phil\Documents\Signal-Tracker`, pushed to github.com/philruts-projects/signal-tracker. VS Code and Git are set up.
- Python: conda env `signal-tracker` (Python 3.12), dependencies installed.
- Keys: `CH_API_KEY` and `ANTHROPIC_API_KEY` are in `.env` (git-ignored). The Anthropic key must be workspace-scoped, not "all workspaces", or it's rejected.
- Database `data/signals.db` is built (git-ignored), 9 companies on the watchlist.
- The pipeline, rules-based risk verdict, Companies House enrichment (status, board churn, charges), Streamlit dashboard, a two-part evaluation, and unit tests are all built and working. Architecture is in `CLAUDE.md`.
- **Don't run `tracker.py` or `run_eval.py` without asking** — they call paid APIs and change the database. `python eval_verdict.py` and `python tests/test_rules.py` are free and offline.

**Heads-up:** an earlier chat reframed this as a "commercial product in discovery" and started over-building. The updated `CLAUDE.md` resets that to learning-first. If a doc (e.g. `docs/product-brief.md`, `docs/discovery-plan.md`) pushes a product-first, discovery-gated framing, treat it as reference — the priorities above win.

**Likely next steps (I'll pick one, no need to do all):**
1. Add a new data source and see what it adds — the FCA register (a `probe_fca.py` exists) or the Gazette.
2. Lift the rules' thresholds out of code into an editable table I can tune.
3. Add search-to-add so companies go on the watchlist without editing the CSV by hand.
4. Package it for show — README polish, a LinkedIn post, a short Loom.

Start by confirming you've read `CLAUDE.md` and the environment above, then ask me which of the next steps I want — or suggest a smaller first move if you see one.
