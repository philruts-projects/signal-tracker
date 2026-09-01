# Phase 6 — Evaluation results

Test cases: 12  ·  Models: Haiku vs Sonnet  ·  Judge: Opus

## Summary (average briefing-quality scores)

| Model | Factual | Usefulness | Clarity | Overall | Hallucinations | Scored |
|---|---|---|---|---|---|---|
| Haiku | 4.17 | 3.58 | 4.75 | 3.5 | 1/12 | 12/12 |
| Sonnet | 4.58 | 3.75 | 4.67 | 3.92 | 0/12 | 12/12 |

## Case-by-case

### 1. Direct Line Insurance Group plc — TM01 (2026-08-05)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Routine  
*Key facts:* Single director (Jane Elizabeth Adamson) departed; large healthy insurer; not distress on its own

**Haiku**

> Risk: Routine
> What happened: Jane Elizabeth Adamson stepped down as a director on 31 July 2026.
> Why it matters: Director changes are normal business events. This termination carries no inherent signal of distress—turnover happens regularly in large listed groups due to retirement, role changes or internal reorganisation.
> Suggested action: Confirm whether a replacement has been appointed and note any change in board composition or governance structure if material to your exposure.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate and clearly written, correctly framing a single director exit at a large insurer as routine, though the action step is fairly generic and 'stepped down' slightly overstates what a TM01 discloses about the reason._

**Sonnet**

> Risk: Routine
> 
> What happened: Direct Line Insurance Group plc filed a TM01 confirming the termination of Jane Elizabeth Adamson as a director, effective 31 July 2026.
> 
> Why it matters: Director changes at this level are a normal part of corporate governance and board turnover, and a single departure filing carries no inherent commercial risk signal on its own.
> 
> Suggested action: Note the change for your records; no immediate action is required unless combined with other adverse signals from this company.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate and clearly written with sensible context, though it could add value by noting the director's role and advising a watch for clustered board departures._

---

### 2. Marshmallow Financial Services Ltd — AP01 (2026-08-11)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Routine  
*Key facts:* New director (Emma Alley) appointed; growth-stage InsurTech; benign or positive

**Haiku**

> Risk: Routine
> 
> What happened: Ms Emma Alley was appointed as a director of Marshmallow Financial Services Ltd on 3 August 2026.
> 
> Why it matters: Director appointments are a normal part of business operations and governance. This is a standard staffing change with no immediate commercial concern.
> 
> Suggested action: Update your internal records and continue standard monitoring of the company's filings.

*Judge:* overall **4/5** · factual 5 · usefulness 3 · clarity 5 · hallucination: False  
> _Accurate and clearly written, but the analysis is generic boilerplate that adds no company-specific context (e.g. board build-out at a growth-stage insurer) beyond restating the filing._

**Sonnet**

> Risk: Routine
> 
> What happened: Marshmallow Financial Services Ltd appointed Ms Emma Alley as a director, effective 3 August 2026.
> 
> Why it matters: Director appointments are a normal part of company governance and do not, on their own, indicate any change in financial health or trading status; this is a routine administrative update to the company's officer record.
> 
> Suggested action: Note the new director on file for future reference; no immediate action is required.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, clearly written and correctly framed as routine, though the action step is generic and it misses context such as the company's growth-stage profile or board composition._

---

### 3. Admiral Group plc — AA (2026-08-27)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Routine  
*Key facts:* Interim accounts to 30 Jun 2026 filed; routine reporting; healthy

**Haiku**

> Risk: Routine
> 
> What happened: Admiral Group plc filed interim accounts for the six-month period ending 30 June 2026.
> 
> Why it matters: This is a standard regulatory filing showing the company's financial position halfway through the financial year. Interim accounts are a normal part of listed company disclosure and allow stakeholders to monitor performance in the current trading period.
> 
> Suggested action: Review the interim results against your credit, account and procurement parameters; no follow-up needed unless the financial position has changed materially since your last review.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate and clearly written summary of the interim accounts filing, though the suggested action is somewhat generic boilerplate._

**Sonnet**

> Risk: Routine
> What happened: Admiral Group plc filed interim annual accounts made up to 30 June 2026, a standard periodic filing with Companies House.
> Why it matters: This is a routine statutory filing reflecting normal reporting activity and does not itself indicate any change in financial health or business risk.
> Suggested action: No action needed beyond noting the filing on file; review the accounts if updated financial detail is required for ongoing credit or commercial assessment.

*Judge:* overall **4/5** · factual 4 · usefulness 4 · clarity 4 · hallucination: False  
> _Accurate and clear routine-filing summary with sensible next steps, though 'interim annual accounts' is a self-contradictory phrasing and the note adds little beyond the filing itself._

---

### 4. Extracover Ltd (Zego) — CS01 (2026-06-21)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Routine  
*Key facts:* Confirmation statement filed; administrative annual confirmation; no real signal

**Haiku**

> Risk: Routine
> 
> What happened: Extracover Ltd filed a confirmation statement on 21 June 2026 with updates to company information, covering the period to 12 June 2026.
> 
> Why it matters: This is the standard annual filing that all active UK companies must make to keep their Companies House record current. It confirms the company remains operational and its core details (directors, shareholders, registered address) are up to date.
> 
> Suggested action: No action required unless you have specific questions about the updates disclosed in the filing.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, clearly written summary of a routine confirmation statement with correct dates and a sensible no-action recommendation, though it could note that the 'with updates' variant may warrant a quick check of what changed._

**Sonnet**

> Risk: Routine
> 
> What happened: Extracover Ltd (Zego) filed its annual confirmation statement, made up to 12 June 2026, confirming that company details on record have been reviewed and include some updates.
> 
> Why it matters: This is a standard statutory filing that all UK companies must submit annually to confirm details such as directors, registered office and shareholders are current; the presence of "updates" simply means minor changes were noted, not a sign of financial or operational distress.
> 
> Suggested action: Note the filing on file and review the specific updates (e.g. via the linked filings) only if your due diligence process requires confirmation of unchanged counterparty details.

*Judge:* overall **5/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, clearly written summary that correctly frames the confirmation statement as routine and gives a proportionate, actionable next step._

---

### 5. Legal & General Group plc — SH01 (2026-08-18)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Routine  
*Key facts:* ~GBP 138m share allotment; routine capital activity at a healthy insurer

**Haiku**

> Risk: Routine
> 
> What happened: Legal & General Group plc allotted new shares worth £138.1m on 13 August 2026.
> 
> Why it matters: Share allotments are a normal part of corporate operations, typically used for employee schemes, acquisitions or capital management. This filing signals the company executed a planned capital action but carries no inherent concern.
> 
> Suggested action: No immediate action required; monitor for related filings that might clarify the purpose (such as regulatory announcements or updated shareholder registers).

*Judge:* overall **4/5** · factual 4 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, clearly written summary matching the filing's ~£138m allotment and date, with sensibly hedged context, though the stated purpose remains generic and the figure is presented as new shares issued rather than a statement of capital._

**Sonnet**

> Risk: Routine
> 
> What happened: Legal & General Group plc filed an SH01 notifying Companies House of a new allotment of shares, with share capital recorded at £138,072,807.475, dated 13 August 2026.
> 
> Why it matters: Share allotments are a normal corporate action (e.g. employee scheme issuance, small capital raises, or reorganisations) and this filing alone does not indicate financial distress or a change in control; it simply confirms an increase or adjustment to issued capital.
> 
> Suggested action: No immediate action needed beyond noting the updated capital position on file; review the next confirmation statement or annual accounts if more context on the purpose of the allotment is required.

*Judge:* overall **5/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, clearly written and appropriately hedged, with sensible next steps; examples of allotment purposes are flagged as possibilities rather than asserted facts._

---

### 6. Aviva plc — SH06 (2026-08-21)
*Rules verdict:* **Watch**  ·  *Ground-truth severity:* Watch  
*Key facts:* ~GBP 987m share cancellation; routine mechanism (buyback) but size warrants observation; check vs other factors; briefing should explain what a cancellation is and why firms do it

**Haiku**

> Risk: Watch
> 
> What happened: Aviva plc cancelled just under £987.3m of its own shares on 14 July 2026.
> 
> Why it matters: Share cancellations are routine capital management — the company is reducing its share capital after a buyback programme. This is a normal housekeeping step that doesn't signal financial distress, but it does mean fewer shares are in issue, which affects earnings per share calculations and ownership percentages for existing shareholders.
> 
> Suggested action: No immediate concern, but note the effective share count for any financial ratio analysis you're running on the company.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, clearly written summary that correctly explains the cancellation mechanism and its share-count implications, though the action step is thin and omits cross-checking against other filings or exposure factors._

**Sonnet**

> Risk: Watch
> 
> What happened: Aviva plc filed an SH06 confirming the cancellation of shares, with capital movements referencing a value of £987,319,303.62, effective from 14 July 2026.
> 
> Why it matters: Share cancellations are a routine part of capital management (e.g. buybacks or restructuring of share classes) and don't inherently signal financial distress, but any change of this scale to issued capital is worth noting for its effect on shareholder structure and reported equity base.
> 
> Suggested action: Note the filing on file and check Aviva's next confirmation statement or annual accounts to confirm the resulting share capital position, but no immediate commercial action is required.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate, well-hedged summary that explains what a share cancellation means and gives a sensible follow-up step, though it could note the buyback context and cross-check against other Aviva signals more explicitly._

---

### 7. London Capital & Finance plc — AA01 (2018-10-17)
*Rules verdict:* **Serious**  ·  *Ground-truth severity:* Serious  
*Key facts:* Third change of accounting reference date in ~15 months; repeated changes are an obfuscation/delay red flag; ~3 months before administration; the tool now detects the repetition and should call it Serious

**Haiku**

> Risk: Serious
> 
> What happened: London Capital & Finance plc changed its accounting reference date from 27 April 2018 to 26 April 2018 — a one-day shift — and filed this change on 17 October 2018, six months after the date it claims to have made the change.
> 
> Why it matters: A one-day accounting reference date change is unusual and suggests potential irregularities in financial period management. The six-month delay between the stated change date and the actual filing creates a significant gap that warrants investigation, as it may indicate financial reporting issues, internal control problems, or attempts to manage reporting timelines in ways that obscure the company's true financial position.
> 
> Suggested action: Contact the company directly to clarify the rationale for this change and request recent audited accounts and explanations of any reporting delays.

*Judge:* overall **2/5** · factual 2 · usefulness 3 · clarity 4 · hallucination: True  
> _Clearly written but misreads the made-up date as the date the change was decided and misses the crucial pattern of repeated accounting reference date changes._

**Sonnet**

> Risk: Serious
> What happened: London Capital & Finance plc changed its accounting reference date, shortening its period so the year now ends on 26 April 2018 instead of 27 April 2018.
> Why it matters: Shortening an accounting reference period, especially when it follows a prior shortening, can be used to delay statutory filing deadlines or adjust reporting periods around other events, and warrants closer scrutiny of the company's filing pattern and financial reporting timeline.
> Suggested action: Cross-check this filing against the company's upcoming accounts due date and any other recent filings to confirm whether reporting deadlines are being deferred, and flag for review before extending or renewing credit terms.

*Judge:* overall **4/5** · factual 4 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate on the dates and rightly flags the repeat shortening pattern, though it understates the history by not noting this is the third change in roughly 15 months._

---

### 8. Carillion plc — TM01 (2017-01-03)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Serious  
*Key facts:* Finance director (Richard John Adam) departed; loss of finance leadership at a strained company; ~1 year before collapse; elevate

**Haiku**

> Risk: Routine
> 
> What happened: Richard John Adam stepped down as a director of Carillion plc on 31 December 2016.
> 
> Why it matters: Director changes are a normal part of business operations and this filing simply records a departure. A single director leaving does not by itself signal financial or operational concern.
> 
> Suggested action: Check the company's board composition and any regulatory news to understand whether this was a planned transition or part of wider management changes.

*Judge:* overall **2/5** · factual 4 · usefulness 2 · clarity 4 · hallucination: False  
> _Accurate on the bare filing facts and clearly written, but it omits that Adam was the finance director and frames the departure as routine, stripping the briefing of the analytical value a credit team needs._

**Sonnet**

> Risk: Routine
> 
> What happened: Carillion plc filed a TM01 confirming that Richard John Adam ceased to be a director of the company effective 31 December 2016.
> 
> Why it matters: Director departures are a normal part of corporate governance and are routinely filed with Companies House; on its own, this filing does not indicate financial distress or operational disruption.
> 
> Suggested action: Note the change in your records and check the company's next confirmation statement or annual accounts to confirm the board composition remains stable.

*Judge:* overall **2/5** · factual 3 · usefulness 2 · clarity 4 · hallucination: False  
> _Filing details are stated correctly and the prose is clear, but it omits that Adam was the finance director and asserts without support that the departure signals nothing, yielding a generic and unhelpful action._

---

### 9. Carillion plc — TM01 (2017-07-10)
*Rules verdict:* **Routine**  ·  *Ground-truth severity:* Serious  
*Key facts:* CEO (Richard John Howson) departed; leadership exit ~6 months before collapse; elevate

**Haiku**

> Risk: Routine
> What happened: Richard John Howson ceased to be a director of Carillion plc on 10 July 2017.
> Why it matters: Director changes are a normal part of company operations. This filing simply records the departure and has no inherent commercial significance on its own.
> Suggested action: Check the company's updated director list to confirm continuity of leadership and identify any replacement appointments.

*Judge:* overall **2/5** · factual 3 · usefulness 2 · clarity 4 · hallucination: False  
> _Accurately states the name and date but fails to identify Howson as CEO and wrongly frames a top-level leadership exit as commercially insignificant, leaving the reader under-informed despite clear prose._

**Sonnet**

> Risk: Routine
> 
> What happened: Carillion plc filed a TM01 notice confirming the termination of Richard John Howson as a director, effective 10 July 2017.
> 
> Why it matters: Director departures are recorded routinely at Companies House and, on their own, are a normal part of corporate governance; this filing alone does not indicate financial distress or operational disruption.
> 
> Suggested action: Note the change in the company's director register and check subsequent filings or public announcements for context on the departure and any successor appointment.

*Judge:* overall **2/5** · factual 4 · usefulness 2 · clarity 4 · hallucination: False  
> _Accurately states the filing details and reads clearly, but fails to identify Howson as CEO or convey the significance of a top-leadership exit, and its framing as 'routine' with generic follow-up actions leaves the reader under-informed._

---

### 10. Carillion plc — MR01 (2017-10-27)
*Rules verdict:* **Serious**  ·  *Ground-truth severity:* Serious  
*Key facts:* New charge (secured borrowing) - one of a cluster of 5 in one week; company raising secured finance ~3 months before collapse; strong distress signal

**Haiku**

> Risk: Serious
> 
> What happened: Carillion plc registered a mortgage charge on 26 October 2017, securing borrowing against company assets.
> 
> Why it matters: A new secured charge signals the company is relying on asset-backed lending, which typically indicates tightening liquidity or difficulty accessing unsecured funding. Given the scale of Carillion's operations, this move warrants close attention to covenant compliance and the lender's terms, as enforcement could materially disrupt the business.
> 
> Suggested action: Obtain details of the charge amount, lender identity and security scope from the full deed filing, and monitor for additional charges or repayment pressures in forthcoming accounts.

*Judge:* overall **4/5** · factual 4 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate and clearly written with sensible follow-up actions, though it omits the charge number and the wider cluster of near-simultaneous charge registrations that sharpens the distress signal._

**Sonnet**

> Risk: Serious
> What happened: Carillion plc registered a new charge (charge number 037823790002) on 26 October 2017, securing borrowing against company assets via a deed.
> Why it matters: New secured charges signal fresh lending typically tied to increased borrowing needs or lender-imposed security requirements, which can indicate tightening liquidity or heightened creditor caution about repayment risk; this is a material event worth tracking alongside any other recent filings or news.
> Suggested action: Review Carillion's full charge register and recent filing history for related patterns (e.g., multiple charges, satisfactions, or credit notices), and consider requesting updated financial assurances or payment terms review before extending further credit or exposure.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 4 · hallucination: False  
> _Accurate and well-reasoned with sound actions, though it misses the wider cluster/distress context and the 'why it matters' sentence is overlong._

---

### 11. Greensill Capital (UK) Ltd — TM01 (2026-06-25)
*Rules verdict:* **Serious**  ·  *Ground-truth severity:* Serious  
*Key facts:* Founder (Alexander David Greensill) removed as director; founder departures always warrant a flag (PE deal / funding round / strategy or performance shift)

**Haiku**

> Risk: Serious
> What happened: Alexander David Greensill stepped down as a director of Greensill Capital (UK) Ltd on 17 June 2026.
> Why it matters: The departure of a founder or namesake director from a company bearing his name signals a material change in leadership and control. This is commercially significant as it may indicate shifts in strategy, ownership, or the company's operational direction, and warrants clarification on succession and continuity of management.
> Suggested action: Contact the company to confirm the reason for departure, identify the replacement director(s), and assess any impact on credit terms, account management or contract continuity.

*Judge:* overall **4/5** · factual 4 · usefulness 5 · clarity 5 · hallucination: False  
> _Accurate, clear and actionable on the founder's departure, though 'stepped down' implies a voluntary resignation the TM01 does not confirm._

**Sonnet**

> Risk: Serious
> What happened: Alexander David Greensill has ceased to be a director of Greensill Capital (UK) Ltd, effective 17 June 2026, as recorded in a TM01 filing lodged 25 June 2026.
> Why it matters: The departure of a director bearing the company's own name is a notable governance change that may signal shifts in control, strategy or ownership, and warrants closer scrutiny given the company's history and current standing.
> Suggested action: Review the company's latest confirmation statement and accounts, and check for any related filings (e.g. new appointments, registered office changes, or insolvency notices) before extending or renewing credit terms.

*Judge:* overall **4/5** · factual 5 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate and clearly written, with sensible checks suggested, though it only implies rather than states the founder link and the vague nod to 'the company's history and current standing' adds no verifiable substance._

---

### 12. Greensill Capital (UK) Ltd — AM01 (2021-03-22)
*Rules verdict:* **Critical**  ·  *Ground-truth severity:* Critical  
*Key facts:* Company entered administration Mar 2021; the failure itself; halt credit and assess exposure

**Haiku**

> Risk: Critical
> 
> What happened: An administrator has been appointed to Greensill Capital (UK) Ltd, placing the company into administration with a view to liquidation.
> 
> Why it matters: This is an insolvency event — the company is being wound down under formal court supervision. Any outstanding contracts, credit lines, or trading relationships with this entity are now at severe risk and subject to administrator control. Creditors and counterparties typically recover only a proportion of amounts owed, if anything.
> 
> Suggested action: If you have exposure to this company (outstanding invoices, deposits, guarantees, or active contracts), contact the appointed administrator immediately to register your claim and understand the process and timeline.

*Judge:* overall **4/5** · factual 4 · usefulness 4 · clarity 5 · hallucination: False  
> _Accurate and clearly written summary of the administration appointment, though it asserts court supervision as a given and omits the explicit step of halting further credit._

**Sonnet**

> Risk: Critical
> 
> What happened: Greensill Capital (UK) Ltd has entered administration, with an administrator formally appointed to take control of the company's affairs.
> 
> Why it matters: This is a formal insolvency event indicating the company is unable to meet its obligations as they fall due; normal trading, payments, and contract performance can no longer be relied upon, and creditors' recoveries will depend on the administration process.
> 
> Suggested action: Immediately suspend new credit or commitments to this entity, freeze any open exposures, and contact the appointed administrator to register your position as a creditor or counterparty.

*Judge:* overall **5/5** · factual 5 · usefulness 5 · clarity 5 · hallucination: False  
> _Accurately reflects the administrator appointment with no invented details, and gives clear, directly actionable credit-team steps._

---
