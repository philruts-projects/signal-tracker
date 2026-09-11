# Discovery plan

**Date:** 1 September 2026
**Purpose:** Find out whether the proposition in `product-brief.md` is real, before building more of it.

Two tracks run in parallel. One asks whether the problem is real and worth paying for. The other asks whether available data can actually see trouble coming in time to act on it. Both have to come back yes.

## Track 1: user discovery

Target: five people working in credit control, finance or supplier management at mid-sized B2B organisations.

### The interview

Open with how they work now, not with the idea. The point is to hear the problem in their words before contaminating it with ours.

1. How do you monitor customers or suppliers today?
2. What prompts a credit review?
3. What do you check, and how often?
4. How many companies could you realistically investigate in a week?
5. What gets missed?
6. Which events have caught you out before? Talk me through the last one.
7. When risk goes up, what can you actually do about it?
8. What would earlier warning have been worth on that last surprise?
9. What tools do you use now, and what do you pay for them?
10. What do you distrust about the scores you already get?
11. What would stop you using something like this, even if it worked?

The last two earn their place. Question 9 tells us whether there is money here at all. Question 11 surfaces the objection that kills adoption, which is usually trust or effort rather than accuracy.

### The prize

Ask one of them for an anonymised historical sales ledger: customer, balance, days overdue, across 18 months or more. That dataset is worth more to this product than any additional public source, because it contains the outcome we actually care about. See the note on outcomes below.

## Track 2: analytical discovery

The question: can public-record signals separate a company heading for trouble from ordinary corporate activity, early enough and cleanly enough to act on?

### On the outcome, honestly

The outcome that matters to a credit manager is not insolvency. It is "this customer stopped paying, went materially late, or had to be written off". Bad debt is far more common than formal failure, and it is the thing they are protecting against.

We cannot measure that yet, because payment default lives in a user's ledger and we don't have one. So the first pass uses formal insolvency, administration or liquidation as an explicit proxy, and the write-up labels it as a proxy rather than pretending it is the target. A real ledger from Track 1 replaces the proxy with the real thing.

### Cohort, first cut

Start small and cheap: thirty companies that entered insolvency, ninety that didn't, matched on sector, rough size, age and period. If there is separation, scale to the fuller design of 50 to 100 failures against 200 to 500 controls.

The outcome date comes from the first insolvency-related filing in the company's history, which also starts the clock for lead time.

Every observation contains only what was knowable at that date. Signals are evaluated at 3, 6, 9 and 12 months before the outcome date, and at equivalent dates for controls.

### Signals in the first cut

Only what we can reconstruct point-in-time, for free:

- accounts overdue, and time since accounts were last filed
- charge registrations, and clusters of them
- accounting reference date changes, and repeats
- director departures, short-tenure exits, PSC changes
- registered address changes
- registered status and Gazette notices
- payment practices reporting, downloadable historically for large filers

Excluded from the first cut, deliberately: CCJs, not obtainable historically at cohort scale without paying; news and M&A context, too messy to reconstruct cleanly; and filed-account financials, which need iXBRL parsing and are a project in their own right. Financials are the most valuable of those three and the obvious candidate for cut two.

### What each signal has to answer

How often does it appear among companies that failed, and among those that didn't? How far ahead of the outcome does it show up? Does it survive controlling for size and sector? Is it useful alone, or only in combination? How many false alerts does it throw? And is it published early enough to act on, or does it only arrive once everybody already knows?

Combinations are where the interesting answer probably lives. A director departure alone is weak. Overdue accounts plus repeated charges may be considerably stronger. Leadership churn alongside acquisition news is probably not distress at all.

### Metrics, and the correction that matters

Precision and recall at Serious or above, false alerts per 100 monitored companies per month, median warning lead time, and the share of failures caught at 3, 6 and 12 months.

One trap sits in wait. A cohort of thirty failures against ninety controls carries a failure rate of 25 percent, while reality is about half a percent. Precision measured on that sample is inflated by roughly the ratio between the two prevalences, somewhere near fifty times. Every headline number gets re-weighted to the true base rate before it goes into the write-up, or the result disintegrates the first time it meets a real book of companies.

The best model is not the one with the highest recall. Something that flags 60 companies in every 100 each month is useless whatever it catches.

## The decision gates

Three questions. A no on any of them means changing the proposition rather than adding features.

1. Is there a real, repeated, expensive problem here?
2. Can accessible data give useful warning before the outcome?
3. Can we cut the review workload enough to make that warning actionable?

## Next steps

**Phil**

- Find the five interviewees. Any route in: network, ex-colleagues, LinkedIn, or an accountant or invoice financier who already serves credit teams.
- Run the interviews, notes into `docs/discovery/` as you go.
- Ask one of them for the anonymised ledger.
- Commit the documentation changes currently sitting in Source Control.

**Claude**

- Build the cohort from Companies House and reconstruct the point-in-time signals.
- Run the separation, lead-time and false-alert analysis, base-rate corrected.
- Write the findings up honestly, including the outcome where nothing separates.
- Then, and only if the signals hold, build the observation history that makes "what changed since you last looked" possible.

**Parked on purpose**

FCA register integration, the wider data-source roadmap, and any front-end rebuild. None of it matters until discovery says the proposition is real.
