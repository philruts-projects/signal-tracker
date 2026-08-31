# Backlog & parking lot

Things deliberately deferred so the core tracker ships first. Review after the
first working vertical slice (one company → one filing → one briefing) is running.

## North star

The watchlist is the product. The briefing is the value. Everything else is
enrichment. Any new data source must earn its place by making a briefing more
*actionable* — not just by adding more data.

## Data source enrichment — review after MVP

| Source | Signal it adds | Cost | Notes |
|---|---|---|---|
| Companies House **Streaming API** | Real-time filings (no polling) | Free | Same data, better plumbing. Natural Phase 3+ upgrade. |
| **The Gazette** (thegazette.co.uk) | Insolvency, administration, strike-off | Free API | Strongest distress-signal set. |
| **FCA Financial Services Register** | Regulatory authorisation status | Free | Relevant if watchlist is financial firms. |
| **Registry Trust** (CCJs) | County court judgments | Paid | Classic credit-risk signal. |
| Credit agencies (Creditsafe, Experian, D&B) | Commercial-grade risk scores | Paid | The "what incumbents charge for" comparison. |
| News (NewsAPI, GDELT) | M&A, leadership exits, layoffs | Free/paid | Noisy; adds context to a filing. |

## Also parked

- Product-journey / user-flow mapping — revisit once the slice reveals the real UX questions.
- Which filing types count as "significant" — refine against real data in Phase 3/6.