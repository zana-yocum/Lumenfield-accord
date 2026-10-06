## v0.4 — 2026-10-03 — Phase 5: Data load and data quality

Synthetic Lumenfield dataset loaded, data quality baseline measured, integrity rules built, and the defects a person should fix, fixed. The two defects automation should fix are left for Phase 7 on purpose.

### Added
- `Legacy_Id__c` External ID fields on Account, Contact, Lead, Opportunity, Service Contract, and Billing Statement, so child records reference parents by stable source IDs instead of Salesforce IDs (D-09)
- Seed dataset loaded via Salesforce CLI bulk import (D-10): 100 accounts, 135 contacts, 100 opportunities, 31 commitments, 100 service contracts, 570 billing statements, 518 payments, 60 promises to pay, 12 adjustments, 30 leads
- Contact matching rule: exact email, plus fuzzy first name with exact last name and account
- Duplicate rule `Contact_Duplicates_Alert` — **alert, not block**, so co-signers sharing a household email can still be saved
- Five validation rules, each with a description tied to its user story and an error message that names the fix:
  - `VR_Statement_DueAfterStatementDate` (Billing Statement)
  - `VR_Payment_AmountPositive` (Payment, US-04)
  - `VR_Payment_DateNotFuture` (Payment, US-04)
  - `VR_Promise_AmountPositive` (Promise to Pay, US-03)
  - `VR_Adjustment_RejectionReason` (Adjustment, US-11)
- **Data Quality** dashboard with five source reports in shared folders (`DataQuality`, `DataQualityDashboard`). Metric tiles use color ranges: zero reads green, open defects read red.

### Changed
- Standard Contact Duplicate Rule deactivated in favor of the custom alert rule. Retrieved into the repo so its inactive state is on record.
- Duplicate contacts component sorted by record count descending, so any email held by more than one contact rises to the top. A top bar of 1 means no duplicates.

### Fixed
- Six seeded duplicate contact pairs merged
- 16 contacts missing a role on agreement filled
- Two billing statements with a due date before the statement date corrected
- Two `noemail@example.com` placeholder emails cleared at the source rather than merged — they belonged to two different customers on two different accounts, and merging would have combined their payment and dispute history
- One `.cm` typo domain corrected to `.com`

### Removed
- All Developer Edition sample data: sample accounts and opportunities, 22 sample leads, the Sample Account for Entitlements and its entitlement, 17 GenWatt products, 10 sample solutions, 4 sample campaigns, and a non-standard sample price book. The Standard Price Book stays for Phase 8.
- Two unused report copies left over from dashboard building

### Data quality, before → after

| Metric | Before (2026-09-30) | After (2026-10-03) |
|---|---|---|
| Duplicate contact pairs | 7 flagged (6 real, 1 placeholder false positive) | 0 |
| Contacts missing agreement role | 16 | 0 |
| Statement date errors | 2 | 0 |
| Accounts invisible to collections (status mismatch) | 3 | 3 — Phase 7 status-stamping flow |
| Residential accounts with no primary contact | 88 | 88 — Phase 7 backfill flow |

### Known, deliberately deferred
- `VR_Account_PrimaryContactRequired` is not built yet. Active now, it would block every edit to all 88 residential accounts. It activates after the Phase 7 backfill and once Account record types exist.
- The primary contact gap comes from a load limitation, not from bad source data: Data Loader didn't expose that relationship by External ID. Full load history in `docs/data-plan.md`.
