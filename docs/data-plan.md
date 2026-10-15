# Data Plan — Accord

The synthetic dataset, how it loads, and how data quality gets measured before and after cleanup.

All data is invented. No real customer information appears anywhere in this org.

---

## Volume budget

Developer Edition caps data storage at 5 MB and a typical record costs about 2 KB, so roughly 2,500 records is the ceiling. The dataset targets 2,050 and leaves headroom for cases, tasks, and everything Phases 6 through 9 add.

| Object | Records | Notes |
|---|---|---|
| Account | 120 | 110 Residential Agreement, 10 Organization (HOA and property managers) |
| Contact | 170 | 50 accounts carry a co-signer, matching D-01 |
| Opportunity | 130 | 120 Closed Won, 10 still open |
| Commitment | 45 | On about 38% of closed deals |
| Service Contract | 120 | One per residential account |
| Billing Statement | 800 | Monthly bills, count varies with activation date |
| Payment | 600 | Most statements paid, some partially, some not at all |
| Promise to Pay | 70 | Across delinquent accounts, mixed outcomes |
| Adjustment | 15 | Historical credits |
| Lead | 40 | Open pipeline for Phase 8 |
| **Total** | **2,110** | |

Cases load in Phase 6, once record types exist.

---

## Delinquency distribution

The shape matters more than the volume. A dataset where everyone is current proves nothing, and one where everyone is 90 days late isn't a business.

| Bucket | Accounts | Why |
|---|---|---|
| Current | 84 (70%) | The normal state |
| 1–30 DPD | 14 (12%) | First-payment misses, the US-20 population |
| 31–60 DPD | 10 (8%) | Active collections work |
| 61–90 DPD | 7 (6%) | Escalating |
| 90+ DPD | 5 (4%) | Crosses the default threshold, triggers US-15 |

Promise outcomes: 40 Kept, 20 Broken, 8 Active, 2 Pending Approval. The broken ones cluster on a handful of accounts so `Broken_Promises_90d__c` and the priority score have something real to rank.

Commitments concentrate on three sales reps, with one rep carrying a noticeably higher rate of undocumented concessions. That's what makes the US-10 root cause reporting show a pattern instead of noise.

---

## Seeded defects

Between 5 and 10% of records carry a deliberate problem, so data quality work has a real baseline to improve rather than a hypothetical one.

| Defect | Count | What it tests |
|---|---|---|
| Duplicate contacts — same person, name and email variants | 8 pairs | Matching and duplicate rules |
| Accounts with no primary contact | 6 | Required-field validation, and the US-19 failure path |
| Contacts with no role on agreement | 12 | Completeness reporting |
| Malformed email addresses | 4 | Why the welcome touch needs an error path |
| Account status inconsistent with actual aging — marked Current at 45 days past due | 3 | The status-stamping flow in Phase 7, and by extension the sharing rule that depends on it |
| Promises with no related statement | 5 | Orphaned child records |
| Statements with a due date before the statement date | 2 | Validation rule catch |

That fifth one is the interesting defect. Account Status drives the sharing rule from D-08, so a stale status isn't a data quality nuisance — it's a collections rep who can't see an account they should be working. Worth calling out explicitly in the case study.

---

## Load sequence

Parents before children, always.

1. Delete the sample data Developer Edition ships with — accounts, contacts, opportunities, leads, cases, products
2. Accounts
3. Contacts
4. Update Accounts with Primary Contact (second pass, since contacts don't exist on the first)
5. Opportunities
6. Commitments
7. Service Contracts
8. Update Commitments with Service Contract (second pass)
9. Billing Statements
10. Payments
11. Promises to Pay
12. Adjustments
13. Leads

The two-pass updates exist because of circular references — an account points at a contact that points back at the account. Standard migration practice, and worth naming as such rather than treating it as a workaround.

---

## Loading by External ID

Child records need a way to point at parents that doesn't require knowing Salesforce record IDs in advance.

Add a `Legacy_Id__c` text field, External ID, unique, to: **Account, Opportunity, Service Contract, Billing Statement**. Each record in the source files carries a stable identifier like `ACC-0001`, and children reference that instead of a Salesforce ID. Data Loader resolves the relationship at insert time.

Payment already has `External_Reference__c` as an External ID, so it doesn't need another.

See D-09 for why these fields stay in the org after the load rather than being deleted.

---

## Rules come after the load, not before

This order is deliberate and worth understanding.

Validation rules and duplicate rules fire on data loads. Building them first would block every seeded defect from loading, and the dataset would arrive clean — which defeats the entire exercise.

So:

1. **Load** the data with defects intact
2. **Measure** the baseline — duplicate rate, completeness, status accuracy
3. **Build** matching rules, duplicate rules, and validation rules
4. **Clean** the existing defects
5. **Measure** again

That sequence produces a real before-and-after number instead of an asserted one. It also mirrors what actually happens in a migration: data arrives, and the rules that should have existed get written afterward.

---

## Rules to build in this phase

Data integrity only. Process rules — the concession block, the promise policy check — belong to Phase 7.

**Matching and duplicate rules**
- Contact matching on email exact, plus fuzzy first name with exact last name and account
- Lead-to-Contact matching on email
- Duplicate rules set to **Allow with alert**, and report. Blocking would stop legitimate co-signer records that share a household email.

**Validation rules**

| Rule | Object | Logic |
|---|---|---|
| `VR_Statement_DueAfterStatementDate` | Billing Statement | Due Date must be on or after Statement Date |
| `VR_Payment_AmountPositive` | Payment | Amount greater than zero |
| `VR_Payment_DateNotFuture` | Payment | Payment Date not in the future |
| `VR_Promise_AmountPositive` | Promise to Pay | Promise Amount greater than zero |
| `VR_Account_PrimaryContactRequired` | Account | Residential Agreement record type, status not Closed, Primary Contact required |
| `VR_Adjustment_RejectionReason` | Adjustment | Rejection Reason required when Status is Rejected (US-11) |

Every error message names the fix, not the rule. "Enter a due date on or after the statement date" beats "Validation rule VR_Statement_DueAfterStatementDate failed."

---

## Data quality measurement

Five reports, one dashboard. The dashboard is the artifact; the reports feed it.

| Metric | Report | Baseline (2026-09-30) | After (2026-10-14) | Target |
|---|---|---|---|---|
| Duplicate contact rate | Contacts flagged by duplicate rules ÷ total contacts | **4.4% — 7 pairs flagged, 6 confirmed, 1 placeholder-email false positive** | **0 pairs** | Under 2% |
| Primary contact completeness | Residential accounts with a primary contact ÷ total | **0% (0 of 88)** — load gap, see note | **100%**, enforced by `VR_Account_PrimaryContactRequired` | 98% |
| Contact role completeness | Contacts with a role on agreement ÷ total | **88% (16 of 135 missing)** | **100%** | 95% |
| Status accuracy | Accounts where status matches DPD bucket ÷ total | **97% (3 of 100 wrong)** | **100%**, corrected nightly by `Account_Daily_Collections_Status` | 100% after Phase 7 |
| Statement date integrity | Statements failing the date rule | **2 of 570** | **0**, enforced by `VR_Statement_DueAfterStatementDate` | 0 |

Every target met. Phase 5 fixed what a person should fix (duplicates, roles, dates); Phase 7 fixed what automation should fix (status, primary contact), and keeps them fixed.

**Baseline captured 2026-09-30**, before any cleanup or rules. Dashboard screenshot: `phase05-data-quality-dashboard-before.png`.

**On the 0% primary contact baseline:** the seed file that set primary contacts couldn't load, because Data Loader didn't expose that relationship by External ID. The number is real, but its cause is a load gap rather than bad source data — and the Phase 7 flow that stamps primary contacts fixes existing and future accounts at once. Stated plainly rather than left to look like a data disaster.

**On the seventh duplicate pair:** six pairs were seeded. The seventh was two different customers on two different accounts who both carried the placeholder email `noemail@example.com`. A report grouping by email can't tell that apart from a real duplicate; a person reviewing the pair can. It was left unmerged and fixed at the source instead, by clearing the placeholder values — merging would have collapsed two customers' payment and dispute history into one record. It's also the evidence behind the duplicate rule alerting rather than blocking: a blocking rule would have stopped a legitimate customer from being saved.

**On the three status mismatches:** these accounts are past due, marked Current, and therefore excluded from the collections sharing rule. They're invisible to the people who should be working them. That's the clearest example in the build of data quality being an access problem, not a hygiene problem.

Status accuracy stays imperfect until the Phase 7 stamping flow exists, and that's the right answer — a data quality problem that automation fixes, rather than one someone corrects by hand forever.

---

## Screenshots

- `phase05-data-quality-dashboard-before.png`
- `phase05-duplicate-rule-config.png`
- `phase05-duplicate-alert-in-action.png` — the alert appearing on a real record beats the config screen
- `phase05-data-quality-dashboard-after.png`
- `phase05-data-loader-success.png` — the load results with counts

---

## What actually happened

The load took several attempts, and every failure was diagnosed from the job's error file rather than guessed at. Recorded here because this is what migrations actually look like, and because it's a better story than a load that worked the first time.

| Failure | Cause | Fix |
|---|---|---|
| All 100 accounts rejected | State and Country picklists were enabled; the source used plain state values | Switched to `BillingStateCode` and `BillingCountryCode` |
| Legacy Id missing in Data Loader | Data Loader caches the object schema at login | Restart after creating fields |
| `MALFORMED_ID` on every contact | Relationship column mapped to the plain lookup, which expects a Salesforce ID | Map to the External ID relationship entry instead |
| Primary contact update never resolved | Data Loader didn't expose that relationship by External ID | Deferred to a Phase 7 flow |
| `Field name not found` on several objects | The Bulk API needs exact API names; some files carried `Legacy_Id__c` on objects that don't have the field | Exact headers, and Legacy Id only on objects something references |
| Relationship syntax rejected | Data Loader takes `Account:Legacy_Id__c`; Bulk API 2.0 takes `Account.Legacy_Id__c` | Dot notation for the CLI |
| 69 of 100 opportunities rejected | Restricted picklist value stored as `No,` with a trailing comma | Corrected the value in Setup |
| 48 of 60 promises rejected | `Kept, Broken` entered as one picklist value instead of two | Split into separate values |
| All 30 leads flagged as duplicates | Standard duplicate rules ship active, and API inserts fail rather than prompt | Leads had loaded on an earlier attempt; the 22 extras were surviving sample data |

**Tool choice:** the load moved from Data Loader to the Salesforce CLI partway through. See D-10.

**The pattern worth keeping:** restricted picklists caught two data entry errors in the org's own configuration by refusing the data. That's the argument for restricting picklists, demonstrated rather than asserted.

---

## After the load

**Billing data was regenerated on 2026-10-08.** The original seed's statement series ended months before the load date, so unpaid statements aged past 90 days and 29 of 30 delinquent accounts landed in 90+. `data/regen/generate_billing.py` rebuilds statements, payments, promises and adjustments anchored to any date, and `data/regen/RUNBOOK.md` reloads them. Regenerated: 632 statements, 545 payments, 60 promises, 12 adjustments; buckets Current 52 · 1–30 14 · 31–60 10 · 61–90 7 · 90+ 5. Days Past Due counts from today, so rerun it before every demo or UAT session.

**A zero-balance formula went unnoticed through the load.** `Balance__c` subtracted a field from itself, so every statement read $0. Load verification counted records but didn't sum any values. Load verification now includes one control total: amount due minus amount paid across all statements should match the source file. See `rca-balance-formula.md`.

**Household names made unique on 2026-10-14.** The seed reused 26 surnames across up to seven accounts ("Coffey Household" seven times), which made search and record pickers ambiguous. All 88 residential accounts were renamed from their primary contact, e.g. "Patrick Boone Household." The seed CSVs in `data/` keep the original names; the regen generator doesn't touch names.

## Known limitations

- **Volume.** Two thousand records is not production scale, and nothing here tests what happens at two million. Roll-up recalculation, sharing recalculation, and report performance all behave differently at volume.
- **Defect realism.** Seeded defects are the ones chosen to be interesting. Real migrations surface problems nobody anticipated.
- **Storage.** The org uses 3 of its 5 MB. Room for UAT records, not for another full dataset.
- **No historical churn.** Every record is created at load time, so field history and audit trails start empty regardless of what the data says about the past.
