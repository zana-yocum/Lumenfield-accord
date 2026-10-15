# Root Cause Analysis — Every statement showed a $0 balance

| | |
|---|---|
| Found | 2026-10-08, while preparing Phase 6 test cases |
| Severity | High. Every collections number in the org was wrong |
| Component | `Billing_Statement__c.Balance__c` (formula, currency) |
| Status | Fixed 2026-10-08; regression covered by UAT-01 and the supervisor dashboard |

---

## What happened

`Balance__c` on Billing Statement read **$0.00 on every one of 570 statements**, including statements that were plainly unpaid.

Because everything downstream is built on that one field, the error spread:

- Statement **Days Past Due** read 0, since it only counts when a balance remains
- The Account roll-ups **Current Balance** and **Past Due Balance** summed to **$0 across the whole book**
- **DPD Bucket** and **Priority Score** on Account had nothing to work with
- The Phase 7 status flow, the work list and the default review trigger would all have run against zeros

After the fix, the book showed about **$10,088 owed**.

## How it was found

Not by a report. While choosing statements to dispute for the Phase 6 test cases, a statement with an amount due and no payments showed a $0 balance. That was the thread. Opening the field definition showed the formula.

## Root cause

The formula was:

```
Amount_Paid__c - Amount_Paid__c
```

It should have been:

```
Amount_Due__c - Amount_Paid__c
```

A field picked from the Insert Field menu twice. Anything minus itself is zero, so the formula was syntactically valid, saved without a warning, and returned a believable number on every record.

## Why it got through

Four checks existed. None of them were looking at this.

| Check | Why it missed |
|---|---|
| Formula syntax check | The formula was valid. Syntax checking doesn't check intent |
| Phase 3 formula testing | The formula chain was checked with throwaway records, but without a hand-worked expected value to compare against. A result that looks like money passes a glance |
| Phase 5 data quality dashboard | Measured duplicates, completeness, status accuracy and date integrity. **Nothing measured balances.** A dashboard only catches the defects it was built to look for |
| Phase 5 load verification | Counted records, not values. 570 statements loaded is true whether their balances are right or not |

The most useful finding is the third row. The data quality baseline was presented as a complete picture of the data and it wasn't — it was a picture of the five defects that were seeded on purpose.

## Fix

1. Corrected the formula through the Tooling API (2026-10-08)
2. Roll-up summaries recalculated on their own; confirmed about $10,088 owed
3. Billing data regenerated anchored to the current date (a separate drift problem the zero balances had been hiding — see `RUNBOOK.md`)
4. Field retrieved into source so the corrected definition is under version control

## Prevention

| Change | Where |
|---|---|
| Every formula gets a known-answer test: one record where the expected result is worked out by hand first, then compared | `conventions.md`, testing section (added at release) |
| UAT-01 checks the actual balance on a known unpaid statement, not just that the field is populated | `docs/uat-scripts.md` |
| Total past due is a tile on the supervisor dashboard. A $0 there is now visible to the person who'd notice | Collections Supervisor dashboard |
| Load verification includes one sum, not just counts: total amount due minus total paid should match the source file | `data-plan.md`, load sequence |

## What this shows

The defect was trivial. Finding it depended on looking at one record with a person's eyes and asking whether the number made sense — and the formal checks had all passed. The fix took a minute; the prevention items are the part that matters.
