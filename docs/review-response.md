# Response to the external review — decisions & staged plan

**Date:** 1 September 2026
**Reviewed document:** `docs/signal-tracker-external-review.md`
**Purpose:** Record which findings I accept, which I accept with caveats, and which I'm
setting aside — and turn the accepted ones into an ordered, do-it-yourself build plan.
This doc is deliberately a decision record, not just a to-do list: at interview, *"here's
what an independent model told me and here's what I did and didn't change, with reasons"*
is a stronger story than the fixes alone.

---

## 1. How I triaged the review

I checked the review's top findings against the actual code before accepting anything. It
held up unusually well — its claims are specific and correct, not generic. Three buckets:

**Accept and fix now (the integrity gaps).** Findings 1, 2, 4, 8. These are places where the
code does something different from what the product claims, and a hiring manager reading the
source would spot them. Small, self-contained, each a clean "found it / fixed it" story.

**Accept, with context — worth stating your own case at interview.** Findings 3, 5, 9, 10.
All legitimate, but a couple slightly under-credit how honest the existing write-up already
is, and one (3) is a real methodological hole whose *practical* effect on the numbers is
tiny. Fix the mechanics; keep the perspective.

**Accept in principle, not this slice.** Findings 6, 7 (partly). Genuine, lower urgency —
audit-trail history is a bigger build; the founder-rule substring bug (7) is quick and I've
folded its quick half into the plan.

**Where the review is slightly wrong (state this confidently).** It lists *"nothing gets
flagged twice"* as an overclaim — but it isn't. You dedupe on `transaction_id`; that claim
is true. Worth knowing so you don't over-correct a thing that's actually fine.

---

## 2. What changed in the priority order

The review's most useful contribution isn't any single fix — it's that it quietly re-ordered
the backlog. Two of the three things we were about to start (FCA register, drill-down
grouping) *add capability*; the review argues, correctly, that adding surface area on top of
Findings 1/2/4 widens the gap between what the dashboard claims and what the code does, which
makes the portfolio *weaker*. So:

1. **Integrity fixes first** (this plan, Steps 1–5). Mostly code you already have.
2. **Then drill-down grouping** — which turns out to be the natural UI expression of Finding 1
   ("company risk should reflect filing clusters"), so it and the Finding-1 fix are nearly the
   same piece of work. We'll do the data/logic half here and the grouped-UI half as its own slice.
3. **FCA register last, if at all.** The review's own source table ranks FCA 6th and flags that
   its reusable data extract is expensive (~£4.5k/yr) and only covers regulated firms. Good to
   *mention* as a considered-and-deferred decision; not the best next build.
4. **LinkedIn post after the fixes** — because the post then becomes *"an independent model
   reviewed my project; here's what it found and what I shipped in response,"* which is a far
   better narrative for an AI-enablement role than a feature tour. The critique-and-response
   is the content.

---

## 3. The staged plan

Each step is a self-contained slice: a clear goal, VS Code-centric actions, a **checkpoint**
(how you know it's done), and roughly how long. Do them in order, worst-first. Commit after
each one from the Source Control panel so every fix is its own reviewable change — that commit
history is itself part of the portfolio story.

### Step 0 — Clean base (do this before anything else)

You currently have a pile of uncommitted changes in Source Control (`tracker.py`,
`briefing.py`, `CLAUDE.md`, the eval results, the new `docs/` files, and more). New work should
land on a clean base so each fix is legible.

- In VS Code, open the **Source Control** panel (the branch-y icon in the left rail).
- Read the diff of each changed file (click it to see the before/after side by side). Nothing
  here should be a surprise — but confirm no secret (`.env`) is staged. `.env` is git-ignored,
  so it shouldn't appear; if it does, stop and tell me.
- Stage everything, write a message like `Add external review + response; misc doc updates`,
  and commit. Optionally push.

**Checkpoint:** Source Control shows no pending changes. `git log --oneline -1` shows your new commit.

*Jargon:* "staging" = choosing which changes go into the next commit; "commit" = a saved
snapshot with a message; "push" = upload your commits to GitHub.

---

### Step 1 — Company risk must reflect filing severity  *(Finding 1 — the important one)*

**Problem.** `app.py` computes each company's headline risk from registered status, insolvency
history, overdue accounts and churn only. The filing verdicts (your Serious/Critical counts)
are used just as sort tie-breakers and never touch the headline or the "Need attention" count.
So a freshly-detected Serious charge cluster can leave a company showing green Routine, sorted
below a yellow Watch company. This defeats the cluster detection you're proudest of.

**Fix (smallest version).** Introduce a `portfolio_company_risk()` in `severity.py` that takes
the existing status-based risk **and** the company's recent filing verdicts, and returns the
higher of the two (with the reason). Then call it from `app.py` in place of `company_risk()`,
and feed the same result into the "Need attention" count.

**VS Code steps.**
1. In `severity.py`, add a function alongside `company_risk()`:
   - inputs: the current status-based risk (call the existing function), plus counts of the
     company's recent Serious/Critical filings within a stated window (e.g. last 180 days).
   - rule (first cut): if there's a Critical filing in-window → at least Serious; if there are
     Serious filings in-window → at least Watch (tune later). Return both the level and a short
     reason string like `"2 Serious filings in last 180d"`.
   - keep it pure and explainable — no model, just `max()` over the two severities.
2. In `app.py`, where the per-company row is built, replace the `company_risk(...)` call with
   `portfolio_company_risk(...)`, passing the filings you already load for that company.
3. Recompute `need_attention` from the *new* risk field (it already keys off `posture["risk"]`,
   so once the field reflects filings, the count fixes itself).
4. Store the reason string on the row and show it as a small caption on the card (e.g.
   *"Elevated by filing signals: 2 Serious in last 180d"*) so the escalation is explained, not
   mysterious.

**Checkpoint.** In the running dashboard, a company with an `active` status but a Serious
filing on record now shows amber/red, appears in "Need attention," and sorts above healthy
companies — with a caption saying why. (Greensill in your data is a good manual test case.)

*Why the small version first:* it's the vertical slice — get filings influencing the headline
at all, then refine the exact thresholds against real cases. Don't build the full
`portfolio_company_risk()` with time-windowed weighting the review sketches until this works.

---

### Step 2 — Missing data must not read as healthy  *(Finding 2)*

**Problem.** In `tracker.py`, a failed profile/officers/charges fetch is caught and turned into
`{}` or zero-filled dicts. Those zeros flow into the risk logic as *reassuring*. A timeout or a
429 rate-limit (ordinary at 600 requests / 5 min) can make a risky company look calm.

**Fix (prototype-appropriate).** Distinguish **Unknown** from **Routine**. You don't need the
full fetch-status audit table the review describes yet — just stop laundering failures into zeros.

**VS Code steps.**
1. In `tracker.py`, when a fetch fails, record the failure rather than a zero: store the status
   as `NULL`/`"unknown"` and add a per-source `*_ok` flag (e.g. `profile_ok`, `officers_ok`,
   `charges_ok`) on the `companies` row. (Add the columns to the `CREATE TABLE`; a fresh DB is
   fine for a prototype, or add them with a one-off `ALTER TABLE`.)
2. In `severity.py`, if status is unknown, return a distinct `"Unknown"` level — never Routine.
3. In `app.py`, give `Unknown` its own icon (e.g. ⚪) and its own bucket, shown *separately*
   from healthy companies, with a caption like *"Data unavailable — last fetch failed."*
4. (Optional, nice) add a single bounded retry on transient errors in `ch_get()`, and treat
   HTTP 429 explicitly with a short wait.

**Checkpoint.** Temporarily point the API base URL at a bad host (or unplug the network) and
run `tracker.py`: the affected companies show ⚪ Unknown, *not* green Routine. Put it back.

---

### Step 3 — No briefing is silently lost  *(Finding 4)*

**Problem.** You `INSERT` every new filing (briefing `NULL`) first, then brief only while the
per-run cap lasts. Next run those transaction IDs aren't "new," so the un-briefed ones are
never revisited. And processing is in watchlist order, so a Routine filing can spend the budget
a Critical one needed.

**Fix.** Treat briefing as a small persistent queue keyed off "briefing IS NULL," and process
worst-first.

**VS Code steps.**
1. Split the loop in `tracker.py`: first pass detects/stores all new filings (as now); second
   pass **queries the DB for any filing where `briefing IS NULL`**, orders them
   Critical→Serious→Watch→Routine and by date, and briefs up to the cap.
   - This one change fixes both halves: leftovers from a previous run are picked up because
     they're still `NULL`, and severity ordering means the budget goes to what matters.
2. (Optional) add a `briefing_status` column (`pending`/`done`/`failed`) and a small attempt
   counter so a genuinely failing briefing doesn't retry forever. The `IS NULL` approach works
   without this; add it only if you want the extra robustness on show.

**Checkpoint.** Set `MAX_BRIEFINGS_PER_RUN = 2`, simulate 4+ new filings across a couple of
companies (there's `simulate_new_filing.py` in the repo), run twice: after the second run every
filing has a briefing, and the Critical/Serious ones were briefed before the Routine ones.

---

### Step 4 — Reconcile the accounting-date rule with its docs  *(Finding 8)*

**Problem.** Your `EVALUATION.md` narrative says LC&F's third accounting-reference-date change
is what triggers Serious. But `pattern_severity()` counts the current filing plus others and
fires at a total of 2 (its own comment says "this one plus 1+ others") — i.e. it actually fires
on the **second** change. Code and docs disagree. Also the window is `18*30` days, not real months.

**Fix.** Decide the rule you actually want, encode it unambiguously, and make the docs match.

**VS Code steps.**
1. Choose: is the trigger the *second* change in ~18 months, or the *third*? (Defensible either
   way — a second change inside 18 months is already unusual. My lean: keep the more sensitive
   second-change trigger, but then **fix the docs to say "second," not "third."** Correct, honest,
   and it still gets LC&F right.)
2. Make the threshold explicit in `pattern_severity()` — a named constant like
   `ARD_CHANGES_TO_ELEVATE = 2` and a comment stating exactly what's being counted (including
   whether the current filing is counted).
3. Use real month arithmetic for the window instead of `18*30` (a small helper, or
   `dateutil.relativedelta`).
4. Update `EVALUATION.md` and any README line to state the actual rule.

**Checkpoint.** Re-run `python eval_verdict.py`: still 10/12, LC&F still Serious. The rule's
constant and the doc now say the same number. Add a tiny inline test (first/second/third change)
if you want to show test discipline.

---

### Step 5 — Make the verdict eval reproducible & leak-free  *(Findings 3 & 5)*

**Problem (two linked).**
- *Leakage (3):* the charge-cluster rule uses `abs(other_date - filing_date) <= 30`, and
  `eval_verdict.py` hands it **all** stored filings — including ones dated *after* the filing
  being scored. Real-world polling only ever sees past+present, so the historical eval can flatter
  itself with future filings. (Practical impact is small — it touches the one Carillion charge case
  — but it's a real methodological hole.)
- *Reproducibility (5):* the eval reads your local `data/signals.db`, which is git-ignored, so
  nobody can re-run your headline number from a clean clone.

**Fix.**
1. In the cluster rule (or in how the eval calls it), only count context filings with
   `date <= evaluated_filing.date`. Cleanest: make `pattern_severity()` window backward-only for
   charges too (the ARD rule already is), or pass an `as_of_date` the eval sets to the filing's date.
2. Commit a small **fixture**: export just the filings the 12 eval cases need into a committed
   CSV/JSON under `eval/`, and have `eval_verdict.py` read that instead of the private DB. Now a
   fresh clone reproduces 10/12 with no API key and no local database.
3. Rename the claim in `EVALUATION.md`: call it a **"12-case rules regression suite,"** not
   "accuracy." Keep your existing honest paragraph about the two Carillion misses being a data
   ceiling — that's already the right tone; the review just wants the headline word changed.

**Checkpoint.** `git stash` your DB (or clone fresh), run `python eval_verdict.py`, still get
10/12 from the committed fixture alone. Adding a *later-dated* charge to a fixture no longer
changes an earlier filing's verdict.

---

### Step 6 — Drill-down grouping (the original task, now on a solid base)

With Step 1 done, the company headline reflects filing clusters. This step makes the cluster
*visible* as one thing instead of a flat list — the confluence the eval says is the real signal.

- Group a company's notable filings in `app.py` by pattern: a "burst of charges" block, a
  "repeated accounting-date changes" block, a "governance changes" block, each with a one-line
  summary and the individual filings folded underneath.
- Lead each company card with the *grouped* story ("5 charges in 8 days") rather than the single
  latest filing.

We'll spec this properly as its own slice when we get here — it's a UI design task, and I'll
show you a couple of layout options first.

**Checkpoint.** Carillion's card shows "Cluster: 5 charges registered within one week" as a
single grouped signal, expandable to the five filings.

---

### Step 7 — README / caption honesty pass  *(Finding 10)*

Small but high-leverage, because it's the contradiction a code-reading reviewer notices first.

- README's "how well it works" still says the tool reads each filing alone and can't see
  clusters — untrue now that `pattern_severity()` exists (the *briefing* is still single-filing;
  say that precisely instead).
- Soften causal language to match what a filing actually proves: *"registered charge"* /
  *"charge marked satisfied"* rather than *"fresh secured borrowing"* / *"debt repaid"*; describe
  the founder rule as *"possible eponymous-officer departure"* (and, quick win from Finding 7,
  tighten `_is_founder()` from a substring test to a whole-word match so "King" stops matching
  "Kingfisher").
- Frame the headline as *"public-record monitoring and triage,"* and state that company risk is a
  heuristic priority, not a probability of insolvency.

**Checkpoint.** A reader diffing README claims against the code finds no statement the code
contradicts.

---

## 4. Explicitly parked (accepted, but not now — and say so at interview)

- **Full audit/history tables** (Finding 6): `company_observations`, `poll_runs`, rule
  provenance. Genuinely valuable for a "what changed since last time" view, but a real build.
  Park with a note; it pairs naturally with the streaming-API upgrade already in `BACKLOG.md`.
- **Population-based evaluation** (review §4): distressed vs matched-healthy controls, lead-time
  and false-alert metrics. This is the *right* long-term answer and a great thing to describe as
  "where I'd take the evaluation next," but it needs a dataset you don't have yet. Describe it;
  don't fake it.
- **FCA register / new sources:** deferred per §2 above.

---

## 5. Suggested commit sequence

One commit per step keeps the story legible:

1. `Add external review response and staged plan` (this doc)
2. `Company risk now reflects filing severity, not just status` (Step 1)
3. `Distinguish Unknown from Routine; stop treating fetch failures as healthy` (Step 2)
4. `Persistent briefing queue, worst-first; no filing loses its briefing` (Step 3)
5. `Reconcile accounting-date rule with docs; explicit threshold + real months` (Step 4)
6. `Reproducible, leak-free verdict eval with committed fixtures` (Step 5)
7. `Grouped cluster view in dashboard` (Step 6)
8. `Honesty pass: README/captions match implementation` (Step 7)

That sequence, read top to bottom, *is* the LinkedIn post: a reviewer pushed hard, here's the
seven-commit response.
