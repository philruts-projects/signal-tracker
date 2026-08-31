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

## Companies House — richer data we already touch or can reach (same free API/key)

Discovered while reviewing the stored data. Highest value first.

- **Capture `description_values` (do this early).** The API returns a `description_values`
  object on each filing (e.g. `officer_name`, `termination_date`, share amounts) that we
  currently discard — we only store the `description` code. Capturing it enables (a) a
  deterministic human-readable label via Companies House's own template file, and (b) far
  more specific briefings (name the actual director/date instead of "a director").
- **Readable-description lookup.** `description` codes are keys into Companies House's
  published enumeration `filing_history_descriptions.yml` (repo: `companieshouse/api-enumerations`),
  which maps e.g. `termination-director-company-with-name-termination-date` →
  "Termination of appointment of {officer_name} as a director on {termination_date}".
  `constants.yml` in the same repo lists `category` values. Vendor these as a local lookup,
  with a prettify fallback for codes not in the file (some SH/CS codes aren't).
- **Company profile** (`/company/{number}`): `company_status` (active/dissolved/liquidation/
  administration), `has_insolvency_history`, `has_charges`, accounts-overdue flags, `sic_codes`,
  `previous_company_names`. For a credit/risk audience this is arguably higher-value than
  filing history — genuine distress shows up here.
- **Charges** (`/charges`): secured lending / mortgages — direct credit signal.
- **Insolvency** (`/insolvency`), **Officers** (`/officers`), **PSC**
  (`/persons-with-significant-control`, ownership).
- Other discarded filing fields: `action_date`, `subcategory`, `links` (to the actual
  filing document via the Document API), `pages`, `paper_filed`.

## Known limitations / failure modes (for the Phase 6 write-up)

- **Uneven look-back window.** We fetch the latest 100 filings per company
  (`items_per_page=100`), so time-depth varies by how often a company files — ~3 months for
  a heavy filer (L&G), years for a light one (Admiral). A company filing >100 documents
  between two polls would overflow the window; in practice this never happens at any sane
  polling cadence, so the risk is near-zero — but it's a deliberate trade-off worth stating.
  Chosen because change detection only needs the recent page (new filings arrive at the top).

## Data-model notes (learned, keep in mind)

- Every company has a permanent unique 8-char **company number**; names are not unique over
  time and can change (see `previous_company_names`). **Always key on number, never name.**
  Subsidiaries are separate entities with their own numbers (Aviva plc `02468686` vs Aviva
  Insurance Ltd `SC002116`).
- Source-of-truth fields (from the API): `transaction_id`, `type`, `category`, `date`,
  `description`. Derived-by-us: `first_seen`, `briefing`.

## Signal heuristics & the pattern-detection gap (from domain review)

The current tool briefs filings **one at a time**. Real distress is a **cluster**, not a
single filing — the biggest limitation and the clearest next feature. Evidence from the
data (all filings the tracker would have caught):

- **Carillion (collapsed Jan 2018):** CFO out (Jan '17), CEO out (Jul '17), replacement CFO
  gone within 8 months, then 5 new charges in one week (Oct '17). The *cluster* is the signal.
- **LC&F (collapsed Jan 2019):** accounting reference date changed 3× in 15 months. One change
  is routine; the *repetition* is the tell — invisible to a single-filing view.
- **Greensill (collapsed Mar 2021):** secured charges through 2020 + governance churn.

Heuristics to encode later (severity is contextual — build rules from these):
- **Founder / named-founder departure → always elevate.** Rarely quiet; often trails a PE deal,
  funding round, or strategy/performance rupture.
- **Finance-leadership churn (CFO exit, short-tenured replacement) → elevate.** Revolving-door
  finance is a classic pre-failure marker.
- **Cluster of new charges in a short window → elevate.** Scrambling for secured finance.
- **Repeated accounting-reference-date changes → elevate.** Obfuscation / delaying accounts.
- **Capital events (allotment/cancellation) → threshold rule**, e.g. flag if the figure is
  material vs revenue / market cap; otherwise inform-only. Briefings should also *explain the
  mechanism* (what a share cancellation is and why firms do it).

Framing: **the value is early warning.** Aftermath filings (liquidation disclaimers,
administration progress reports) are post-mortem — correctly labelling them is near-worthless.
The eval is built around the run-up, not the collapse.

## Also parked

- Product-journey / user-flow mapping — revisit once the slice reveals the real UX questions.
- Which filing types count as "significant" — refine against real data in Phase 3/6.