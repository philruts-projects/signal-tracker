# Phase 6 — Evaluation results

Test cases: 12  ·  Models: Haiku vs Sonnet  ·  Judge: Opus

## Summary (average judge scores)

| Model | Factual | Interpretation | Action | Overall | Severity match | Hallucinations |
|---|---|---|---|---|---|---|
| Haiku | 4.38 | 3.62 | 3.62 | 3.62 | 6/8 | 0/8 |
| Sonnet | 4.75 | 3.67 | 2.75 | 3.58 | 7/12 | 0/12 |

## Case-by-case

### 1. Direct Line Insurance Group plc — TM01 (2026-08-05)
*Expected severity:* **Routine**  
*Ground truth:* Single director (Jane Elizabeth Adamson) departed; large healthy insurer; not distress on its own

**Haiku**

> **What happened:**
> Jane Elizabeth Adamson stepped down as a director of Direct Line Insurance Group plc on 31 July 2026.
> 
> **Why it matters:**
> Director changes are routine corporate housekeeping when departures are orderly and announced without controversy. This filing simply signals that Adamson's directorship has ended; the lack of surrounding detail suggests a standard transition rather than a departure under difficult circumstances.
> 
> **Suggested action:**
> Check the company's latest annual report or RNS announcements if you need to understand the context of her departure or identify her replacement.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, correctly routine framing with a sensible follow-up check, though the inference that absence of detail implies an amicable exit is mildly speculative and it omits the insurer's scale/financial health as reassuring context._

**Sonnet**

> **What happened:** Direct Line Insurance Group plc filed a TM01 notice confirming that Jane Elizabeth Adamson ceased to be a director of the company, effective 31 July 2026.
> 
> **Why it matters:** Director departures are routinely filed and, on their own, are a normal part of board turnover rather than a sign of operational or financial distress; the assessed severity here is Routine, indicating no immediate cause for concern based on this filing alone.
> 
> **Suggested action:** No immediate action required, but note the change and check Direct Line's next investor or governance announcement for context on board composition.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, correctly framed as routine board turnover with sensible low-urgency follow-up, though the action advice is somewhat generic and the self-referential mention of the severity label is slightly awkward._

---

### 2. Marshmallow Financial Services Ltd — AP01 (2026-08-11)
*Expected severity:* **Routine**  
*Ground truth:* New director (Emma Alley) appointed; growth-stage InsurTech; benign or positive

**Haiku**

> **What happened:**
> Emma Alley was appointed as a director of Marshmallow Financial Services Ltd on 3 August 2026.
> 
> **Why it matters:**
> This is a routine leadership change. Marshmallow Financial Services is a UK-regulated financial services company, so director appointments are standard governance updates that Companies House records. The appointment was effective over a week before public filing, indicating normal administrative processing.
> 
> **Suggested action:**
> No action needed unless you hold existing credit or service arrangements with Marshmallow that require you to update your records of company officers.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

**Sonnet**

> **What happened:** Marshmallow Financial Services Ltd filed notice of the appointment of Ms Emma Alley as a director, effective 3 August 2026.
> 
> **Why it matters:** Routine director appointments are a normal part of corporate governance and do not typically signal financial distress or operational change; this is standard board maintenance activity.
> 
> **Suggested action:** No immediate action required, though credit/account teams may wish to note the update in their records and check for any related pattern of officer changes over time.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 3 · assigned **Routine** (match) · hallucination: False  
> _Accurate and correctly pitched as routine, though it misses company context (growth-stage InsurTech, potential positive signal) and the suggested action is generic._

---

### 3. Admiral Group plc — AA (2026-08-27)
*Expected severity:* **Routine**  
*Ground truth:* Interim accounts to 30 Jun 2026 filed; routine reporting; healthy

**Haiku**

> **What happened:**
> Admiral Group plc has filed interim financial accounts for the six-month period ending 30 June 2026.
> 
> **Why it matters:**
> Interim accounts are routine filing obligations for listed companies and provide a mid-year snapshot of financial performance. This filing confirms the company is meeting its reporting requirements and allows stakeholders to monitor trading performance before the full-year accounts.
> 
> **Suggested action:**
> Review the interim results to assess any changes in profitability, underwriting performance, or cash position since the last full-year filing.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, appropriately low-key summary of a routine interim filing with a sensible if generic review action._

**Sonnet**

> **What happened:** Admiral Group plc filed interim (half-year) accounts with Companies House for the period made up to 30 June 2026.
> 
> **Why it matters:** This is a routine, expected filing for a listed group reporting interim financial results and carries no inherent negative signal; it confirms the company is meeting its normal statutory reporting obligations on schedule.
> 
> **Suggested action:** No action required beyond noting the filing is up to date; review the accounts only if you need updated financial figures for credit or commercial risk assessment.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, appropriately low-urgency summary of a routine interim accounts filing with sensible if generic guidance._

---

### 4. Extracover Ltd (Zego) — CS01 (2026-06-21)
*Expected severity:* **Routine**  
*Ground truth:* Confirmation statement filed; administrative annual confirmation; no real signal

**Haiku**

> # Extracover Ltd (Zego) — Confirmation Statement Filing
> 
> **What happened:**
> The company filed its routine annual confirmation statement on 21 June 2026, confirming its registered details as at 12 June 2026.
> 
> **Why it matters:**
> Confirmation statements are a standard annual filing requirement and indicate the company remains active and compliant with Companies House obligations. This filing carries no warning signals.
> 
> **Suggested action:**
> No action required unless you are reviewing this company for other reasons; proceed with normal monitoring.

*Judge:* overall **4/5** · factual 4 · interp 4 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate and correctly routine, though it omits that this was a confirmation statement 'with updates', which could warrant a quick check of what changed._

**Sonnet**

> **What happened:** Extracover Ltd (trading as Zego) filed its annual confirmation statement dated 12 June 2026, confirming its company details are up to date, with some information updated as part of this filing.
> 
> **Why it matters:** This is a routine statutory filing that all UK companies must submit annually; the "with updates" flag simply means minor details (such as officer, address, or shareholder information) were amended, which is normal and does not itself signal financial distress or operational change.
> 
> **Suggested action:** No immediate action required, but if you hold an active commercial relationship with Zego, it may be worth a quick check of the full filing on Companies House to see exactly which details were updated.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, correctly framed as routine, with a sensible low-effort follow-up suggestion._

---

### 5. Legal & General Group plc — SH01 (2026-08-18)
*Expected severity:* **Routine**  
*Ground truth:* ~GBP 138m share allotment; routine capital activity at a healthy insurer

**Haiku**

> **What happened**
> Legal & General Group plc allotted new shares worth approximately £138m on 13 August 2026.
> 
> **Why it matters**
> Share allotments typically signal either a capital raise, employee share scheme activity, or settlement of corporate transactions. This figure is material but the filing doesn't specify the purpose, so the commercial context—whether this reflects organic growth funding, acquisition-related payments, or routine equity compensation—remains unclear from this notification alone.
> 
> **Suggested action**
> Check the company's regulatory news service announcements or upcoming annual report narrative for detail on the allotment's purpose and whether it materially dilutes existing shareholders.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

**Sonnet**

> **What happened:** Legal & General Group plc filed an SH01 return notifying Companies House of a share allotment dated 13 August 2026, with an associated capital figure of approximately £138.07 million.
> 
> **Why it matters:** Share allotments are a routine corporate action for a large listed group like L&G and can relate to a variety of ordinary business activities (e.g. employee share schemes, capital management, or scrip dividends); on its own, this filing does not indicate financial distress or a change in trading relationship.
> 
> **Suggested action:** No immediate action needed — log the filing for the record and continue standard periodic monitoring of the company's filings.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Routine** (match) · hallucination: False  
> _Accurate, appropriately hedged summary of a routine SH01 with correctly calibrated low-urgency framing and sensible no-action guidance._

---

### 6. Aviva plc — SH06 (2026-08-21)
*Expected severity:* **Watch**  
*Ground truth:* ~GBP 987m share cancellation; routine mechanism (buyback) but size warrants observation; check vs other factors; briefing should explain what a cancellation is and why firms do it

**Haiku**

> **What happened:**
> Aviva plc cancelled shares worth approximately £987.3 million on 14 July 2026.
> 
> **Why it matters:**
> Share cancellation typically follows a buyback programme and reduces the total number of shares in issue. This is a routine capital management action that can signal management confidence in the business, though it also reduces the equity base. The large value suggests a material reduction in Aviva's share count.
> 
> **Suggested action:**
> Confirm whether this relates to a previously announced buyback programme and note the impact on share dilution metrics used in your credit or covenant assessments.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

**Sonnet**

> **What happened:** Aviva plc filed an SH06 notice confirming the cancellation of shares with an aggregate nominal value of £987,319,303.62, effective 14 July 2026.
> 
> **Why it matters:** This is consistent with a routine share buyback and capital reduction exercise, which large listed companies like Aviva undertake periodically to return capital to shareholders; it does not typically indicate financial distress, but it does reduce the company's issued share capital base, which counterparties may wish to note for reference.
> 
> **Suggested action:** No immediate action required — log this as a standard

*Judge:* overall **3/5** · factual 5 · interp 3 · action 2 · assigned **Routine** (MISMATCH) · hallucination: False  
> _Facts and figures are accurate and the buyback mechanism is correctly explained, but the briefing downplays the scale (~£987m) to Routine rather than Watch, omits any prompt to cross-check other exposures, and the action line is truncated mid-sentence._

---

### 7. London Capital & Finance plc — AA01 (2018-10-17)
*Expected severity:* **Serious**  
*Ground truth:* Third change of accounting reference date in ~15 months; repeated changes are an obfuscation/delay red flag; ~3 months before administration; the tool now detects the repetition and should call it Serious

**Haiku**

> # Companies House Filing Briefing
> 
> **Company:** London Capital & Finance plc | **Date filed:** 17 October 2018
> 
> ---
> 
> **What happened:**
> The company changed its accounting reference date from 26 April to 27 April 2018 — a one-day shift marked as a shortened accounting period.
> 
> **Why it matters:**
> A one-day change to the accounting reference date is unusual and typically signals administrative correction rather than a commercial restructuring. The "shortened period" designation suggests this may have been a correction to align records with actual year-end practice. On its own, this is a technical adjustment with no direct bearing on financial health, though the narrow margin warrants checking whether this reflects broader accounting or compliance issues.
> 
> **Suggested action:**
> Request the company's most recent accounts (filed after this change) to confirm the new reporting cycle is being followed consistently and to verify there are no underlying compliance concerns.

*Judge:* error — could not parse judge output: Expecting value: line 1 column 1 (char 0)

**Sonnet**

> What happened: London Capital & Finance plc filed a change to its accounting reference date, shortening its financial year end from 27 April to 26 April 2018.
> 
> Why it matters: On its face this is a one-day technical adjustment, but changes to the accounting reference date can sometimes signal an

*Judge:* overall **2/5** · factual 4 · interp 2 · action 1 · assigned **Routine** (MISMATCH) · hallucination: False  
> _Dates are stated correctly but the briefing is truncated, downplays the change as a one-day technicality, and misses the critical pattern of repeated ARD changes shortly before administration._

---

### 8. Carillion plc — TM01 (2017-01-03)
*Expected severity:* **Serious**  
*Ground truth:* Finance director (Richard John Adam) departed; loss of finance leadership at a strained company; ~1 year before collapse; elevate

**Haiku**

> **What happened:**
> Richard John Adam stepped down as a director of Carillion plc on 31 December 2016.
> 
> **Why it matters:**
> Director changes are routine in most cases, but this filing alone doesn't signal whether the departure was planned or problematic. Given Carillion's subsequent collapse in 2018, this historical filing reflects the company's operating period, but the departure itself carries no inherent warning sign without additional context around the circumstances or other board changes at the same time.
> 
> **Suggested action:**
> Cross-reference this filing with any concurrent board announcements or other director changes from late 2016 to assess whether the departure was part of planned succession or a wider governance shift.

*Judge:* overall **2/5** · factual 3 · interp 2 · action 2 · assigned **Routine** (MISMATCH) · hallucination: False  
> _Correctly states the name and date but fails to identify Adam as Finance Director and dismisses the departure as unremarkable, materially understating the risk signal._

**Sonnet**

> What happened: Carillion plc filed a TM01 notice confirming the termination of director Richard John Adam, effective 31 December 2016.
> 
> Why it matters: Board-level departures are routine filings, but given Richard Adam's long tenure as Carillion's Finance Director, this signals a leadership change in a key financial oversight role worth noting for context in future filings or credit assessments.
> 
> Suggested action: Check subsequent filings for a replacement finance director appointment and monitor for any related commentary in the company's next annual report or announcements.

*Judge:* overall **3/5** · factual 5 · interp 3 · action 3 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Accurate and correctly identifies Adam's finance director role, but frames the CFO exit as routine context rather than a serious red flag at an already strained contractor, and the suggested action is passive monitoring rather than escalation._

---

### 9. Carillion plc — TM01 (2017-07-10)
*Expected severity:* **Serious**  
*Ground truth:* CEO (Richard John Howson) departed; leadership exit ~6 months before collapse; elevate

**Haiku**

> **What happened:**
> Richard John Howson stepped down as a director of Carillion plc on 10 July 2017.
> 
> **Why it matters:**
> Director departures are routine changes in board composition, though this particular departure occurred during a period when Carillion faced significant financial and operational pressures (the company entered administration in January 2018). At the time of filing, this move would not have flagged immediate concern on its own, but it forms part of the broader context of leadership changes the company experienced in 2017.
> 
> **Suggested action:**
> Cross-reference this departure with other board changes and financial performance data from mid-2017 to establish whether it was routine succession planning or part of a wider pattern of instability.

*Judge:* overall **2/5** · factual 3 · interp 2 · action 3 · assigned **Watch** (MISMATCH) · hallucination: False  
> _Correct name and date but fails to identify Howson as CEO and frames a critical leadership exit six months before collapse as largely routine, understating severity._

**Sonnet**

> What happened: Carillion plc filed a TM01 confirming that Richard John Howson ceased to be a director of the company, effective 10 July 2017.
> 
> Why it matters: A single director termination is a routine administrative filing and does not, by itself, indicate distress; however, board changes at a

*Judge:* overall **2/5** · factual 4 · interp 2 · action 1 · assigned **Routine** (MISMATCH) · hallucination: False  
> _Filing details are accurate but the briefing misses that Howson was the CEO, wrongly frames the exit as routine administration, and cuts off mid-sentence without any recommended action._

---

### 10. Carillion plc — MR01 (2017-10-27)
*Expected severity:* **Serious**  
*Ground truth:* New charge (secured borrowing) - one of a cluster of 5 in one week; company raising secured finance ~3 months before collapse; strong distress signal

**Haiku**

> **What happened:**
> Carillion plc registered a mortgage charge on 26 October 2017, creating a secured loan arrangement (charge number 037823790002).
> 
> **Why it matters:**
> This signals the company has taken on new secured debt. While mortgage charges are routine, the timing and context matter: Carillion was facing serious liquidity and contract performance issues in 2017, and new secured borrowing typically indicates lenders are tightening terms or the company needs cash urgently. This adds to creditor hierarchy risk if the company's position deteriorates further.
> 
> **Suggested action:**
> Review recent trading updates and cash flow statements to establish why this borrowing was needed, and check whether other secured lenders have priority claims over the same assets.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Serious** (match) · hallucination: False  
> _Accurate and appropriately urgent, correctly framing new secured borrowing as a distress signal, though it misses the aggravating pattern of five charges registered in a single week._

**Sonnet**

> What happened: Carillion plc registered a new charge (deed, charge number 037823790002) with Companies House on 27 October 2017, securing borrowing created the previous day, 26 October 2017.
> 
> Why it matters: The creation of a new secured charge indicates the company has pledged assets against a debt obligation, which can signal increased reliance on secured funding or lender-imposed conditions on existing facilities; the "Serious" severity flag suggests this may be part of a wider pattern of financial strain, though the filing alone does not specify the lender, amount, or assets secured.
> 
> Suggested action: Request s

*Judge:* overall **2/5** · factual 4 · interp 3 · action 1 · assigned **Serious** (match) · hallucination: False  
> _Accurate on the filing facts and correctly Serious, but it misses the cluster of five charges and proximity to collapse, awkwardly cites its own severity flag, and the recommended action is cut off mid-sentence._

---

### 11. Greensill Capital (UK) Ltd — TM01 (2026-06-25)
*Expected severity:* **Serious**  
*Ground truth:* Founder (Alexander David Greensill) removed as director; founder departures always warrant a flag (PE deal / funding round / strategy or performance shift)

**Haiku**

> **What happened:**
> Alexander David Greensill stepped down as a director of Greensill Capital (UK) Ltd on 17 June 2026, with the termination filed at Companies House on 25 June 2026.
> 
> **Why it matters:**
> The departure of a founder or senior director can signal strategic change, internal dispute, or operational restructuring. Given the company name and timing, this warrants prompt clarification on whether this reflects planned succession, a change in the company's operating model, or other material developments affecting its governance and credit profile.
> 
> **Suggested action:**
> Contact the company to understand the reason for the director's departure and whether this affects credit terms, operational continuity, or the company's financial trajectory.

*Judge:* overall **4/5** · factual 5 · interp 4 · action 4 · assigned **Serious** (match) · hallucination: False  
> _Accurate and appropriately urgent, though it only hints at the founder/eponymous link rather than stating it outright, and the suggested action is somewhat generic._

**Sonnet**

> What happened: Alexander David Greensill ceased to be a registered director of Greensill Capital (UK) Ltd, effective 17 June 2026, as recorded in a TM01 filing on 25 June 2026

*Judge:* overall **2/5** · factual 5 · interp 2 · action 1 · assigned **Routine** (MISMATCH) · hallucination: False  
> _Accurate but purely descriptive — it fails to flag that this is the founder's departure or suggest any follow-up, understating the seriousness._

---

### 12. Greensill Capital (UK) Ltd — AM01 (2021-03-22)
*Expected severity:* **Critical**  
*Ground truth:* Company entered administration Mar 2021; the failure itself; halt credit and assess exposure

**Haiku**

> **What happened:**
> Greensill Capital (UK) Ltd entered formal administration on 22 March 2021, meaning an external administrator was appointed to manage the company's assets and liabilities.
> 
> **Why it matters:**
> This signals the company could not meet its obligations and creditors (including any you may have outstanding with them) are now at risk. Administration is a formal insolvency process where an administrator takes control, typically leading to asset sales or liquidation. Any outstanding invoices, deposits or contractual commitments with this company are unlikely to be recovered in full.
> 
> **Suggested action:**
> Check your exposure to this company immediately — verify any open invoices, prepayments or ongoing contracts — and contact the appointed administrator to register as a creditor in the insolvency process.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 4 · assigned **Critical** (match) · hallucination: False  
> _Accurate, appropriately urgent summary of the administration appointment with sound creditor guidance, though it could have added explicit instruction to halt further credit or new business immediately._

**Sonnet**

> **What happened:** On 22 March 2021, Greensill Capital (UK) Ltd was placed into administration, with administrators formally appointed to take control of the company's affairs.
> 
> **Why it matters:** This is a critical, formal insolvency event confirming the company is no longer trading normally and control has passed to insolvency practitioners; any outstanding payments, contracts, or supply arrangements with this entity are now at high risk and subject to the administration process rather than normal commercial terms.
> 
> **Suggested action:** Immediately freeze any new credit or trading exposure to this entity, review and cease reliance on existing contracts or receivables with them, and contact the appointed administrators (via the Companies House filing or Gazette notice) to register any claims.

*Judge:* overall **5/5** · factual 5 · interp 5 · action 5 · assigned **Critical** (match) · hallucination: False  
> _Accurate, appropriately urgent summary of the administration appointment with concrete, well-targeted credit actions._

---
