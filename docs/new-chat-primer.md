# New-chat primer

Paste everything below the line into a fresh chat to start clean and aligned.

---

We're continuing my Signal Tracker project. Before anything else:

1. Read `CLAUDE.md` (project purpose, priorities, how I work, architecture).
2. Read `BACKLOG.md`, `eval/EVALUATION.md`, `docs/review-response.md` (an external review and what it fixed) and `docs/signal-tracker-data-sources.md` (research on candidate data sources) to get current.
3. Turn on the ADHD output style in `skills/i-have-adhd/SKILL.md` and keep it on for the whole chat — lead with the next action, number multi-step work, restate where we are each turn, give specific time estimates, no preamble or closing pleasantries.
4. Before any work: tell me which model tier fits this session (see "Model choice" in `CLAUDE.md`) and ask yes/no whether I want to switch. Repeat whenever the type of work changes.

**Priorities, in order:** (1) my learning and skill development, (2) staying engaged and enjoying it, (3) a working product — which may never ship. When a call is fuzzy, pick what teaches more and keeps momentum. Don't over-build or gold-plate. Build the smallest useful thing, look at the real data, then decide. I'm a commercial data leader, not a software engineer, so explain jargon and stage the work so I can do each step myself in VS Code.

**Where things stand:**
- Repo cloned at `C:\Users\phil\Documents\Signal-Tracker`, pushed to github.com/philruts-projects/signal-tracker. VS Code and Git are set up.
- Python: conda env `signal-tracker` (Python 3.12), dependencies installed.
- Keys: `CH_API_KEY` and `ANTHROPIC_API_KEY` are in `.env` (git-ignored). The Anthropic key must be workspace-scoped, not "all workspaces", or it's rejected.
- Database `data/signals.db` is built (git-ignored). 11 companies on the watchlist; the newest (Marks and Spencer, added via `add_company.py`) has not been baselined yet — the next `tracker.py` run will do that.
- The pipeline, rules-based risk verdict, Companies House enrichment (status, board churn, charges), Streamlit dashboard, a two-part evaluation, and unit tests are all built and working. Architecture is in `CLAUDE.md`.
- Rule thresholds live in `rules.csv` (not code) since 11 Sept; tune there, then `python eval_verdict.py` to measure. Tests hard-code a 3-charge cluster, so moving `charge_cluster_count` also fails a test by design.
- `add_company.py "name"` searches Companies House and appends the chosen company to `watchlist.csv` (free, one call).
- `probe_gazette.py` (free, no key) showed The Gazette beats Companies House by 4–14 days on all three collapse cases, zero false positives on healthy companies, but only at the formal event. Finding recorded in `BACKLOG.md`; not wired into `tracker.py` yet.
- **Don't run `tracker.py` or `run_eval.py` without asking** — they call paid APIs and change the database. `python eval_verdict.py` and `python tests/test_rules.py` are free and offline.

**Heads-up:** an earlier chat reframed this as a "commercial product in discovery" and started over-building. The updated `CLAUDE.md` resets that to learning-first. If a doc (e.g. `docs/product-brief.md`, `docs/discovery-plan.md`) pushes a product-first, discovery-gated framing, treat it as reference — the priorities above win.

**Likely next steps (I'll pick one, no need to do all):**
1. Wire The Gazette into `tracker.py` as a fourth fetch: the one source allowed to set Critical on its own, with a `gazette_ok` flag and a test. Watch for winding-up petitions (notice code 2450) as its only run-up signal.
2. Package it for show — README section on the Gazette and rules-table findings, refresh `docs/linkedin-post.md`, a short Loom.
3. FCA register (`probe_fca.py` exists, needs a free key in `.env`).
4. Move the churn threshold (3 resignations, hard-coded in `company_risk`) into `rules.csv` too.

Start by confirming you've read `CLAUDE.md` and the environment above, then ask me which of the next steps I want — or suggest a smaller first move if you see one.
