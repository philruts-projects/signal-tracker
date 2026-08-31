# Phase 6 — Evaluation results

Test cases: 12  ·  Models: Haiku vs Sonnet  ·  Judge: Opus

## Summary (average judge scores)

| Model | Factual | Interpretation | Action | Overall | Severity match | Hallucinations |
|---|---|---|---|---|---|---|
| Haiku | 4.5 | 3.5 | 3.4 | 3.5 | 7/10 | 0/10 |
| Sonnet | 4.9 | 3.8 | 3.4 | 3.8 | 7/10 | 0/10 |

## Case-by-case

### 1. Direct Line Insurance Group plc — TM01 (2026-08-05)
*Expected severity:* **Routine**  
*Ground truth:* Single director (Jane Elizabeth Adamson) departed; large healthy insurer; not distress on its own

**Haiku**

> # Direct Line Insurance Group plc — Director Departure
> 
> **What happened:**
> Jane Elizabeth Adamson stepped down as a director of Direct Line Insurance Group plc on 31 July 2026.
> 
> **Why it matters:**
> Director departures are routine events, but the commercial significance depends on seniority and context. This filing alone doesn't indicate whether Adamson held an executive role, chaired a committee, or was independent; her departure could reflect planned rotation, role changes, or other circumstances. Check the company's recent announcements or RNS disclosures for context on her position and any replacement.
> 
> **Suggested action:**
> Review Direct Line's latest regulatory news and board composition statements to assess whether this departure signals any change in governance, strategy, or risk oversight relevant to your engagement.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, appropriately routine framing with sensible follow-up steps, though it adds little beyond restating the filing and omits the mitigating context of the insurer's scale and financial health._

**Sonnet**

> **What happened:** Direct Line Insurance Group plc filed a TM01 confirming that Jane Elizabeth Adamson ceased to be a director of the company, with an effective termination date of 31 July 2026.
> 
> **Why it matters:** Director departures at large, listed companies like Direct Line are routine governance events and often reflect planned retirements, role changes, or board reshuffles rather than operational distress; on its own, this filing gives no indication of financial or trading concern.
> 
> **Suggested action:** Note the change for your records and check Direct Line's investor relations announcements or board composition pages to confirm the context and any successor appointment, but no immediate commercial action is required.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, correctly framed as routine governance with a sensible low-effort verification step._

---

### 2. Marshmallow Financial Services Ltd — AP01 (2026-08-11)
*Expected severity:* **Routine**  
*Ground truth:* New director (Emma Alley) appointed; growth-stage InsurTech; benign or positive

**Haiku**

> **What happened:**
> Ms Emma Alley was appointed as a director of Marshmallow Financial Services Ltd on 3 August 2026.
> 
> **Why it matters:**
> This signals a change in the company's governance and management structure. Director appointments typically reflect business expansion, succession planning, or a shift in operational focus, though the appointment alone does not indicate the underlying reason or Ms Alley's specific remit.
> 
> **Suggested action:**
> Confirm Ms Alley's background and responsibilities with your account contact to understand whether this affects your credit, commercial or procurement position with the company.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 3 · assigned **Routine** (match) · hallucination: False  
> _Accurate and appropriately low-key, though the interpretation is generic and the suggested outreach is slightly heavy for a routine director appointment at a growth-stage firm._

**Sonnet**

> **What happened:** Marshmallow Financial Services Ltd filed notice of the appointment of Ms Emma Alley as a director, effective 3 August 2026.
> 
> **Why it matters:** New director appointments are routine governance events and typically signal continuity or strengthening of leadership rather than distress; without further context (e.g. her role or background), the specific commercial significance is unclear.
> 
> **Suggested action:** Note the appointment on file and check future filings or public announcements for any related changes in company direction, ownership, or financial position.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 3 · assigned **Routine** (match) · hallucination: False  
> _Accurate and correctly routine, though generic—adds no sector or growth-stage context and the suggested action is boilerplate monitoring._

---

### 3. Admiral Group plc — AA (2026-08-27)
*Expected severity:* **Routine**  
*Ground truth:* Interim accounts to 30 Jun 2026 filed; routine reporting; healthy

**Haiku**

> **What happened:**
> Admiral Group plc has filed interim accounts covering the six-month period to 30 June 2026.
> 
> **Why it matters:**
> Interim accounts are filed mid-way through the financial year and provide an early indicator of trading performance and financial position. For a listed insurance group like Admiral, this filing allows stakeholders to assess H1 profitability, underwriting performance, and capital adequacy before year-end results.
> 
> **Suggested action:**
> Review the interim accounts for material changes in underwriting results, investment returns, claims experience and regulatory capital ratios compared to prior year, and assess any commentary on market conditions or strategic developments.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, appropriately routine framing of an interim accounts filing, though the suggested review points are generic rather than tailored to any specific risk signal._

**Sonnet**

> What happened: Admiral Group plc filed interim accounts made up to 30 June 2026, submitted to Companies House on 27 August 2026.
> 
> Why it matters: This is a routine, expected filing for a listed group (interim/half-year accounts), consistent with normal statutory reporting rather than any sign of distress or change in status; it offers an opportunity to review updated financial position and trading performance for counterparty risk purposes.
> 
> Suggested action: Obtain and review the filed interim accounts to refresh your credit/exposure assessment, noting any material changes versus the prior period.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, appropriately routine framing of interim accounts with a sensible if generic review action._

---

### 4. Extracover Ltd (Zego) — CS01 (2026-06-21)
*Expected severity:* **Routine**  
*Ground truth:* Confirmation statement filed; administrative annual confirmation; no real signal

**Haiku**

> **What happened:**
> Extracover Ltd (Zego) filed its annual confirmation statement on 21 June 2026, confirming the accuracy of company records as at 12 June 2026.
> 
> **Why it matters:**
> This is a routine annual filing requirement showing the company is maintaining its statutory compliance. The filing was submitted on time, which indicates normal administrative operations and no obvious governance issues.
> 
> **Suggested action:**
> No immediate action needed; continue standard monitoring for material changes flagged in future filings.

*Judge:* overall **4/5** · factual 4 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate and correctly low-urgency, though it omits that this was a confirmation statement 'with updates' and asserts timeliness/no governance issues without support._

**Sonnet**

> What happened: Extracover Ltd (trading as Zego) filed its annual confirmation statement with Companies House, dated as at 12 June 2026, and indicated that updates were made to the company's registered details as part of this filing.
> 
> Why it matters: This is a routine statutory filing confirming the company's records are current, but the "with updates" flag suggests something changed (e.g. registered address, officers, shareholders, or SIC code) — the specific change isn't detailed here, so its commercial significance is ambiguous without further review.
> 
> Suggested action: Pull the full CS01 filing or company profile from Companies House to identify exactly what was updated before deciding whether any follow-up with Zego is warranted.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate and appropriately routine, with a sensible caveat about the 'with updates' flag, though the suggested follow-up slightly overstates the need for action on a purely administrative filing._

---

### 5. Legal & General Group plc — SH01 (2026-08-18)
*Expected severity:* **Routine**  
*Ground truth:* ~GBP 138m share allotment; routine capital activity at a healthy insurer

**Haiku**

> **What happened:**
> Legal & General Group allotted new shares worth £138.07 million on 13 August 2026.
> 
> **Why it matters:**
> Share allotments typically signal capital-raising activity, which can fund acquisitions, debt repayment, or expansion. The scale here is material relative to the company's size, though the commercial purpose isn't specified in this filing alone and could range from routine employee share schemes to a significant equity raise.
> 
> **Suggested action:**
> Cross-reference recent announcements or regulatory news releases to confirm the purpose and whether this signals strategic change or refinancing activity.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

**Sonnet**

> # Briefing: Legal & General Group plc — SH01 Allotment of Shares
> 
> **What happened:** On 13 August 2026, Legal & General Group plc filed a notice confirming an allotment of shares with a total value of approximately £138,072,807.48, formally registered with Companies House on 18 August 2026.
> 
> **Why it matters:** Share allotments are routine for large listed groups and can relate to a variety of activities—employee share schemes, scrip dividends, bonus issues, or capital raising—so this filing alone does not necessarily signal financial distress or a major strategic shift; without further context (e.g. an accompanying prospectus, RNS announcement, or stated purpose), the significance of this specific allotment is ambiguous.
> 
> **Suggested action:** If Legal & General is a material counterparty, check the company's recent RNS/investor announcements or annual report for the stated purpose of this allotment to understand whether it

*Judge:* overall **3/5** · factual 4 · interp 4 · action 2 · assigned **Routine** (match) · hallucination: False  
> _Accurate and appropriately low-key framing, but the suggested action is cut off mid-sentence and adds little beyond 'check the RNS'._

---

### 6. Aviva plc — SH06 (2026-08-21)
*Expected severity:* **Watch**  
*Ground truth:* ~GBP 987m share cancellation; routine mechanism (buyback) but size warrants observation; check vs other factors; briefing should explain what a cancellation is and why firms do it

**Haiku**

> **What happened:**
> Aviva plc cancelled £987.3m of share capital on 14 July 2026.
> 
> **Why it matters:**
> Share cancellations typically follow a share buyback programme, reducing the total number of shares in issue without changing the company's underlying assets or earnings. This increases earnings per share mechanically and signals management confidence in the company's valuation, though it does not improve operational performance. For a large insurer like Aviva, this is a routine capital management exercise.
> 
> **Suggested action:**
> Confirm whether this cancellation was part of a previously announced buyback programme and check if any further tranches are planned.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

**Sonnet**

> **What happened:** Aviva plc filed an SH06 confirming a cancellation of shares (effective 14 July 2026), reducing issued share capital by £987,319,303.62.
> 
> **Why it matters:** This is consistent with a share buyback programme or capital restructuring, both routine for a large listed insurer managing its capital base; it does not, by itself, indicate financial distress and may reflect a return of surplus capital to shareholders. However, a reduction of this scale warrants confirmation against Aviva's public announcements (e.g. buyback or capital return plans) to understand the full context.
> 
> **Suggested action:** Cross-check this filing against Aviva's investor relations announcements or press releases for the corresponding period to confirm the transaction's purpose before drawing any commercial conclusions.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Watch** (match) · hallucination: False  
> _Accurate figures and correctly frames the cancellation as a routine buyback mechanism whose scale merits cross-checking, though it could explain the mechanics of a cancellation more explicitly._

---

### 7. London Capital & Finance plc — AA01 (2018-10-17)
*Expected severity:* **Watch**  
*Ground truth:* Third change of accounting reference date in ~15 months; a single change is routine but repeated changes are an obfuscation/delay red flag; ~3 months before administration; the signal is the repetition (single-filing view misses it)

**Haiku**

> **What happened:**
> London Capital & Finance plc changed its accounting reference date from 27 April to 26 April 2018 — a one-day adjustment to when its financial year ends.
> 
> **Why it matters:**
> This is a minor technical change with no obvious commercial significance. One-day shifts to accounting year-ends are usually administrative housekeeping and don't signal financial distress or operational change. The company's reporting cycle and financial obligations remain essentially unchanged.
> 
> **Suggested action:**
> No immediate action needed; verify this doesn't affect your audit, reporting or payment cycle timelines with the company.

*Judge:* overall **2/5** · factual 4 · interp 2 · action 2 · assigned **Routine** (MISMATCH) · hallucination: False  
> _Accurately describes the one-day date change but dismisses it as housekeeping, missing that this was the third ARD change in ~15 months at a firm months from administration._

**Sonnet**

> What happened: London Capital & Finance plc filed a change to its accounting reference date, shortening its financial year-end from 27 April to 26 April 2018.
> 
> Why it matters: A one-day shift in the accounting reference date is a minor technical adjustment and, taken alone, carries no inherent commercial significance; however, changes to reference dates can sometimes be used to alter statutory filing deadlines, so it's worth noting alongside other filings from this period.
> 
> Suggested action: Check subsequent accounts and confirmation statement filings from this company for timeliness and any related governance changes, given the date is close to this company's later known financial difficulties.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

---

### 8. Carillion plc — TM01 (2017-01-03)
*Expected severity:* **Serious**  
*Ground truth:* Finance director (Richard John Adam) departed; loss of finance leadership at a strained company; ~1 year before collapse; elevate

**Haiku**

> **What happened:**
> Richard John Adam stepped down as a director of Carillion plc on 31 December 2016.
> 
> **Why it matters:**
> Director departures can signal internal changes in strategy, governance, or leadership structure. In Carillion's case, this filing was one of several senior-level changes during a period of significant operational challenge for the company. Monitoring who remains on the board helps assess continuity of management and financial control.
> 
> **Suggested action:**
> Cross-check this departure against other recent filings to understand the broader context of board changes and confirm the company's current leadership structure.

*Judge:* overall **2/5** · factual 4 · interp 2 · action 2 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Facts are correct but the briefing fails to identify Adam as finance director, understating the severity of losing finance leadership at a strained company roughly a year before collapse._

**Sonnet**

> **What happened:** Carillion plc filed a TM01 notice confirming that Richard John Adam ceased to be a director of the company effective 31 December 2016.
> 
> **Why it matters:** Director departures are routine and this filing alone does not indicate financial distress, but a departure of a senior figure (Adam was Carillion's long-serving Finance Director) can be commercially relevant if it coincides with other signals such as changes in auditors, profit warnings, or governance shifts, so it warrants noting rather than ignoring.
> 
> **Suggested action:** Check Carillion's other recent filings and public announcements (e.g. board changes, trading updates) around this date to see whether this departure is part of a wider pattern before adjusting risk assessments.

*Judge:* overall **3/5** · factual 5 · interp 3 · action 3 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Facts are correct and the Finance Director role is identified, but framing it as routine and merely 'worth noting' understates the seriousness of losing finance leadership at a strained company._

---

### 9. Carillion plc — TM01 (2017-07-10)
*Expected severity:* **Serious**  
*Ground truth:* CEO (Richard John Howson) departed; leadership exit ~6 months before collapse; elevate

**Haiku**

> **What happened:**
> Richard John Howson stepped down as a director of Carillion plc on 10 July 2017.
> 
> **Why it matters:**
> This filing signals a change in the company's board composition, though without knowing Howson's specific role or the circumstances of his departure, the significance is unclear. At this time, Carillion was facing significant financial and operational challenges that would lead to its collapse within months, so director departures merit attention to any related disclosures about business difficulties or governance concerns.
> 
> **Suggested action:**
> Cross-check against any contemporaneous RNS announcements or narrative filings to understand whether this was a routine rotation or connected to the company's wider financial position.

*Judge:* overall **3/5** · factual 4 · interp 3 · action 3 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Correct facts and useful collapse context, but it fails to identify Howson as CEO and hedges into a Watch-level tone when a CEO exit six months before failure warrants Serious._

**Sonnet**

> **What happened:** Carillion plc filed a TM01 notice confirming the termination, effective 10 July 2017, of Richard John Howson as a director of the company.
> 
> **Why it matters:** A change in senior leadership can signal a shift in strategic direction or governance, and if this involves the CEO or another key executive, counterparties may want to understand the context, especially given Carillion's scale as a major contractor; however, this filing alone does not indicate the reason for departure or any wider operational or financial concern.
> 
> **Suggested action:** Check for a corresponding public announcement (e.g. RNS/press release) or other recent filings to establish the context and reason for the departure, and monitor for any further officer changes or financial filings in the coming weeks.

*Judge:* overall **2/5** · factual 5 · interp 2 · action 3 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Facts are correct but the briefing hedges on whether Howson was CEO and downplays the significance of a chief executive's exit at a stressed major contractor, understating the expected Serious severity._

---

### 10. Carillion plc — MR01 (2017-10-27)
*Expected severity:* **Serious**  
*Ground truth:* New charge (secured borrowing) - one of a cluster of 5 in one week; company raising secured finance ~3 months before collapse; strong distress signal

**Haiku**

> **What happened:**
> Carillion plc registered a new mortgage charge on 26 October 2017, securing borrowed money against company assets.
> 
> **Why it matters:**
> This signals the company drew down additional secured debt. The timing is notable — Carillion faced significant operational and financial difficulties in late 2017, and additional secured borrowing at this point indicates lenders were tightening their grip on company assets as risk increased.
> 
> **Suggested action:**
> Cross-reference this charge against the company's debt facilities and covenant position as of Q3 2017, and monitor for any announcements about refinancing or liquidity pressure.

*Judge:* overall **4/5** · factual 4 · interp 4 · action 3 · assigned **Serious** (match) · hallucination: False  
> _Accurate and appropriately urgent read of the new charge, but misses the key aggravating context that this was one of five charges filed in a single week, and the suggested action is somewhat generic._

**Sonnet**

> **What happened:** Carillion plc registered a new charge (secured borrowing) with Companies House, charge number 037823790002, created on 26 October 2017 and filed the following day.
> 
> **Why it matters:** A newly created charge indicates the company has granted a lender or creditor security over its assets, which is a routine part of corporate borrowing but can also signal increased reliance on secured debt; the filing alone does not reveal the charge amount, the lender's identity, or the assets involved.
> 
> **Suggested action:** Request or review the full charge document (available on Companies House) to identify the lender, secured assets, and amount, and consider this alongside other credit-risk indicators for Carillion plc given the period's context.

*Judge:* overall **3/5** · factual 5 · interp 2 · action 3 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Accurate on the filing details but frames the charge as largely routine, missing the cluster of five charges in one week and the acute distress signal months before Carillion's collapse._

---

### 11. Greensill Capital (UK) Ltd — TM01 (2026-06-25)
*Expected severity:* **Serious**  
*Ground truth:* Founder (Alexander David Greensill) removed as director; founder departures always warrant a flag (PE deal / funding round / strategy or performance shift)

**Haiku**

> **What happened:**
> Alexander David Greensill stepped down as a director of Greensill Capital (UK) Ltd on 17 June 2026, with the termination formally filed on 25 June 2026.
> 
> **Why it matters:**
> This marks a significant change in the company's governance structure, given Greensill's namesake status as founder of the group. The departure signals a potential shift in strategic direction or ownership control, though the filing alone does not indicate whether this was a planned transition, internal restructuring, or other circumstance.
> 
> **Suggested action:**
> Cross-check current director appointments and recent ownership filings to establish the company's current governance structure and any related changes in control or management.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Serious** (match) · hallucination: False  
> _Accurate and correctly flags founder departure as a serious governance signal, though the action could be sharper on credit exposure and covenant/key-man implications._

**Sonnet**

> # Companies House Filing Briefing
> 
> **Company:** Greensill Capital (UK) Ltd (08126173)
> **Filing:** TM01 – Termination of a Director
> **Date filed:** 25 June 2026
> 
> ---
> 
> **What happened:** Alexander David Greensill ceased to be a registered director of Greensill Capital (UK) Ltd, with an effective termination date of 17 June 2026.
> 
> **Why it matters:** A single director departure is a routine governance change and not inherently a cause for concern, but given this company's history and the founder-linked surname, counterparties may want to note who remains on the board and whether it signals any wider change in control or management direction; on its own, this filing does not indicate financial distress or wrongdoing.
> 
> **Suggested action:** Check the current filed list of officers and any recent confirmation statement or accounts to see who now governs the company, and ask your relationship contact there for context on the change if the company is a material coun

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

---

### 12. Greensill Capital (UK) Ltd — AM01 (2021-03-22)
*Expected severity:* **Critical**  
*Ground truth:* Company entered administration Mar 2021; the failure itself; halt credit and assess exposure

**Haiku**

> **GREENSILL CAPITAL (UK) LTD – ADMINISTRATION ORDER**
> 
> **What happened:**
> An administrator has been appointed to manage the company's assets and liabilities; the company is now in formal insolvency proceedings.
> 
> **Why it matters:**
> This is a significant distress signal. The company is no longer operating under normal management control. Creditors and counterparties face material risk of partial or total loss on outstanding invoices, deposits or contractual obligations. Payment of routine liabilities cannot be assumed.
> 
> **Suggested action:**
> Treat this as a high-priority credit risk review; cease any new trading activity, secure or write down any exposure, and monitor administrator updates on the Companies House register for distribution timetables.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 5 · assigned **Critical** (match) · hallucination: False  
> _Accurate and appropriately urgent administration briefing with clear credit actions, though generic and lacking Greensill-specific context such as its supply-chain finance role or the filing date._

**Sonnet**

> # Briefing: Greensill Capital (UK) Ltd (08126173)
> 
> **What happened:** On 22 March 2021, an administration order was filed for Greensill Capital (UK) Ltd, confirming that the company has entered administration and an administrator has been formally appointed.
> 
> **Why it matters:** This is a formal insolvency event — the company is no longer under normal director control, and creditors, suppliers, and counterparties should expect payments, contracts, and ongoing obligations to be managed (and likely disrupted) by the appointed administrator rather than existing management; recovery of any outstanding sums is now subject to the insolvency process and creditor ranking.
> 
> **Suggested action:** Treat this entity as high-risk for any live exposure — freeze new credit or commitments, identify the appointed administrator via Companies House records, and submit any claims or queries through the formal administration process rather than to prior company contacts.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Critical** (match) · hallucination: False  
> _Accurate, appropriately urgent read of the administration appointment with practical creditor actions; company number is unverified from the supplied facts but appears correct._

---
