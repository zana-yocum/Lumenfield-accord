# Seed Data — Load Runbook

Synthetic dataset for Lumenfield Home Energy. 1,656 records, roughly 3.2 MB of the 5 MB Developer Edition allowance, leaving headroom for cases, tasks, and everything Phases 6 through 9 add.

Every name, address, and dollar figure is invented. No real customer data appears here.

---

## Before you load

**1. Delete the Developer Edition sample data.** Accounts like Edge Communications and Burlington Textiles, plus their contacts, opportunities, cases, and leads. A reviewer clicking through the org should never see them next to Lumenfield records.

**2. Add `Legacy_Id__c` to five objects** — Text(20), External ID, Unique, case sensitive:

| Object | Why |
|---|---|
| Account | Parent for statements, promises, adjustments |
| Contact | Needed for the primary contact second pass |
| Opportunity | Parent for commitments |
| Service Contract | Referenced by statements and commitments |
| Billing Statement | Parent for payments, referenced by promises and adjustments |

Description on each: *Migration identifier from the seed dataset. Lets child records resolve their parent at load time without Salesforce IDs. See D-09.* Hide it from all page layouts.

**3. Restart Data Loader** if it was already open when you created the Legacy Id fields. It won't see them otherwise.

**4. Do not build validation or duplicate rules yet.** They fire on data loads and would reject the seeded defects, which are the entire point. Rules come after the baseline measurement.

---

## Load order

Parents before children. Use Data Loader with **Insert** for files 1 through 12, and **Update** for the two marked as passes.

| # | File | Object | Operation | Records |
|---|---|---|---|---|
| 1 | `01-accounts.csv` | Account | Insert | 100 |
| 2 | `02-contacts.csv` | Contact | Insert | 135 |
| 3 | `03-accounts-primary-contact-update.csv` | Account | **Upsert** on `Legacy_Id__c` | 95 |
| 4 | `04-opportunities.csv` | Opportunity | Insert | 100 |
| 5 | `05-commitments.csv` | Commitment | Insert | 31 |
| 6 | `06-service-contracts.csv` | Service Contract | Insert | 100 |
| 7 | `07-commitments-service-contract-update.csv` | Commitment | **Upsert** on `Legacy_Id__c` | 31 |
| 8 | `08-billing-statements.csv` | Billing Statement | Insert | 570 |
| 9 | `09-payments.csv` | Payment | Insert | 518 |
| 10 | `10-promises-to-pay.csv` | Promise to Pay | Insert | 60 |
| 11 | `11-adjustments.csv` | Adjustment | Insert | 12 |
| 12 | `12-leads.csv` | Lead | Insert | 30 |

Files 3 and 7 are second passes, and they exist because of circular references — an account points at a contact that points back at the account, and a commitment can't reference a service contract that doesn't exist when the commitment loads. Standard migration practice rather than a workaround.

---

## Loading with the Salesforce CLI

Headers are exact API names, so the CLI's bulk import needs no mapping at all. This is the fastest path and avoids Data Loader's mapping dialog entirely.

```
sf data import bulk --sobject Account --file data/01-accounts.csv -o lumenfield --wait 10
sf data import bulk --sobject Contact --file data/02-contacts.csv -o lumenfield --wait 10
sf data import bulk --sobject Opportunity --file data/04-opportunities.csv -o lumenfield --wait 10
sf data import bulk --sobject Commitment__c --file data/05-commitments.csv -o lumenfield --wait 10
sf data import bulk --sobject ServiceContract --file data/06-service-contracts.csv -o lumenfield --wait 10
sf data import bulk --sobject Billing_Statement__c --file data/08-billing-statements.csv -o lumenfield --wait 10
sf data import bulk --sobject Payment__c --file data/09-payments.csv -o lumenfield --wait 10
sf data import bulk --sobject Promise_to_Pay__c --file data/10-promises-to-pay.csv -o lumenfield --wait 10
sf data import bulk --sobject Adjustment__c --file data/11-adjustments.csv -o lumenfield --wait 10
sf data import bulk --sobject Lead --file data/12-leads.csv -o lumenfield --wait 10
```

Relationship columns use `Object:External_Id__c` for standard lookups and `Relationship__r:External_Id__c` for custom ones. The Bulk API resolves the parent by External ID at insert time.

If a job fails, the error detail comes from:

```
sf data bulk results -o lumenfield --job-id <the id it printed>
```

**Files 03 and 07 are upserts** and aren't part of this sequence. File 03 sets the primary contact on each account; file 07 links commitments to their service contract. Both are handled better by flows in Phase 7, where the same logic also covers records created after the load. See open items.

**Record types:** the `RecordType` column was removed, since the API needs an ID rather than a name. After loading, set the twelve organization accounts with a list view mass update — filter for names containing HOA, LLC, or Association.

**If you use Data Loader instead**, map each `*:Legacy_Id__c` column to the field entry labeled **(Legacy Id)** — never the plain lookup, which expects a Salesforce record ID and fails with MALFORMED_ID.

**Dates are ISO format** (`2026-09-27`), which both tools read natively.

## What's in the data

**Delinquency spread**, which is what makes the aging reports and priority scoring meaningful:

| Bucket | Accounts |
|---|---|
| Current | 70 |
| 1–30 days | 12 |
| 31–60 days | 8 |
| 61–90 days | 6 |
| 90+ days | 4 |

**Promise outcomes:** 32 kept, 16 broken, 8 active, 4 pending approval. Some broken promises carry a partial payment, which is the case US-04 has to handle.

**Commitments** land on 31 of the 100 closed deals, spread across four sales reps unevenly — one carries noticeably more than the others, so the root cause reporting in US-10 shows a pattern rather than noise.

**Twelve organization accounts** — HOAs and property managers — exercise the second Account record type.

---

## Seeded defects

33 deliberate problems across 7 categories, listed record by record in `seeded-defects.csv`. Don't open that file until after you've measured the baseline; the point is to find them with reports, not a cheat sheet.

| Defect | Count |
|---|---|
| Duplicate contacts, name and email variants | 6 |
| Accounts with no primary contact | 5 |
| Contacts missing role on agreement | 10 |
| Placeholder or typo email domains | 3 |
| Account status says Current while the account is past due | 3 |
| Promises with no related statement | 4 |
| Statements with a due date before the statement date | 2 |

That fifth one matters most. Account Status drives the sharing rule from D-08, so a stale status means a collections rep can't see an account they're supposed to be working. It isn't a hygiene problem, it's an access problem, and it's the one worth leading with in the case study.

---

## After the load

1. Spot-check ten accounts. Balances, days past due, and DPD buckets should populate on their own — those are roll-ups and formulas doing their work with no automation involved.
2. Build the five data quality reports and the dashboard. **Screenshot the baseline before fixing anything.**
3. Build matching rules, duplicate rules, and validation rules.
4. Clean the defects.
5. Screenshot the dashboard again.

Three accounts will still show a status that doesn't match their aging after cleanup, and that's correct — the stamping flow that fixes them permanently is Phase 7. A data quality problem solved by automation rather than by hand is the better ending.
