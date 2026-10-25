## v1.0.1 — 2026-10-14 — System test and DEF-01

The UAT scripts were run as an evidenced system test through the API (admin-run; not UAT with outside users). 12 scripts pass, one after a same-night fix. Full results: `docs/system-test-results-2026-10-14.md`.

### Fixed
- **DEF-01 (High): posted credits didn't reduce the statement balance.** A customer credited in full stayed past due and on the work list. Added `Billing_Statement__c.Credits_Applied__c`, new flow `Adjustment_AfterSave_ApplyCredits` (sums posted adjustments onto the statement; marks it Paid when cleared and no dispute is open), and `Balance__c` = `MAX(0, due − paid − credits)`. Five seeded credits backfilled. Retested: $214.29 statement → $139.29 → $0 → Paid; account off the work list.
- **OBS-01 (Low): deleting an active promise left the collection hold in place.** Delete on Promise to Pay removed from `PS_Collections_Core`, the only permission set that granted it; Cancelled is the supported exit.

### Changed
- UAT-11 and the quick reference used an adjustment type that doesn't exist ("Credit"); corrected to Billing Correction / Goodwill Credit / Production Guarantee
- UAT-21 no longer expects a follow-up task the requirement doesn't call for

### Process
- An AI-generated "all scripts passed" UAT summary was checked against the org before being recorded, and rejected: no test records existed for the scripts it reported. Pass/fail in this repo comes only from evidence in the org.

### Known limits added
- Credits don't carry forward past $0 on a statement; deleting a posted credit doesn't recalculate (record-triggered flows can't run after delete)
