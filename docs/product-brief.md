# Product brief

**Date:** 1 September 2026
**Status:** Active. Supersedes `stakeholder-brief.md`, which was written under the earlier portfolio framing.

## The objective

Help a business identify customers or suppliers whose risk has materially changed, understand why, and decide where to act before the problem becomes obvious.

That is deliberately not "predict which company will collapse". The product does not need to forecast insolvency. It needs to surface a change early enough, and clearly enough, that someone can do something useful about it.

## What "useful" means

The actions open to a user are modest and specific: review or reduce a credit limit, stop extending further credit, contact the customer, ask for updated figures, adjust terms, escalate the account, line up an alternative supplier, or just watch more closely. Every one of those is a decision a human makes. The product points attention at the right company and hands over the evidence. It does not make the call.

The test for any feature is the same one: did this flag cause a better action, sooner? A flag that changes nothing is decoration.

## The user we build for first

Credit managers and controllers in mid-sized B2B organisations that don't have a sophisticated credit-risk platform.

The pain is frequent and measurable, the available actions are clear, exposure can be quantified in pounds, and preventing a single bad debt pays for the tool many times over. Smaller credit teams still monitor by hand, when they get to it. The product extends naturally into supplier risk later.

Two audiences are parked, not rejected:

| User | Their problem | Their decision |
|---|---|---|
| Procurement / supplier risk | A supplier may fail or become unreliable | Which suppliers need continuity action? |
| Account management | A customer relationship is deteriorating | Which customers do we contact or escalate? |

Serving all three at once produces something generic. We return to them once the first wedge works.

Credit analysts inside large organisations are explicitly not the target. They already have Experian, Creditsafe and D&B, and competing with those on predictive accuracy is a fight we lose.

## What success looks like for the user

"Instead of manually checking 100 companies, I open Signal Tracker and see the five whose circumstances have changed, why they've been flagged, how exposed we are, and what I should consider doing."

The output is a prioritised review queue. Not a dashboard, and not a score.

## What the product has to answer

What changed. Why it might matter. Whether it's one ambiguous event or a pattern. How confident we are. How exposed the organisation is. What to review or do next.

## The analytical outputs

**Review priority.** Routine, Watch, Serious, Critical or Unknown. This means priority for human review, never probability of collapse.

**Change since last review.** Stable, escalated, accumulating corroboration, improved, or carrying new information since the user last looked.

**Evidence dimensions.** Financial, payment behaviour, funding, governance, legal and regulatory, operational, context, and the user's own exposure. Confluence across independent dimensions is the signal. A single event rarely is.

**Explanation.** A short, evidence-backed account of what changed and why the combination matters, in plain English.

**Suggested review action.** A proportionate next step, never an automated credit decision.

## Where the differentiation might sit

Not Companies House data, which anyone can pull. Not AI summaries either, which are easy to reproduce.

The candidate proposition: Signal Tracker combines changes across public and user-owned data, explains the evidence plainly, and prioritises by how exposed the organisation actually is. The parts that could hold up are that it leads with what changed since the last review rather than a static score; that escalation needs several independent signals instead of one opaque number; that every flag links back to the record behind it; that prioritisation reflects money owed or operational dependency; that it says what to review rather than only what happened; that it runs on public and user-owned data before anything expensive; and that Unknown stays Unknown rather than being quietly converted into Routine.

None of that is proven. It is a hypothesis, and Track 1 of the discovery plan exists to test it against real users.

## The constraints we build inside

**The base rate is punishing.** Roughly 4.9 million companies sit on the effective register, and there were 23,938 insolvencies in 2025, about one in 190 a year. When failure is that rare, precision decides everything. An alert list that is even slightly noisy destroys trust, and the product dies with it.

**Exposure is the moat and the obstacle at once.** Nobody else can see what a user is owed, which is exactly why it differentiates, and it is also the hardest input to obtain. The first version takes a CSV of customer name, balance and days overdue, which exports from any ledger in about two minutes. Integrations come later, once the value is proven.

**Advisory framing is not optional.** Telling a paying customer that a named private company is heading for trouble carries defamation and liability risk. Everything is evidence plus a suggested review, never a verdict on a company's viability.

**Distribution is unsolved.** Mid-market credit managers are not in the existing network. Either we reach them warm or we find a channel that already holds them. That question is open and it may yet move the wedge.

## What this changes in the build

"What changed since you last looked" is the core promise, and the current code cannot deliver it. Company state is overwritten on every poll, so there is no history to compare against and no record of when a company was last reviewed. The observation history the external review raised, and that we parked as a nice-to-have, is now the spine of the product.
