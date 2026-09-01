# Signal Tracker — External Review

**Review date:** 1 September 2026  
**Repository:** [philruts-projects/signal-tracker](https://github.com/philruts-projects/signal-tracker)

## 1. Executive verdict

Signal Tracker is a credible portfolio project with a sound central idea, but its current interface overstates what the underlying system actually does.

The strongest decision is separating deterministic verdicts from LLM-written explanations. That is appropriate for an explainable triage product. The weakest part is not the LLM: it is the disconnect between collection, filing severity and company-level presentation.

Most seriously, the dashboard calculates each company’s headline risk without using its filing verdicts. A company can therefore have a newly detected Serious filing and still appear as Routine and fall to the bottom of the watchlist. In addition, failed API calls are silently converted into zero or missing values, which the risk logic interprets as reassuring. Those two defects undermine the central promise that the tool reliably tells users what needs attention.

The reported 10/12 evaluation is a useful regression demonstration, not evidence of early-warning performance. Its cases were curated, labels were assigned by the builder, the historical database is not packaged reproducibly, and the charge-cluster rule can see filings after the historical event being assessed. The test therefore contains selection risk and possible point-in-time leakage.

The project is still worthwhile. It demonstrates commercial problem selection, API integration, deterministic rules, storage, an LLM with a constrained role and an attempt at evaluation. But it should be presented as a prototype for prioritising public filing signals—not yet as a system that predicts corporate distress.

The next two weeks should be spent fixing reliability, time integrity, company-level aggregation and evaluation—not adding machine learning or multiple noisy sources.

## 2. Scores

| Standard | Score | What prevents a higher score |
|---|---:|---|
| Portfolio credibility | **7/10** | Strong concept and architectural judgement, but material code/UI contradictions and an overclaimed evaluation weaken the story |
| Operational readiness | **2.5/10** | Silent data failures, incomplete alert aggregation, no state history, permanently skipped briefings, weak evaluation and no operational monitoring |

## 3. Ten findings ranked by seriousness

### 1. Serious filings do not determine the dashboard’s company risk

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** In [`app.py`](https://github.com/philruts-projects/signal-tracker/blob/main/app.py), `company_risk()` is called using status, insolvency history, overdue accounts and churn. The filing-level `severity` values are counted afterwards but never passed into the company-risk calculation. [`severity.py`](https://github.com/philruts-projects/signal-tracker/blob/main/severity.py) confirms that `company_risk()` knows nothing about filings, charges or filing patterns.
- **Consequence:** A newly detected Serious charge cluster or accounting-date pattern can leave the company headline at Routine. It will not contribute to “Need attention” and may be sorted beneath less important companies. This contradicts the product’s central workflow.
- **Action:** Introduce `portfolio_company_risk()` that combines current registered status, active company signals, recent filing verdicts within explicit time windows, corroborating patterns and data-quality state. Store both `signal_severity` and the reason it influenced the current company posture.

### 2. API failures masquerade as healthy data

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** In [`tracker.py`](https://github.com/philruts-projects/signal-tracker/blob/main/tracker.py), exceptions fetching profiles, officers and charges are caught broadly. Profiles become `{}`; officers and charges become zero-filled dictionaries. In `company_risk()`, absent status and zero signals ultimately return Routine.
- **Consequence:** An outage, timeout, authentication failure or rate limit can make a risky company look healthy. Companies House allows 600 requests per five minutes and returns `429` when that limit is exceeded, so this is an ordinary operational condition, not a theoretical edge case. See the [Companies House developer guidelines](https://developer.company-information.service.gov.uk/developer-guidelines).
- **Action:** Never convert failed retrieval into valid zero data. Store `fetch_status`, `last_attempted_at`, `last_successful_at`, HTTP status/error type, source timestamp and whether displayed data is stale. Show Unknown/Data unavailable separately from Routine. Add bounded retries for transient failures and explicit handling for `429`, `404` and authentication errors.

### 3. The evaluation is not point-in-time safe

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** In [`severity.py`](https://github.com/philruts-projects/signal-tracker/blob/main/severity.py), the charge-cluster rule counts filings within `abs(other_date - filing_date) <= 30`. When evaluating a historical filing against today’s database, that includes filings occurring after the event being scored. [`eval_verdict.py`](https://github.com/philruts-projects/signal-tracker/blob/main/eval_verdict.py) loads all currently stored filings for the company and supplies them to the rule.
- **Consequence:** Historical performance may benefit from future information. A supposed early warning can be credited because of an event that had not happened yet.
- **Action:** Construct the historical feature set as of an explicit `as_of_date`. Every contextual query must require `other_filing.date <= evaluated_filing.date`. For same-day records, use a deterministic tie-breaker such as `first_seen`, transaction order or “known by end of day.” Record the exact snapshot used.

### 4. Briefings skipped by the cost cap are lost permanently

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** [`tracker.py`](https://github.com/philruts-projects/signal-tracker/blob/main/tracker.py) inserts every new filing before generating briefings. Once `MAX_BRIEFINGS_PER_RUN` reaches zero, later filings retain `briefing = NULL`. On the next run, their transaction IDs are already stored, so they are no longer new and are never reconsidered.
- **Consequence:** A filing can permanently lose its briefing simply because it was sixth in one polling run. Processing follows watchlist/API order rather than severity, so Routine filings may also consume the budget before Critical ones.
- **Action:** Treat briefing generation as a persistent queue. Store `briefing_status = pending/completed/failed`, process Critical and Serious first, retry failures with a capped attempt count, and make the cap apply to attempts rather than eligibility.

### 5. The 10/12 result is a regression check, not an accuracy claim

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** [`eval/eval_set.csv`](https://github.com/philruts-projects/signal-tracker/blob/main/eval/eval_set.csv) contains 12 deliberately selected cases, including famous failures and five routine/healthy examples. The labels were assigned by the project builder. Some labels use information absent from the filing, such as the Carillion officers’ executive roles and the assertion that Direct Line was healthy. [`eval_verdict.py`](https://github.com/philruts-projects/signal-tracker/blob/main/eval_verdict.py) depends on a local SQLite database excluded by `.gitignore`, rather than committed point-in-time fixtures.
- **Consequence:** “83% accuracy” sounds statistically meaningful when it is not. The selection process favours known examples and does not measure alert prevalence among ordinary companies.
- **Action:** Rename this the “12-case rules regression suite.” Commit sanitised source fixtures so another person can run it without reconstructing the database. Add a blind-labelled, population-based evaluation before using performance language.

### 6. The product has no historical company state or auditable decision record

- **Classification:** High value
- **Confidence:** High
- **Evidence:** [`tracker.py`](https://github.com/philruts-projects/signal-tracker/blob/main/tracker.py) uses `INSERT OR REPLACE` on one `companies` row per company. Previous status, overdue state, churn summary and charge summary are overwritten. Filing rows store a severity but not rule version, matched rule, explanation or input snapshot.
- **Consequence:** The UI cannot honestly show trends or “what changed since I last looked.” A verdict changed by later code cannot be reconstructed. This is a material weakness for an explainability claim.
- **Action:** Add `company_observations`, `poll_runs`, `source_fetches`, `signal_events`, `rule_id`, `rule_version`, `evaluated_at`, `as_of_date` and `evidence_json`. Rules can remain in Python for now. Reproducible rule provenance matters more than an editable rule-management screen.

### 7. Some rules encode unsupported causal claims

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** In [`severity.py`](https://github.com/philruts-projects/signal-tracker/blob/main/severity.py), `_is_founder()` treats a departing officer as a founder when their surname, longer than three characters, occurs anywhere in the company name. Mortgage-category filings are described in the code and [`lookups.py`](https://github.com/philruts-projects/signal-tracker/blob/main/lookups.py) as “fresh secured borrowing,” while a satisfied charge is described as “debt repaid.” These conclusions do not necessarily follow from the filing alone.
- **Consequence:** False founder identification is easy, especially with common surnames or word fragments. A charge registration confirms security was registered, not the live debt amount or necessarily deteriorating creditworthiness. Satisfaction does not always mean the exposure has simply been repaid.
- **Action:** Remove automatic Serious classification from the surname rule. Rename it `possible_eponymous_officer_departure` and make it Watch pending corroboration. Use “registered charge” and “charge marked satisfied” throughout. Cite the source rather than asserting motive.

### 8. The accounting-date rule does not match its documentation

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** The narrative says “third or later change,” but `pattern_severity()` counts the current filing plus other filings and escalates when the total is at least two. Its comment explicitly says “this one plus 1+ others.” The 18-month window is approximated as `18 * 30` days.
- **Consequence:** The implemented threshold is effectively the second change, not the third. This damages trust in the claimed evaluation and makes the rule harder to explain.
- **Action:** Decide the actual rule and encode it unambiguously. Use true calendar-month arithmetic and test the first, second, third and boundary cases.

### 9. The LLM evaluation is structurally useful but too self-referential

- **Classification:** High value
- **Confidence:** High
- **Evidence:** [`run_eval.py`](https://github.com/philruts-projects/signal-tracker/blob/main/run_eval.py) uses Claude models to generate both variants and another Claude model to judge them. It runs each candidate once, averages ordinal 1–5 scores and loads stored severity rather than recalculating it from the current rules.
- **Consequence:** Model-family bias, run variance and stale stored verdicts can affect conclusions. “Near-zero hallucinations” from twelve cases and one judge run is weak evidence.
- **Action:** Keep model judging as a cheap regression test, but recompute verdicts, randomise and blind candidate order, repeat generation, use deterministic factual checks where possible, manually review a stratified subset and report distributions rather than only means.

### 10. The README and interface overclaim the implementation

- **Classification:** Must fix
- **Confidence:** High
- **Evidence:** [`README.md`](https://github.com/philruts-projects/signal-tracker/blob/main/README.md) says a new charge means fresh secured borrowing, refers to founder departure as established fact, says nothing gets flagged twice, and claims the tool “scores how worried you should be.” It also says the tool reads filings alone and cannot detect clusters even though cluster rules now exist. The Streamlit caption says companies are “heading for trouble.”
- **Consequence:** A hiring manager who reads the code will notice the contradictions. That hurts portfolio credibility more than openly describing a limited prototype.
- **Action:** Rewrite the proposition around “public-record monitoring and triage.” State that current company risk is heuristic, not a probability of insolvency. Update documentation whenever behaviour changes.

## 4. Evaluation redesign

### Target outcome

Do not begin with four severity labels. First define the event the system is intended to anticipate.

Recommended v2 target:

> Identify companies that warrant analyst review because public information indicates a materially increased risk of insolvency, inability to pay suppliers, or operational disruption within the next 6–12 months.

The verdict should initially mean **review priority**, not predicted failure probability.

### Unit of evaluation

Use one observation per company per weekly or monthly snapshot—not one hand-picked filing. This represents the user’s real decision: “Which companies in my portfolio need attention now?”

### Observation and prediction windows

- Observation window: all information publicly available up to the snapshot date.
- Feature windows: 30, 90, 180 and 365 days, plus longer financial trends where available.
- Prediction horizons: 3, 6 and 12 months.
- Outcomes:
  - insolvency, administration or liquidation;
  - compulsory strike-off or winding-up event;
  - material worsening in payment behaviour or CCJs when those sources become available;
  - analyst-review relevance as a separate human-labelled outcome.

### Dataset

For a credible portfolio evaluation:

- 50–100 companies with adverse outcomes;
- 200–500 matched controls;
- matching on period, sector, company size and company age;
- multiple pre-event snapshots per company;
- a later time period held out from rule development.

That would not support industrial ML claims, but it would materially improve the rule evaluation.

### Labels

Create a written rubric before labelling. Have at least one second reviewer label a subset without seeing the system verdict. Report agreement, disagreements and adjudication.

Do not label a director departure Serious because later news revealed the person was CFO unless that role information was actually available to the product on the date.

### Point-in-time safeguards

Each fixture should contain:

- source payload;
- source endpoint;
- retrieval/publication timestamp;
- observation cut-off;
- company number;
- rule version;
- expected outcome;
- label rationale.

Tests must reject any contextual event after the cut-off.

### Metrics

Report:

- recall at Serious-or-higher;
- precision at Serious-or-higher;
- false alerts per 100 monitored companies per month;
- proportion of portfolio flagged;
- median warning lead time;
- recall among failures at 3, 6 and 12 months;
- severity-weighted cost using explicit false-positive/false-negative assumptions;
- missing/stale-data rate;
- briefing factual pass rate.

Accuracy should not be the headline metric because Routine cases will dominate a realistic population.

## 5. Ranked data sources

Access information checked **1 September 2026**.

| Rank | Source | Signal added | Coverage/duplication | Access and cost | Effort |
|---:|---|---|---|---|---|
| 1 | Companies House Document API and insolvency endpoint | Filed accounts, going-concern wording, balance-sheet and liquidity ratios, insolvency case detail | Same provider but materially richer evidence; some insolvency duplication | Official read APIs; document metadata/content and insolvency endpoints are documented. No separate price is stated; existing API authentication applies. [Document API](https://developer-specs.company-information.service.gov.uk/document-api/reference/document-location/fetch-a-document), [insolvency endpoint](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/insolvency) | Medium–High because PDF/iXBRL extraction is variable |
| 2 | UK Payment Practices Reporting | Average payment time, percentage paid late, percentage beyond 60/90/120 days, changes between reports | Distinct behavioural signal, but only qualifying large businesses | Reports are public and all published reports can be downloaded; businesses report at least twice yearly. [GOV.UK service](https://www.gov.uk/check-when-businesses-pay-invoices) | Low–Medium |
| 3 | Companies House Streaming API | Timely filing, officer, charge and insolvency events | Duplicates current Companies House facts; improves freshness and reliability rather than signal breadth | Stream-key authentication; official streams exist for filings, insolvencies, charges and officers. No separate charge identified. [Streaming API](https://developer-specs.company-information.service.gov.uk/streaming-api/reference/insolvency-cases/stream) | Medium; unnecessary for a small two-week demo |
| 4 | The Gazette | Formal insolvency, winding-up, administration and strike-off notices with legal context | Considerable duplication with Companies House, potentially different timing/detail | Gazette information excluding personal data is reusable under OGL v3; data-service terms apply. [Gazette data terms](https://www.thegazette.co.uk/data/terms-and-conditions) | Medium; verify the precise retrieval route before committing |
| 5 | Registry Trust | Company CCJs and judgment activity—strong evidence of unpaid obligations | Genuinely additive, not available from Companies House | Public lookups and paid bulk/segment services are offered; current bulk/API price is not publicly verified and requires sales contact. [Registry Trust services](https://www.registry-trust.org.uk/services) | Medium–High; paid access and entity matching |
| 6 | FCA Register | Authorisation, restrictions, cancellations and permissions | Highly valuable only for regulated financial-services companies | Public search is available, but reusable extracts are paid. For example, the current weekly firms-only compliance extract is £4,467.83 annually excluding VAT; other-use pricing is higher. [FCA extract charges](https://www.fca.org.uk/firms/financial-services-register/data-extract) | Medium; poor general-market coverage |
| 7 | Creditsafe or equivalent credit bureau | Credit score, recommended limit, payment history, CCJs, financials and monitoring | Strong signal breadth, but duplicates much of the intended product and makes the demo dependent on an incumbent | API available; public API pricing was not verified and appears quote-based. [Creditsafe API](https://www.creditsafe.com/gb/en/enterprise/integrations/company-data-api.html) | Medium technically; high commercial dependency |
| 8 | GDELT/news | M&A, restructuring, layoffs, profit warnings and executive-role context | Additive context but noisy and difficult to entity-match | GDELT describes its data as free and open, with raw downloads and BigQuery access. [GDELT data](https://www.gdeltproject.org/data.html) | High if used for automatic verdicts; Medium if displayed as analyst context |

The best next source is not generic news. It is either Payment Practices Reporting for a quick behavioural signal or filed-account extraction for deeper credit evidence.

## 6. UI and workflow recommendations

The current card layout is suitable for a demo, but not an analyst workflow.

### Portfolio screen

Each row should answer five questions:

| User question | UI element |
|---|---|
| What changed? | New-since-last-review summary |
| How serious is it? | Current review priority with rule explanation |
| Is the information complete? | Freshness/data-quality indicator |
| Why was it escalated? | Two or three evidence chips |
| What should I do? | Review, assign, snooze or dismiss action |

Use a table for the portfolio, not large cards. Credit teams need to scan and sort 50–500 companies. Reserve cards for a compact demonstration mode.

Suggested columns:

- company;
- current priority;
- change since last review;
- latest material signal;
- corroborating signals;
- data freshness;
- exposure value;
- owner;
- review status;
- next review date.

### Company detail

Show:

1. current assessment and evidence;
2. what changed since last review;
3. time-ordered signal history;
4. filing source links;
5. accounts/payment trends;
6. analyst notes and decisions;
7. data-quality history.

Separate:

- **event severity:** importance of a specific filing;
- **company priority:** need for review now;
- **confidence/data completeness:** strength of the evidence.

Do not represent confidence through another red/amber/green scale.

### User actions

Add:

- mark useful;
- dismiss as irrelevant;
- mark M&A/restructure explanation;
- already known;
- assign to colleague;
- add note;
- snooze until date;
- record action taken;
- mark reviewed.

These outcomes become future evaluation data.

### User segmentation

Do not build three separate products yet. Use the same evidence with configurable actions:

- **Credit analyst:** review limit, suspend credit, request accounts.
- **Account manager:** contact customer, escalate internally.
- **Procurement:** assess continuity plan, alternate supplier, contract exposure.

## 7. Two-week v2 backlog

### Must have

| Order | Build | Evidence of success |
|---:|---|---|
| 1 | Fix API failure/missingness handling | Forced timeout/401/429 tests produce Unknown/Stale, never Routine |
| 2 | Fix company-level risk aggregation | A Serious new filing raises company priority and “Need attention” in an automated test |
| 3 | Make rules point-in-time safe | A future filing added to a fixture cannot alter an earlier verdict |
| 4 | Add a persistent briefing queue | More than five new filings are all eventually briefed, with Serious/Critical processed first |
| 5 | Package reproducible evaluation fixtures | A fresh clone can run the verdict suite without a private SQLite database or live API calls |
| 6 | Correct rule/documentation inconsistencies | Tests demonstrate first/second/third accounting-date behaviour and terminology no longer overstates founder/borrowing claims |
| 7 | Add rule provenance and source freshness | Every displayed priority can show matched rule, evidence, rule version and last successful retrieval |

### Should have

| Order | Build | Purpose |
|---:|---|---|
| 8 | Add company observation history | Enables genuine trend and changed-since-last-run views |
| 9 | Expand to a population-based evaluation | Measures false-alert burden and warning lead time |
| 10 | Redesign portfolio UI as a sortable work queue | Makes the product credible for daily use |
| 11 | Add analyst feedback states | Captures usefulness and M&A explanations |
| 12 | Integrate Payment Practices Reporting for matching companies | Adds a distinct payment-behaviour signal at manageable effort |

### Later

- Companies House streaming;
- filed-account extraction and ratio calculation;
- Registry Trust/CCJ integration;
- FCA-specific sector module;
- news context;
- authentication, teams and production deployment.

## 8. Three things not to build yet

### 1. Machine-learning failure prediction

There is no representative, point-in-time-labelled training population. An ML model now would add opacity without adding justified predictive power.

### 2. An editable rules-management interface

Rule provenance and automated tests matter first. A polished configuration UI over weak or unvalidated rules would be theatre.

### 3. Generic news sentiment

Entity ambiguity, duplicated articles, M&A confusion and sentiment noise will create work rather than reduce it. News should eventually supply corroborating context, not independently drive severity.

## 9. Final top five actions

1. **Correct headline company prioritisation** so filing severity actually affects what users see.
2. **Represent missing and stale data explicitly** instead of converting failures into healthy zeros.
3. **Rebuild the verdict evaluation around committed point-in-time fixtures** and remove future-event leakage.
4. **Add persistent briefing queuing and rule provenance** so work is not silently lost and decisions are reproducible.
5. **Replace the “10/12 accuracy” proposition with an honest regression claim**, then expand evaluation across distressed companies and matched healthy controls.

## Conclusion

The project’s core concept is better than its current implementation. The architecture shows good judgement, but the dashboard and evaluation presently create more confidence than the code earns. Fixing those contradictions would make the portfolio story substantially stronger than adding another API or more AI.
