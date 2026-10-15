## v0.8 — 2026-10-14 — Phase 9: Analytics, and org cleanup

Eight collections reports, a supervisor dashboard, and a home page for the Collections Console. Reports and dashboard were built through the Analytics REST API and verified by running each one; the Data Quality dashboard now reads zero on every metric.

### Added — reports (folder `Collections`)
| Report | Shape | Answers | Stories |
|---|---|---|---|
| Collections Work List | Summary by Account Status, sorted by Priority Score | Who to call today. Excludes Do Not Contact and accounts on an active promise hold | US-05 |
| Past Due by DPD Bucket | Summary by bucket, sum of past-due balance | Where the money is aging | US-12 |
| Open Disputes by Status | Summary by status | Where disputes are stuck | US-12 |
| Resolved Disputes by Root Cause | Summary by root cause | What keeps causing disputes upstream | US-10, US-12 |
| Default Review Timeliness | Summary by Review Opened On Time | Did every 90+ account get a review in the window | US-15 |
| Promise Outcomes Last 90 Days | Summary by outcome, promised vs received | Kept rate and money actually collected | US-04, US-12 |
| Dispute Milestone Compliance 30 Days | Summary by Violation | SLA compliance | US-12, US-14 |
| Open Milestones Closest to Breach | Tabular, nearest target first | Which case breaches next | US-09, US-12 |

### Added — dashboard and home page
- **Collections Supervisor** dashboard (folder `Collections Dashboards`): three metric tiles (accounts to work today, total past due, open disputes) and seven charts (balance and accounts by bucket, disputes by status, milestone compliance, promise outcomes, review timeliness, root causes). Runs as the supervisor, a deliberate running-user choice rather than the admin.
- **Collections Home** Lightning home page: the supervisor dashboard plus the Default Reviews queue list, set as the Collections Console's home through an app-level page assignment. Replaces the default Sales home (quarterly performance, key deals) that reps were landing on.

### Changed — access
- Collections report and dashboard folders shared: **View** to VP Customer Operations and subordinates, **Edit** to the Collections Supervisor role.
- **Run Reports** added to `PS_Collections_Core` and `PS_Dispute_Management`. Without it, reps couldn't open their own work list. Create/customize reports stays with the supervisor and reporting permission sets.
- Collections Work List changed from tabular to summary (grouped by status). Lightning dashboards can't chart a tabular report without a row limit, and grouping by Delinquent vs Default Review is more useful to a rep anyway.

### Added — rule found missing
- `VR_Case_DisputeNeedsStatement` (US-07 criterion 4): a Billing Dispute can't save without the disputed statement. Found while writing UAT-07; no existing dispute lacked one. Tested: an API insert with no statement was refused with the field-level message.

### Changed — error messages
- Four Phase 5 validation rule messages reworded to name the fix rather than the problem, per `conventions.md`: "Enter a due date on or after the statement date" · "Enter an amount greater than zero. To reduce a balance, create a credit Adjustment instead" · "Enter today's date or earlier…" · "Enter a promise amount greater than zero."

### Org cleanup
- **88 household accounts renamed** from "Boone Household" to "Patrick Boone Household" style. 26 surnames repeated across up to seven accounts, which made search, lookups and record pickers ambiguous — the cause of the wrong-account debug run in Phase 7.
- Stray "Check" value removed from Commitment Status (no records used it); field description added.
- Sample "Delivery Status" link, 24 Developer Edition sample fields and 6 sample Account and Case layouts staged for deletion in `manifest/cleanup-fields` and `manifest/cleanup-layouts` (destructive deploys).

### Data quality, before → after (final)
| Metric | Before (2026-09-30) | After (2026-10-14) | Fixed by |
|---|---|---|---|
| Duplicate contact pairs | 7 flagged | 0 | Phase 5 merge and placeholder cleanup |
| Contacts missing agreement role | 16 | 0 | Phase 5 cleanup |
| Statement date errors | 2 | 0 | Phase 5 cleanup + `VR_Statement_DueAfterStatementDate` |
| Accounts invisible to collections (status mismatch) | 3 | 0 | `Account_Daily_Collections_Status` |
| Residential accounts with no primary contact | 88 | 0 | Backfill + `Contact_AfterSave_StampPrimaryContact` |

### Numbers on the day of release (re-aged data)
- 35 accounts on the work list; $10,618.80 past due across 35 accounts (Current 53 · 1–30 12 · 31–60 8 · 61–90 10 · 90+ 5)
- 10 open billing disputes; milestone compliance 18 of 26 (69%) over 30 days — the misses are the test disputes nobody worked between loads, which is exactly what the tile is for
- Promises, last 90 days: 8 Kept, 16 Broken, 3 Active; $1,879 received against $4,734 promised
- Default reviews opened on time: 0 of 5. All five accounts crossed 90 days before automation existed. The first review the scheduled flow opens on its own becomes the first "on time."

### Lessons recorded
- Report charts set through the Analytics API don't persist on the report, and a Donut chart in the create request returns a generic 500. Charts live on the dashboard components instead.
- `PATCH /analytics/reports/{id}` and `/analytics/dashboards/{id}` clear the description when it isn't in the body. Send it every time.
- Dashboard PATCH takes the metadata unwrapped; wrapping it in `dashboardMetadata` returns a JSON parse error.
- Dashboard component titles are limited to 40 characters.
- A dashboard created by cloning keeps an auto-generated API name. Cosmetic; recorded rather than chased.
