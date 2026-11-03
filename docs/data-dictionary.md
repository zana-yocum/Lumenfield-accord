# Data Dictionary — Accord

Every custom field, what it's for, and how it's configured. Written as the build plan in Phase 3 and checked against the org on 2026-11-03: field lists, types, picklist values and formulas match the org, and where the build departed from the plan the entry says so.

The description column summarizes each field's description in Setup. Per `conventions.md`, every field has one; five that didn't were filled in on 2026-11-03.

**Legacy Id.** Account, Contact, Opportunity, Service Contract, Billing Statement, Case and Lead each carry `Legacy_Id__c` (Text 20, External ID, unique): the seed dataset's identifier, kept so the data can be reloaded (D-09). Product2 has one too, though the org has no products. They're left out of the tables below.

---

## Account

Record types: **Residential Agreement**, **Organization**

| Field | API name | Type | Description (paste into Setup) |
|---|---|---|---|
| Primary Contact | `Primary_Contact__c` | Lookup (Contact) | The person automation contacts, since a household can have two people on the lease (D-01). Stamped by `Contact_AfterSave_StampPrimaryContact`; required on Residential Agreement accounts that aren't closed, after the first save (`VR_Account_PrimaryContactRequired`). |
| Current Balance | `Current_Balance__c` | Roll-up (SUM of Billing Statement Balance) | Total owed across all statements. Drives the collections panel in US-01. |
| Past Due Balance | `Past_Due_Balance__c` | Roll-up (SUM of Balance, filter Status = Past Due) | What's actually late. Filter requires the stamped status field, not a formula. |
| Oldest Past Due Date | `Oldest_Past_Due_Date__c` | Roll-up (MIN of Due Date, filter Status = Past Due) | Anchor for days past due. |
| Days Past Due | `Days_Past_Due__c` | Formula (Number) | `TODAY() - Oldest_Past_Due_Date__c`. Zero when nothing is past due. |
| DPD Bucket | `DPD_Bucket__c` | Formula (Text) | Current, 1-30, 31-60, 61-90, 90+. Groups the Past Due by DPD Bucket report. The default threshold in US-15 compares Days Past Due itself with `Default_Threshold_DPD`. |
| Collection Hold Until | `Collection_Hold_Until__c` | Date | Set by an approved promise. Outreach and escalation skip this account through this date, per US-03. |
| Do Not Contact | `Do_Not_Contact__c` | Checkbox | Customer asked for no further contact. Suppresses every channel, per US-21. Set by US-06, never by automation. |
| Account Status | `Account_Status__c` | Picklist | Current, Delinquent, Hardship Review, Default Review, Closed. |
| Broken Promises (90d) | `Broken_Promises_90d__c` | Number | Rolling count stamped nightly. Can't be a roll-up — filter criteria can't use a dynamic date. |
| Priority Score | `Priority_Score__c` | Formula (Number) | Ranks accounts for the rep work list. Weighted `(Days Past Due × 2) + (Past Due Balance ÷ 50) + (Broken Promises 90d × 25)` — aging matters most, every $50 owed adds a point, a broken promise costs about two weeks of aging. Weights are a judgment call and should be tuned against what reps actually collect on. US-05. |
| High Value | `High_Value__c` | Checkbox | A supervisor's flag for an account worth extra attention, on the Residential Agreement layout. Planned to escalate breach alerts (US-14); not built, so no automation reads it. |
| Threshold Crossed Date | `Threshold_Crossed_Date__c` | Date | Stamped when the account first crosses the default threshold. The clock US-15 audits against. |

---

## Contact

| Field | API name | Type | Description |
|---|---|---|---|
| Role on Agreement | `Role_on_Agreement__c` | Picklist | Primary, Co-signer, Authorized Third Party. Determines who automation can contact and who a rep may discuss the account with. |
| Individual | `IndividualId` | Standard lookup | Appears once Data Protection and Privacy is enabled. Unused: no contact is linked to an Individual, because no promotional automation exists yet (D-05, `data-model.md`). |

---

## Opportunity

| Field | API name | Type | Description |
|---|---|---|---|
| Concession Offered | `Concession_Offered__c` | Picklist (Yes/No) | Whether anything was promised at signing. Drives the validation rule in US-02. |
| Commitment Count | `Commitment_Count__c` | Roll-up (COUNT of Commitment) | Lets the validation rule see child records. The reason Commitment is master-detail. |
| Commitment Value | `Commitment_Value__c` | Roll-up (SUM of Commitment Value) | Total promised. Flags deals above rep authority. |
| Service Address | `Service_Address__c` | Text (255) | Where the system goes. Carried to the Service Contract at close. |

---

## Service Contract (standard)

| Field | API name | Type | Description |
|---|---|---|---|
| Activation Date | `Activation_Date__c` | Date | System activation. Starts the welcome touch scheduled path in US-19. |
| PTO Date | `PTO_Date__c` | Date | Permission to operate from the utility. Billing before this date is a dispute reason in US-07. |
| First Due Date | `First_Due_Date__c` | Date | First payment due. Anchors the reminder in US-20. |
| Monthly Payment | `Monthly_Payment__c` | Currency | Base lease payment. |
| Escalator Rate | `Escalator_Rate__c` | Percent | Annual increase. The dispute reason behind Annual Escalator Increase. |
| System Size kW | `System_Size_kW__c` | Number (2 dp) | Used with production estimates when a customer disputes output. |
| Estimated Annual Production | `Est_Annual_Production_kWh__c` | Number | The estimate a production-shortfall dispute is measured against. |
| Welcome Sent On | `Welcome_Sent_On__c` | Date | Stamped when the welcome touch sends. Prevents duplicates on reactivation, per US-19. |

---

## Commitment `Commitment__c`

Master-detail → Opportunity · Auto-number `COM-{00000}`

| Field | API name | Type | Description |
|---|---|---|---|
| Account | `Account__c` | Lookup (Account) | Stamped from the opportunity by `Commitment_BeforeSave_StampAccount`, so commitments show on the account page where servicing works. Read-only to every persona. Added for DEF-07. |
| Type | `Type__c` | Picklist (global value set) | Payment Coverage, Promotional Credit, Delayed Billing Start, Referral Bonus, Other. |
| Value | `Value__c` | Currency | Dollar value of what was promised. Blank for non-monetary terms. |
| Months Covered | `Months_Covered__c` | Number | For payment coverage commitments. |
| Terms | `Terms__c` | Long Text (1000) | What was actually said, in the rep's words. This is the field a dispute specialist reads first. |
| Service Contract | `Service_Contract__c` | Lookup (Service Contract) | Set at Closed Won so service and collections can see the commitment. |
| Status | `Status__c` | Picklist | Recorded, Applied, Expired, Disputed. |
| Recorded By | `Recorded_By__c` | Lookup (User) | Who entered it. Makes the pattern reportable by rep, per US-10. |

Files are attached to the record for signed evidence.

---

## Billing Statement `Billing_Statement__c`

Master-detail → Account · Auto-number `STMT-{00000}`

| Field | API name | Type | Description |
|---|---|---|---|
| Service Contract | `Service_Contract__c` | Lookup | Which agreement this bills for. |
| Statement Date | `Statement_Date__c` | Date | Billing date. |
| Due Date | `Due_Date__c` | Date | Payment due. |
| Amount Due | `Amount_Due__c` | Currency | Billed amount. |
| Amount Paid | `Amount_Paid__c` | Roll-up (SUM of Payment Amount) | Total received against this statement. |
| Credits Applied | `Credits_Applied__c` | Currency | Total of posted adjustments against this statement, kept by `Adjustment_AfterSave_ApplyCredits`. A lookup can't roll up, so a flow sums them. Added for DEF-01. |
| Balance | `Balance__c` | Formula (Currency) | `MAX(0, Amount_Due__c - Amount_Paid__c - Credits_Applied__c)`. Credits came in with DEF-01. |
| Status | `Status__c` | Picklist | Open, Past Due, In Dispute, Paid, Written Off. A stored field, not a formula, because the account roll-ups filter on it and roll-up filters can't use dynamic formulas. Kept current each morning by `Billing_Statement_Daily_Status`, which was missing until DEF-12. |
| Days Past Due | `Days_Past_Due__c` | Formula (Number) | Statement-level aging for reports. |
| Dispute Open | `Dispute_Open__c` | Checkbox | Stamped when a dispute case opens. Suppresses the reminder in US-20. |
| Date Integrity Issue | `Date_Integrity_Issue__c` | Formula (Checkbox) | Due date before the statement date. Feeds the Data Quality dashboard; `VR_Statement_DueAfterStatementDate` stops new ones. |

---

## Lease Payment `Payment__c`

Master-detail → Billing Statement · Auto-number `PAY-{00000}` · Labelled Payment in the plan; relabelled Lease Payment on 2026-10-14

| Field | API name | Type | Description |
|---|---|---|---|
| Amount | `Amount__c` | Currency | Amount received. |
| Payment Date | `Payment_Date__c` | Date | When it posted. |
| Method | `Method__c` | Picklist | ACH, Card, Check, Other. |
| External Reference | `External_Reference__c` | Text (64), External ID, Unique | Processor reference. Unused in this build; the hook the next project's integration writes to. |

---

## Promise to Pay `Promise_to_Pay__c`

Master-detail → Account · Auto-number `PTP-{00000}`

| Field | API name | Type | Description |
|---|---|---|---|
| Promise Date | `Promise_Date__c` | Date | When the customer said they'd pay. |
| Promise Amount | `Promise_Amount__c` | Currency | What they committed to. |
| Amount Received | `Amount_Received__c` | Currency | Stamped when the promise is evaluated. Retained on broken promises so partial payment is visible, per US-04. |
| Status | `Status__c` | Picklist | Active, Pending Approval, Kept, Broken, Cancelled. |
| Grace Ends | `Grace_Ends__c` | Formula (Date) | Promise date plus the grace period. When the nightly evaluation judges it. |
| Related Statement | `Related_Statement__c` | Lookup (Billing Statement) | Which bill the promise covers. |
| Out of Policy | `Out_of_Policy__c` | Formula (Checkbox) | Flags a promise falling short of the past-due balance or extending beyond the policy window. `OR(Promise_Amount__c < Account__r.Past_Due_Balance__c, Promise_Date__c - TODAY() > $CustomMetadata.Policy_Setting__mdt.Promise_Window_Days.Number_Value__c)`. Routes to approval instead of applying a collection hold. US-03. |

---

## Adjustment `Adjustment__c`

Master-detail → Account · Auto-number name, `ADJ-{00000}` (Adjustment Number), since 2026-11-03. It was built as plain text, so the 12 seeded adjustments still show their record IDs until the next re-age rebuilds them (`data-model.md`, Gotchas)

| Field | API name | Type | Description |
|---|---|---|---|
| Case | `Case__c` | Lookup (Case) | The dispute this resolves, when there is one. |
| Billing Statement | `Billing_Statement__c` | Lookup | Which bill it applies to. |
| Amount | `Amount__c` | Currency | Credit amount. |
| Type | `Type__c` | Picklist | Goodwill Credit, Billing Correction, Production Guarantee, Write-off. |
| Status | `Status__c` | Picklist | Draft, Pending Approval, Approved, Rejected, Posted. |
| Rejection Reason | `Rejection_Reason__c` | Text (255) | Required when rejected. Exists because native approval comments can't be made mandatory, per US-11. |
| Posted Date | `Posted_Date__c` | Date | When the credit actually applied. |

---

## Case

Record types: **Billing Dispute**, **Default Review**

| Field | API name | Type | Description |
|---|---|---|---|
| Dispute Reason | `Dispute_Reason__c` | Picklist (global value set) | Billing Started Before Activation, Production Below Estimate, Promised Credit Not Applied, Duplicate or Unauthorized Draft, Payment Not Posted, Annual Escalator Increase, Home Sale or Transfer, Outage or Repair Credit. |
| Root Cause | `Root_Cause__c` | Picklist (global value set) | Required at close, per US-10. Includes Customer Misunderstanding — No Company Error, so the data stays honest. |
| Resolution Summary | `Resolution_Summary__c` | Long Text (2000) | What was decided and why. |
| Disputed Statement | `Disputed_Statement__c` | Lookup (Billing Statement) | The bill in question. |
| Service Contract | `Service_Contract__c` | Lookup | The agreement, and how the entitlement attaches. |
| Originating Opportunity | `Originating_Opportunity__c` | Lookup (Opportunity) | Set when the root cause is a missing concession. Makes the pattern reportable by rep. |
| Sales Input Requested | `Sales_Input_Requested__c` | Date/Time | When the sales rep was added to the case team, per US-08. |
| Threshold Crossed Date | `Threshold_Crossed_Date__c` | Date | Default Review only. Copied from the account at creation. |
| Review Opened On Time | `Review_Opened_On_Time__c` | Formula (Checkbox) | Whether the default review opened inside the policy window. `AND(NOT(ISBLANK(Threshold_Crossed_Date__c)), DATEVALUE(CreatedDate) - Threshold_Crossed_Date__c <= $CustomMetadata.Policy_Setting__mdt.Default_Review_Window_Days.Number_Value__c)`. The audit metric in US-15. |

---

## Lead

| Field | API name | Type | Description |
|---|---|---|---|
| Service Address | `Service_Address__c` | Text (255) | Where the system would go. Drives territory assignment. |
| Service Area | `Service_Area__c` | Picklist | Assignment rule input, per US-16. |
| Inquiry Detail | `Inquiry_Detail__c` | Long Text (500) | What they typed in the web form. |

---

## Custom metadata

### `Policy_Setting__mdt`

One record per threshold from the requirements policy table.

| Field | API name | Type |
|---|---|---|
| Number Value | `Number_Value__c` | Number (2 dp) |
| Text Value | `Text_Value__c` | Text (255) |
| Notes | `Notes__c` | Text (255) |

Records: `Promise_Window_Days` (30) · `Promise_Grace_Days` (3) · `Contact_Attempt_Threshold` (3) · `Rep_Credit_Limit` (100) · `Supervisor_Credit_Limit` (500) · `Default_Threshold_DPD` (90) · `Default_Review_Window_Days` (3) · `Welcome_Offset_Days` (7) · `Pre_Due_Offset_Days` (7). Values as in the org on 2026-10-25.

Steward adds three records of its own, kept in Steward's repository: `Self_Service_Broken_Promise_Limit` (2) and `Self_Service_Min_Coverage_Pct` (100) for ST-04, and `Production_Guarantee_Pct` (90) for ST-14.

### `Dispute_Evidence_Requirement__mdt`

| Field | API name | Type |
|---|---|---|
| Dispute Reason | `Dispute_Reason__c` | Text (100) |
| Evidence Item | `Evidence_Item__c` | Text (255) |
| Required | `Required__c` | Checkbox |

One record per reason-and-evidence pair. The dynamic checklist in US-07 reads these, which means adding a new dispute reason later is a data change, not a flow change.

---

## Global value sets

Shared across objects, and built before the picklist fields that use them:

- **Contact Outcome** — Right Party Contact, Third Party on Agreement, Wrong Number, No Answer, Left Voicemail, Promise Made, Refused to Pay, Disputed Balance, Requested No Further Contact, Hardship or Bankruptcy Mentioned
- **Dispute Reason** — as listed under Case
- **Root Cause** — Concession Not Recorded at Signing, Billing Start Date Error, Activation Date Mismatch, Production Shortfall — Equipment, Production Shortfall — Weather or Shading, Payment Posting Error, Duplicate Draft, Customer Misunderstanding — No Company Error
- **Commitment Type** — Payment Coverage, Promotional Credit, Delayed Billing Start, Referral Bonus, Other

---

## Formula reference

The formulas worth knowing by heart, because they carry the design decisions.

**Account.Days_Past_Due__c**
```
IF(ISBLANK(Oldest_Past_Due_Date__c), 0, TODAY() - Oldest_Past_Due_Date__c)
```

**Account.DPD_Bucket__c**
```
IF(Days_Past_Due__c = 0, "Current",
IF(Days_Past_Due__c <= 30, "1-30",
IF(Days_Past_Due__c <= 60, "31-60",
IF(Days_Past_Due__c <= 90, "61-90", "90+"))))
```

**Account.Priority_Score__c**
```
(Days_Past_Due__c * 2) + (Past_Due_Balance__c / 50) + (Broken_Promises_90d__c * 25)
```

**Billing_Statement__c.Balance__c**
```
MAX(0, Amount_Due__c - Amount_Paid__c - Credits_Applied__c)
```

**Billing_Statement__c.Days_Past_Due__c**
```
IF(AND(Balance__c > 0, Due_Date__c < TODAY()), TODAY() - Due_Date__c, 0)
```

**Promise_to_Pay__c.Grace_Ends__c**
```
Promise_Date__c + $CustomMetadata.Policy_Setting__mdt.Promise_Grace_Days.Number_Value__c
```

**Promise_to_Pay__c.Out_of_Policy__c**
```
OR(
  Promise_Amount__c < Account__r.Past_Due_Balance__c,
  Promise_Date__c - TODAY() > $CustomMetadata.Policy_Setting__mdt.Promise_Window_Days.Number_Value__c
)
```

**Case.Review_Opened_On_Time__c**
```
AND(
  NOT(ISBLANK(Threshold_Crossed_Date__c)),
  DATEVALUE(CreatedDate) - Threshold_Crossed_Date__c <= $CustomMetadata.Policy_Setting__mdt.Default_Review_Window_Days.Number_Value__c
)
```

Three of these read policy values from custom metadata rather than hardcoding them. Changing the grace period, the promise window, or the review window is a data edit, not a formula edit.
