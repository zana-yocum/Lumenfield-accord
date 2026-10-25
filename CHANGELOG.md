# Changelog — Accord

Newest first. Each phase of the build is a version, v1.0 is the release, and later versions are fixes found in testing and in use. Entries record what changed in the org, how it was verified, and what went wrong.

## v1.0.2 — 2026-10-24 — Persona access fix, scheduled results, repository restored

A Steward hand check found that collections personas couldn't log a contact attempt. The scheduled checks left open by the system test have now run, and the repository has the metadata back that it lost in Phase 6.

### Fixed
- **DEF-08 (High): collections personas couldn't see Log Contact Attempt.** Found by Steward's Phase 5 hand check, the first time anyone used the console as a collections persona since the action was built. The action launches a screen flow, which needs the Run Flows permission or access to that flow. No persona had either, so Lightning hid the action, and US-06 didn't work for reps, specialists or supervisors. The fix is least privilege: version 3 of `Account_Screen_LogContactAttempt` restricts the flow to enabled permission sets, and `PS_Collections_Core` grants that one flow. Run Flows wasn't used, because it opens every current and future flow and this one runs in system context. Verified through the API; the console check is the rest of Steward's hand check. Details are in `docs/system-test-results-2026-10-14.md`.
- **DEF-07 written up.** Commitment's account lookup and `Commitment_BeforeSave_StampAccount` were built on Oct 14 at 8:48 PM CT and never recorded. This entry reconstructs them from the Setup Audit Trail, along with three other changes from the same evening:
  - payment fields removed from the Minimum Access profile
  - lead conversion rights for Sales Core
  - the supervisor role added to the Collections Team group

  DEF-02 to DEF-06 were never written down; the results doc explains. Still open: the Commitments related list on the account page.
- Permission set descriptions: four began with a stray "Description: ", and `PS_Sales_Core` and `PSG_Sales_Rep` cited US-17, which was cut. Corrected in the org.
- `Collection_Hold_Until__c` described as what it is — the hold date an in-policy promise sets and the daily evaluation clears — instead of repeating Do Not Contact's description. Found by Steward's persona-access check.

### Confirmed — scheduled runs, checked 2026-10-24
- **UAT-04 step 3:** six promises were set to Broken the morning after their grace date. Holds were released and Broken Promises (90d) went up.
- **UAT-14:** dispute 00001049's Acknowledge and Request Evidence milestones were flagged violated at their targets. Whether the email arrived is a check in the supervisor's inbox.
- **UAT-15:** ACC-0051 and ACC-0026 crossed 90 days past due on Oct 18 and 19. The nightly run opened a Default Review for each, owned by the queue and opened on time — the first two on-time reviews.

### Changed by Steward (2026-10-23)
- **Residential Agreement account layout:** Steward's Briefing and Follow-up Draft actions and the standard Email action added to the Lightning actions. They now read Briefing, Log Contact Attempt, Follow-up Draft, Email, Edit.
- **Billing Dispute case layout:** Steward's Dispute Summary action added first in the Lightning actions.
- **Collections Rep, Dispute Specialist and Collections Supervisor permission set groups:** Steward added `PS_Steward_Rep_Assistant` and `PS_Steward_Collections_Contact` to all three groups, and `PS_Steward_Dispute_Specialist` to the specialist and supervisor groups (Steward S-22). Accord's own permission sets are unchanged.
- **Found:** no persona could read a case's Subject, Description, AccountId or ContactId. Reps couldn't read a contact's Email, Phone or MobilePhone, or the account's Phone. Steward closes this for the collections personas (S-22).
- **Found:** `Collection_Hold_Until__c`'s description was a copy of `Do_Not_Contact__c`'s. Rewritten in the org 2026-10-24 (below).
- **Ownership:** from this point, those two layouts and three groups are maintained in Steward's repository and deployed by its pipeline. The copies here are snapshots; change them through Steward, or Steward's next deploy undoes the change.

### Repository
- **Metadata restored.** The Phase 6 commit (`d55887f`, 2026-10-07) deleted 655 files from `force-app`. Among them were every custom object, Accord's custom fields on standard objects, five permission sets, the permission set groups, the custom metadata records, the global value sets, the Account and Opportunity sharing rules, and the Data Quality reports and dashboard. The org wasn't affected; only the repository lost them. Accord's components were retrieved again from the org on 2026-10-24 (`manifest/accord.xml`).
- **Left out on purpose:** what's still missing from v0.4 is noise from that release's wildcard retrieve: standard fields and list views, empty sharing-rule files for 225 standard objects, Salesforce-managed groups, the nine sample roles deleted in Phase 6, and the deleted Developer Edition sample fields.
- **Placeholders:** nine files name an org user: the approval process, two dashboards, four folders and the two assignment rule files. Each carries a placeholder on `example.com` instead. Before deploying one of those files, put a real username back.
- **Tidying:**
  - Seven per-version changelog files folded into this one.
  - The Phase 5 bulk-load result files moved from the root to `data/load-results/`; scratch ID lists removed.
  - Steward's portal screenshots moved to Steward's repository.

### Corrected
- 13 flows, not 12. `Commitment_BeforeSave_StampAccount` came after the release docs.
- v1.0.1 said 12 scripts pass; it's 11. DEF-01's retest was counted twice.
- The README listed `docs/release-readiness-winter27.md`, which was never committed.

## v1.0.1 — 2026-10-14 — System test and DEF-01

The UAT scripts were run as an evidenced system test through the API (admin-run; not UAT with outside users). 11 scripts pass; UAT-10 and 11 passed after a same-night fix. (Corrected 2026-10-24: this first said 12, counting DEF-01's retest twice.) Full results: `docs/system-test-results-2026-10-14.md`.

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

## v1.0 — 2026-10-14 — Phase 10: Release

Accord is feature-complete: 20 of 21 stories delivered, one cut on purpose. This release adds the documentation that turns the build into something another admin could test, run and support. Outside UAT and the walkthrough video are the two items that need people and time, and are tracked in `open-items.md`.

### Added — docs
- `docs/case-study.md` — the project in ten minutes: problem, decisions, what went wrong, results
- `docs/uat-scripts.md` — 21 scripts, one per story, each with its negative case and a sign-off table
- `docs/rca-balance-formula.md` — root cause analysis of the $0-balance formula, including why four existing checks missed it
- `docs/quick-reference.md` — one page per role
- `README.md` — rewritten as the front door: results, what's in the org, how to explore, known limits
- `docs/requirements.md` — traceability complete; US-17 marked cut with the reason
- `docs/data-plan.md` — after numbers (every target met), billing regeneration, household rename, control-total check added to load verification
- Security model additions: case sharing, role cleanup, case teams, activity access, folder sharing, D-07 exceptions, admin self-approval

### Added — manifests
- `manifest/phase9-retrieve.xml` — everything built through the API in Phases 7–9 that isn't in source yet
- `manifest/cleanup-fields/` — destructive deploy: 24 Developer Edition sample fields and the sample Delivery Status link
- `manifest/cleanup-layouts/` — destructive deploy: 6 sample Account and Case layouts

### Release checks
| Check | Result |
|---|---|
| All 11 flows active | ✓ |
| 12 validation rules active, each with a description | ✓ |
| Data Quality dashboard | 0 on every metric |
| Collections Supervisor dashboard refreshes, all 10 components return data | ✓ |
| Standard Lead and Contact duplicate rules inactive; custom alert rules active | ✓ |
| Collections Console opens on Collections Home | ✓ |
| No real-looking personal data in the org | ✓ (one web-form test lead corrected) |

### Still open, by design
- **Outside UAT** with 3–5 testers who didn't build it
- **Walkthrough video**
- **Automatic Default Review.** Two accounts reach 90 days past due around October 18–19. The nightly flow should open their reviews on its own — the first "on time" review on the dashboard.

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

## v0.7 — 2026-10-14 — Phase 8: Sales

Website inquiries become routed leads, a lead that matches an existing customer is flagged, and collections reps log every contact attempt with a structured outcome. One Could story was cut on purpose.

### Added
| Component | Type | Does | Stories |
|---|---|---|---|
| `web/lumenfield-solar-inquiry.html` | Web-to-lead form | Name, email, phone, service address, service area, inquiry detail. Posts to the org; custom fields mapped by field ID | US-16 |
| `VR_Lead_EmailOrPhoneRequired` | Validation rule | A lead with neither email nor phone is rejected, because there's no way to follow up | US-16 |
| `Accord Lead Routing` | Lead assignment rule | Every new lead, web or manual, goes to the Inbound Leads queue | US-16 |
| `Contact_Match_Email_Only` | Matching rule | Exact email match, lead to contact | US-16 |
| `Lead.Lead_Matches_Existing_Customer` | Duplicate rule | **Alert, not block.** Flags a lead whose email belongs to an existing customer, so web submissions still arrive | US-16 |
| `Contact_Outcome__c` | Activity field | Picklist on the global value set Contact Outcome | US-06 |
| `Account_Screen_LogContactAttempt` | Screen flow | Logs a completed task with an outcome. Promise Made goes straight into the promise screen; Requested No Further Contact sets Do Not Contact; Hardship or Bankruptcy sets Hardship Review | US-06, US-21 |
| `Account.Log_Contact_Attempt` | Quick action | Launches the flow from the Residential Agreement layout | US-06 |

### Changed
- Standard Lead Duplicate Rule deactivated. It blocked API and web-to-lead inserts outright; the custom rule alerts instead.
- Minimum Access profile given **Residential Agreement** as its default Account record type. This is the single exception to D-07: permission sets can grant record types but can't set a default, and lead conversion needs one.
- `Contact_Outcome__c` field-level security granted: System Administrator, Collections Core (edit), Dispute Management (read). New fields deployed from source get no access by default.

### Verified
- Web form submission → lead created with all custom fields populated → owned by Inbound Leads
- Submission with no email or phone → rejected, no lead
- Submission using an existing customer's email → lead created and flagged as a 100% match to that contact
- Log Contact Attempt is covered by UAT-06 (outcome required, Promise Made chains into the promise, Do Not Contact and Hardship flags)

### Cut on purpose
- **US-17, pipeline and forecast against quota (Could).** Collaborative Forecasts and quota loading add setup and screenshots without touching the lead-to-cash problem Accord exists to solve. Cutting the only Could story is a scope decision, recorded so it isn't mistaken for an oversight.
- **Quotes.** Not needed by any story. `PS_Sales_Core` has no Quote, Product or Price Book access.

### Lessons recorded
- The promise step has its own fault screen. `Promise_AfterSave_ApplyPolicy` can refuse a promise (a second active promise, for example), and without a fault path the rep would see a raw flow error instead of the reason.
- Activity custom fields live under `objects/Activity` in source, but field permissions reference them as `Task.Contact_Outcome__c`.
- Flows can't run assignment rules, so anything a flow creates must set its owner directly. The lead rule covers people and the web form; the default review flow sets its queue itself.

### Data
- One test lead entered through the web form with a real-looking personal email and phone was changed to fictional values (`example.com`, `555`). All data in this org stays invented.

## v0.6 — 2026-10-09 — Phase 7: Automation

Ten flows, an approval process and five validation rules. Every story they serve was tested against the org through the API, and every test record was deleted afterward.

### Added — flows
| Flow | Type | Does | Stories |
|---|---|---|---|
| `Account_Daily_Collections_Status` | Scheduled, daily | Sets Account Status from Days Past Due; stamps Threshold Crossed Date; opens a Default Review case owned by the Default Reviews queue | US-05, US-15, D-08 |
| `Account_Daily_BrokenPromiseCount` | Scheduled, daily | Recounts broken promises in the last 90 days so the count rises and falls | US-04, US-05 |
| `Contact_AfterSave_StampPrimaryContact` | After save | Primary-role contact becomes the account's primary; first contact stands in until then | US-01, US-19 |
| `Case_BeforeSave_StampEntitlement` | Before save | Attaches the account's active entitlement to new Billing Disputes | US-09 |
| `Case_AfterSave_DisputeLifecycle` | After save | Flags and restores the disputed statement; completes milestones as status advances; removes the case team at close | US-07, US-08, US-09, US-18 |
| `Promise_AfterSave_ApplyPolicy` | After save | Blocks a second active promise; out-of-policy promises go to Pending Approval; in-policy promises set the collection hold | US-03 |
| `Promise_Daily_Evaluate` | Scheduled, daily | After grace, totals real payments and marks Kept or Broken; releases the hold | US-04 |
| `Opportunity_AfterSave_CreateServiceContract` | After save | At Closed Won, creates the service contract and links the deal's commitments | US-02 |
| `Adjustment_AfterSave_Lifecycle` | After save | Credits within the rep limit post immediately; submission, approval and rejection move the related dispute; a rejection without a reason assigns the approver a task to record one | US-11, US-13 |
| `ServiceContract_AfterSave_WelcomeAndReminder` | After save + scheduled path | Welcome email on activation, first-payment reminder 7 days before due, follow-up task when there's no email | US-19, US-20, US-21 |

### Added — rules and approvals
- `VR_Account_PrimaryContactRequired` — activated after backfilling all 100 accounts; skips the first save so new households can be created
- `VR_Opp_ConcessionNeedsCommitment` — fires only on the move to Closed Won, so historical deals aren't blocked
- `VR_Adjustment_ApprovalRequired` — credits over the limit can't be set to Approved or Posted by hand. Approval field updates skip validation rules, which makes the approval process the only route through
- `VR_Adjustment_AmountLockedAfterApproval`
- `VR_Case_RootCauseRequired` — a billing dispute can't be Resolved without a root cause (US-10)
- **Credit Approval** process: over $100 to the Collections Supervisor; only Dispute Specialists and Collections Reps can submit

### Data
- Primary Contact backfilled on all 100 accounts; the "no one to contact" data quality metric goes from 88 to 0
- The 13 test disputes brought in line with the new flows: 10 statements flagged In Dispute, 12 passed milestones completed

### Verified
- Status flow fixed a mismatch account and it became visible to collections immediately, while the other mismatch stayed hidden until processed — status is a security control
- New household: saves without contacts → co-signer stands in → Primary-role contact takes over; clearing the primary is blocked
- Dispute: entitlement attached, statement flagged, milestones completed in order and on skips, case team removed at close, statement restored to its real status
- Promise: second active promise blocked; full in-window promise held the account to the grace date; short promise went to Pending Approval with no hold
- Deal with a concession blocked at Closed Won until a commitment existed; then a service contract was created and the commitment linked
- Welcome email sent and stamped on activation; reminder scheduled for 7 days before first due
- Credits: $75 posted on its own; $250 blocked from manual approval, approved through the process, posted, dispute returned to Under Review; approved amount locked

### Lessons recorded
- Approval field updates skip validation rules. Used deliberately to make the approval process the only path for large credits — and it's why a rejection reason can't be required at the moment of an approval-process rejection; the lifecycle flow assigns the approver a task to record it instead
- System Administrators can submit any approval regardless of allowed submitters. In a two-license org where the admin is also the supervisor, self-approval is possible; in production, admins don't approve credits
- Approval entry criteria can't read custom metadata, so the $100 threshold is duplicated from `Rep_Credit_Limit`
- Milestones lock once their case exits the entitlement process
- Detail objects in a master-detail relationship can't be owned by queues
- Validation rule API names are limited to 40 characters

### Known limits
- Scheduled path offsets can't read custom metadata; the reminder is fixed at 7 days and duplicates `Pre_Due_Offset_Days`
- Promise evaluation counts payments on the promise's related statement only; promises without a related statement (5 seeded orphans) can only be marked Broken
- Approver is a named user, a Developer Edition license constraint

## v0.5 — 2026-10-08 — Phase 6: Service

Disputes and default reviews now run as governed cases: their own record types and status paths, queue routing, a business-hours SLA with alerts, and a console for the people who work them. The phase also surfaced and fixed a formula bug and a dataset that didn't match its own plan.

### Added
- **Account record types** Residential Agreement (88) and Organization (12), granted through `PS_Sales_Core` only, since record type assignment governs create and change, not view
- **Case record types** Billing Dispute and Default Review, each with a support process. Seven Case Status values: Acknowledged, Awaiting Evidence, Under Review, Pending Credit Approval, Resolved, Cured, Default Confirmed (deployed from source)
- **Page layouts** for all four record types. Residential accounts lead with a Collections section; Billing Dispute carries reason, statement, originating deal, entitlement and resolution; sample fields left off every layout
- **Queues** Dispute Specialists and Default Reviews, with roles as members rather than named users
- **Case assignment rule** `Accord Case Routing`; the assignment checkbox is defaulted on and hidden so it can't be bypassed
- **Case sharing rule** `Billing_Disputes_to_Collections`: Read Only on billing disputes to Collections Reps (US-01). Default reviews stay private
- **Entitlement process** `Billing Dispute SLA` on Lumenfield Support Hours: acknowledge in 1 business day, request evidence in 3, resolve in 10 (600 / 1800 / 6000 minutes). 88 entitlements, one per residential account
- **Milestone alerts (US-14)**: warning to the case owner at 75% of each milestone, violation to the owner and Collections Supervisors at the target
- **Dispute evidence requirements** for the remaining five reasons; all 8 reasons now have a checklist (16 records)
- **Outbound contact business hours**: Mon–Fri 8 AM–8 PM, Sat 9 AM–5 PM, Eastern; inside the FDCPA 8 AM–9 PM window
- **Collections Console** (Lightning console app) and object tabs for Billing Statement, Payment, Promise to Pay, Adjustment and Commitment, granted through permission sets with tab defaults
- **Test cases**: 13 billing disputes across every status and all 8 reasons, and 5 default reviews on the 90+ accounts
- `data/regen/generate_billing.py` and runbook: regenerates billing history anchored to a given date; rerun to re-age the book before UAT or a demo
- `requirements.md` rewritten with acceptance criteria for all 21 user stories

### Fixed
- **`Billing_Statement__c.Balance__c` was `Amount_Paid__c - Amount_Paid__c`** and always zero, so every account's Current Balance and Past Due Balance read $0. Corrected to `Amount_Due__c - Amount_Paid__c`; about $10,088 in balances appeared. The Phase 5 dashboard couldn't have caught it, since nothing measured balances
- **Delinquency distribution**: 29 accounts sat at 90+ days past due against a plan of 5, because each statement series ended months before the load. Billing data regenerated against today: Current 52 · 1–30 14 · 31–60 10 · 61–90 7 · 90+ 5
- `PS_Collections_Core` had no Read on Case, so the dispute sharing rule had nothing to open. Added Case Read and read on Dispute Reason and Root Cause
- Persona users landed in Salesforce Classic; Minimum Access lacks Lightning Experience User. Added to the three persona permission sets
- `Case.EntitlementId` was hidden from System Administrator, so cases couldn't be linked to an SLA
- Developer Edition leftovers removed: nine sample roles (three sat under Dispute Specialist, giving upward visibility into sales records), the Standard Case entitlement process and its milestones, Developer Edition sample campaigns, solutions, products and price book
- `PS_Payment_Detail` label double space

### Verified
- SLA counts business hours only: a case opened Wednesday evening targeted Thursday 6 PM, Monday 6 PM (weekend skipped) and ten business days out (US-09)
- Collections Rep reads billing disputes, can't edit them, can't see default reviews
- Sales rep not on a case team can't open a dispute, including one about their own deal; added to the team, they can read it and nothing more (US-08, US-18)

### Lessons recorded
- An entitlement process locks once any case has used it, even a deleted one. Milestone actions were added in Setup instead. In production, enable entitlement versioning before go-live
- Some standard fields are required on every layout (Account: Parent Account; Case: Contact, Origin, Web fields)
- Static seed data with TODAY() formulas drifts a day every day; a re-age routine is part of the dataset, not an afterthought

### Known, deliberately deferred to Phase 7
- New disputes don't yet stamp their entitlement, complete milestones on status change, flag the disputed statement, or remove case team members at close
- Default reviews are opened by hand; the flow that opens them on the threshold crossing (and sets the owner, since Flow can't run assignment rules) comes next

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
