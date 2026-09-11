# Signal Tracker — Data Source Landscape

**Prepared:** 1 September 2026  
**Purpose:** Identify free and paid data sources that could strengthen Signal Tracker beyond its current Companies House monitoring.

## Executive recommendation

Signal Tracker should eventually combine five distinct families of evidence:

1. **Financial strength** — accounts, liquidity, debt and going-concern evidence.
2. **Payment behaviour** — late payment, CCJs, missed payments and disputes.
3. **Legal and regulatory events** — insolvency notices, enforcement and licence restrictions.
4. **Commercial and operational change** — lost contracts, closures, recruitment and disruption.
5. **Internal exposure** — how much the user is owed, supplier dependence and behavioural change.

The goal is not to collect the most data. It is to combine independent dimensions so that an ambiguous event becomes a defensible confluence of risk signals.

## Priority shortlist

| Priority | Source | Signal added | Cost | Recommendation |
|---:|---|---|---|---|
| 1 | Companies House accounts data | Financial deterioration and ratios | Free | Best immediate addition |
| 2 | UK Payment Practices Reporting | How promptly large businesses pay suppliers | Free | High-value and relatively accessible |
| 3 | The Gazette | Formal insolvency and winding-up notices | Free/open data | Strong distress evidence |
| 4 | Registry Trust | CCJs and unsatisfied judgments | Paid | Probably the most valuable paid addition |
| 5 | Internal customer/supplier data | Late payments, exposure and behavioural change | User-owned | Potentially the strongest overall signal |
| 6 | FCA Register and actions | Authorisation restrictions and regulatory trouble | Free API | Excellent for financial-services companies |
| 7 | News and announcements | M&A, executive roles, restructuring and profit warnings | Free/paid | Best used as corroboration |
| 8 | Credit-reference provider | Scores, credit limits, payment data and monitoring | Paid | Valuable benchmark but potentially duplicative |

## 1. More value from Companies House

### Filed accounts and financial ratios

Companies House provides a free accounts data product containing electronically filed accounts in XBRL/iXBRL format. Daily and monthly downloads are available through [Companies House data products](https://www.gov.uk/guidance/companies-house-data-products).

Useful fields include:

- cash and cash equivalents;
- current assets and current liabilities;
- total assets and liabilities;
- creditors due within and after one year;
- net assets;
- turnover;
- operating profit and profit after tax;
- retained earnings;
- employee count;
- audit status;
- accounts type: full, small, micro-entity or dormant.

Potential derived signals:

- current and quick ratios;
- debt-to-assets;
- working-capital deterioration;
- falling cash;
- declining net assets;
- creditor growth relative to assets or turnover;
- consecutive loss-making periods;
- turnover and margin deterioration;
- declining employee count;
- accounts becoming progressively less detailed;
- movement to dormant or micro-entity reporting.

Directional deterioration matters more than one isolated ratio. For example:

> Accounts overdue + falling net assets + growing short-term creditors + a new registered charge.

### Filing documents

The [Companies House Document API](https://developer-specs.company-information.service.gov.uk/document-api/reference/document-location/fetch-a-document) provides the documents behind filing-history entries.

Potential textual evidence includes:

- going-concern uncertainty;
- material uncertainty;
- qualified audit opinions;
- emphasis-of-matter paragraphs;
- covenant breaches;
- dependence on refinancing or parent support;
- restructuring and redundancy provisions;
- contingent liabilities;
- significant litigation;
- declining order books;
- auditor resignation explanations.

This is a strong future LLM use case: use the model to extract structured evidence from a document, while deterministic rules decide how that evidence affects review priority.

### Additional Companies House data

Also consider:

- insolvency case details;
- persons with significant control;
- previous company names;
- officer appointments across connected businesses;
- director disqualifications;
- group and subsidiary relationships;
- rapid ownership changes;
- repeated address changes;
- auditor appointments and resignations;
- replacement or correction filings;
- unusually late confirmation statements;
- Companies House streaming for faster filings, charges, officers and insolvency events.

## 2. UK Payment Practices Reporting

Qualifying large businesses publish information including average invoice-payment time and the proportion of invoices paid late. Reports are submitted at least twice annually and published reports can be downloaded through the [GOV.UK Payment Practices service](https://www.gov.uk/check-when-businesses-pay-invoices).

Potential signals:

- worsening average payment time;
- increasing percentage of invoices paid late;
- growing proportion paid after 60 days;
- increasing value of disputed invoices;
- lengthening contractual payment terms;
- deterioration across consecutive reports;
- poor payment performance combined with weakening accounts.

Coverage is limited to qualifying large businesses, but the data directly measures supplier-payment behaviour and is more relevant to supplier risk than many governance signals.

## 3. The Gazette

[The Gazette](https://www.thegazette.co.uk/data) contains official public notices and makes much of its data available under the Open Government Licence, subject to restrictions around personal data.

Potential events include:

- winding-up petitions and orders;
- appointment of administrators;
- notices to creditors;
- liquidator appointments;
- company voluntary arrangements;
- meetings of creditors;
- intended dividends to creditors;
- strike-off notices;
- insolvency-practitioner changes.

Some events overlap with Companies House. Before integrating it fully, test whether Gazette notices appear earlier or provide more actionable information:

> For a sample of failed companies, which source published the first usable warning, and by how many days?

## 4. Registry Trust and CCJs

[Registry Trust](https://www.registry-trust.org.uk/services/judgment-data) maintains the official register of judgments, orders and fines and offers searches, bulk datasets and monitoring services.

Useful fields and patterns:

- new company CCJ;
- judgment amount;
- satisfied versus unsatisfied status;
- number of judgments;
- cumulative judgment value;
- repeated judgments in a short period;
- time taken to satisfy;
- judgments affecting connected companies.

Possible rules:

- first unsatisfied CCJ → Watch;
- multiple unsatisfied CCJs within six months → Serious;
- increasing judgment amounts → escalate;
- CCJ + overdue accounts + new charges → strong confluence.

Pricing is sales-led. A sensible first step would be pay-as-you-go searches across the historical evaluation cohort before considering bulk access.

## 5. Internal customer and supplier data

This could turn Signal Tracker from a public-record viewer into a genuinely useful credit and supplier-risk product.

### Customer-credit signals

- aged receivables;
- days beyond terms;
- missed direct debits or bounced payments;
- partial payments;
- payment-plan requests;
- increasing disputes;
- worsening contactability;
- credit-limit utilisation;
- falling order frequency;
- unusually large final orders;
- requests to change payment terms;
- current financial exposure.

### Supplier-risk signals

- late deliveries;
- falling fill rate;
- increasing defects;
- longer lead times;
- reduced order acceptance;
- requests for deposits or payment in advance;
- abrupt price increases;
- changed bank details;
- turnover among key contacts;
- service-level breaches;
- replacement time and supplier dependency.

The commercially meaningful calculation is:

> **External risk × financial or operational exposure = review priority**

A company with Serious external signals but £500 exposure may be less urgent than one with Watch signals and £2 million exposure.

## 6. FCA data

For insurers, brokers, lenders, payments businesses and other regulated firms, FCA data could be excellent. The FCA offers a currently free Register API without an SLA, alongside paid extracts. See the [FCA Financial Services Register](https://www.fca.org.uk/firms/financial-services-register).

Potential signals:

- authorisation cancelled or suspended;
- new restrictions;
- permissions removed;
- regulatory-status changes;
- appointed-representative relationship ended;
- change of principal;
- disciplinary or enforcement action;
- Warning List appearance;
- key regulated individual no longer registered.

For some financial-services companies, FCA records may also help address Companies House's inability to identify CFOs, CEOs and other functional roles.

## 7. Listed-company announcements

For listed businesses, regulatory announcements may provide richer and earlier evidence than Companies House. The [FCA National Storage Mechanism](https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism) contains regulated disclosures and documents.

Potential signals:

- profit warnings;
- covenant breaches;
- emergency fundraising;
- refinancing announcements;
- delayed results;
- auditor resignation;
- suspension of trading;
- dividend cancellation;
- major contract loss;
- CEO or CFO departure;
- restructuring;
- going-concern statements;
- adverse litigation.

Coverage is limited to listed businesses, but signal quality is high.

## 8. News and media

Possible sources include:

- GDELT;
- NewsAPI;
- Event Registry;
- specialist trade publications;
- local business publications;
- company press-release and investor-relations pages.

[GDELT](https://www.gdeltproject.org/data.html) provides free and open underlying datasets.

Search for:

- redundancies and site closures;
- restructuring or rescue talks;
- delayed salaries;
- funding problems;
- contract losses;
- product recalls;
- cyberattacks;
- investigations and litigation;
- executive departures;
- M&A or private-equity activity.

News should primarily explain ambiguity. For example, a director-resignation cluster combined with acquisition news should be labelled as likely M&A-related rather than automatically treated as distress.

Generic sentiment scoring is unlikely to be useful: it is noisy, difficult to explain and vulnerable to irrelevant coverage.

## 9. Government contracts and procurement

[Find a Tender](https://www.find-tender.service.gov.uk/Developer/Documentation) exposes notices using the Open Contracting Data Standard through an API.

Potential signals:

- major contract won;
- contract unexpectedly terminated;
- supplier replaced;
- contract value reduced;
- failure to secure renewal;
- dependence on one public-sector customer;
- repeated contract modifications;
- procurement disputes.

The Procurement Act introduced a central debarment list. Addition to the list could materially affect government-dependent suppliers. See the [Debarment Review Service](https://www.gov.uk/guidance/debarment-review-service-drs).

This is especially relevant to construction, outsourcing, facilities management, defence, health, consulting and technology suppliers.

## 10. Regulatory and enforcement sources

### Information Commissioner's Office

The [ICO](https://ico.org.uk/action-weve-taken/) publishes monetary penalties, enforcement notices, prosecutions and reprimands.

Signals include substantial fines, serious data breaches and obligations that could create financial or operational pressure.

### Health and Safety Executive

The [HSE](https://www.hse.gov.uk/enforce/convictions.htm) publishes enforcement notices and convictions.

Signals include prohibition notices, repeated improvement notices, prosecutions, substantial fines and fatality-related convictions.

### Other sector regulators

Depending on the watchlist, investigate:

- CQC for care providers;
- Ofsted for education and childcare;
- Ofgem for energy;
- Ofcom for telecoms;
- Environment Agency;
- Solicitors Regulation Authority;
- Gambling Commission;
- Charity Commission;
- Financial Reporting Council;
- Competition and Markets Authority.

Loss of a regulatory licence can represent greater operational risk than a weak financial ratio.

## 11. Sanctions and compliance

The [UK Sanctions List](https://www.gov.uk/government/publications/the-uk-sanctions-list) is the single official source for UK sanctions designations and is available in downloadable formats.

Potential checks:

- company directly designated;
- director or beneficial owner designated;
- parent or subsidiary connection;
- sanctioned-jurisdiction exposure;
- connected entity newly designated;
- director or related organisation on a procurement debarment list.

This is not normally a distress signal, but it can create immediate trading, banking and supply-chain risk.

## 12. Employment and organisational signals

Possible sources include:

- [Adzuna API](https://developer.adzuna.com/overview);
- company careers pages;
- job boards;
- redundancy announcements;
- licensed company-headcount data;
- employee-review trends.

Potential signals:

- recruitment suddenly stops;
- finance or restructuring roles appear;
- replacement CFO recruitment;
- repeated reposting of senior roles;
- rapid geographic contraction;
- high vacancy turnover;
- multiple temporary finance or debt-collection roles.

These are weak individually but may become useful alongside payment, accounts and leadership evidence.

## 13. Digital and operational footprint

More experimental ideas include:

- repeated website outages;
- domain-expiry proximity;
- reduction in website products or locations;
- store closures;
- changes to delivery promises;
- app-store rating deterioration;
- website-traffic change;
- technology removal;
- customer-service response times;
- review volume and complaint themes;
- social accounts becoming inactive;
- changes in Google search interest.

These should not independently produce Serious or Critical verdicts. They are contextual prompts for human review.

## 14. Paid commercial sources

Providers worth exploring include:

- Creditsafe;
- Experian Business;
- Dun & Bradstreet;
- CRIF;
- Red Flag Alert;
- Moody's Orbis;
- Graydon;
- Allianz Trade;
- Atradius;
- Coface;
- Sayari;
- OpenCorporates for broader international entity matching.

Paid sources may add:

- commercial credit scores;
- recommended credit limits;
- trade-payment experience;
- CCJs;
- group structures and international entities;
- failure-risk scores;
- credit-limit monitoring;
- trade-credit-insurance decisions.

Before purchasing, compare a provider against Signal Tracker on the same evaluation companies. Otherwise, the project risks paying for a black-box score without knowing whether it materially improves decisions.

## Suggested evidence model

Avoid combining everything into one arbitrary points score. Organise evidence into dimensions:

| Dimension | Example evidence |
|---|---|
| Financial | Falling net assets, losses and weak liquidity |
| Payment | Late invoices, CCJs and worsening payment practices |
| Funding | Registered charges, emergency fundraising and covenant issues |
| Governance | Executive churn, auditor resignation and ownership changes |
| Legal/regulatory | Enforcement, licence restrictions and winding-up action |
| Operational | Contract loss, closure and delivery failures |
| Context | M&A, restructuring and sector shocks |
| Exposure | Amount owed, contract dependency and replacement difficulty |

Suggested review states:

- **Routine:** no material deterioration.
- **Watch:** one meaningful but ambiguous signal.
- **Serious:** multiple independent dimensions worsening.
- **Critical:** formal failure or an immediate threat requiring action.
- **Unknown:** data unavailable, stale or contradictory.

## Recommended build order

1. Extract financial fields and trends from Companies House XBRL accounts.
2. Add Payment Practices Reporting.
3. Test Gazette timing against Companies House on failed companies.
4. Trial Registry Trust searches across the historical evaluation cohort.
5. Add synthetic internal exposure and payment data to demonstrate prioritisation.
6. Add FCA data for a financial-services demonstration cohort.
7. Use news to classify contextual explanations such as M&A versus distress.
8. Add sector-specific sources once the intended customer segment is clearer.

The standout proposition is:

> **Here are the companies showing signs of trouble, why they have been flagged, and where your business is most exposed.**
