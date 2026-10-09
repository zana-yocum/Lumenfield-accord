# Open Items — Accord

Everything deferred, flagged, or half-finished. Updated at the end of every sitting. Nothing gets to live only in a chat log or someone's memory.

**Status key:** ☐ open · ☑ done · ⊘ deliberately not doing

---

## Verify before Phase 5

Quick confirmations, not real work. Each one is something that may or may not have been finished.

- ☐ Global value set descriptions — all four sets (Contact Outcome, Dispute Reason, Root Cause, Commitment Type) need a Description filled in
- ☑ Service Contract org-wide default set to Private
- ☑ Admin user assigned to the Collections Supervisor role
- ☐ Test records used to verify the formula chain deleted from the org
- ☑ Permission set API names carry the `PS_` prefix per `conventions.md`
- ☑ Adjustment → Type field marked Required
- ☑ Field history tracking enabled on all five custom objects

---

## Deferred to a later phase

### Phase 5 — data load and quality ☑ closed 2026-10-03
- ☑ Developer Edition sample data deleted (Edge Communications, Burlington Textiles, Sample Account for Entitlements, 22 sample leads); confirmed nothing else survived
- ☑ 5–10% deliberate defects seeded into the dataset
- ☑ `Legacy_Id__c` External ID fields on Account, Contact, Lead, Opportunity, Service Contract, Billing Statement (D-09)
- ☑ Dataset loaded via CLI bulk import: 100 accounts, 135 contacts, 100 opportunities, 31 commitments, 100 service contracts, 570 statements, 518 payments, 60 promises, 12 adjustments, 30 leads
- ☑ Data quality baseline captured 2026-09-30: 7 duplicate pairs flagged · 0% primary contact · 88% role completeness · 97% status accuracy · 2 statement date errors
- ☑ Contact matching rule and duplicate rule (alert, not block) built; Standard Contact Duplicate Rule deactivated
- ☑ Five validation rules built, with descriptions
- ☑ Cleanup: six duplicate pairs merged, missing roles filled, two statement dates corrected
- ☑ Two `noemail@example.com` placeholder emails cleared; one `.cm` typo domain fixed
- ☑ Dashboard renamed **Data Quality**; duplicate chart sorted by count, metric tiles color-ranged, titles shortened
- ☑ Two unused report copies deleted from the `DataQuality` folder
- ☑ Screenshot `phase05-data-quality-dashboard-after.png`
- ☑ CHANGELOG v0.4 written
- ☑ Phase 5 metadata retrieved: objects (with validation rules), matching rule, both Contact duplicate rules, dashboard, five reports, both folders
- ☑ Commit Phase 5 to GitHub
- ☑ **Org verification via the Salesforce connector (2026-10-03)** caught three items marked done that weren't: the `.cm` typo and both placeholder emails were never fixed (one placeholder had been changed to `.cm`, which is why the duplicate chart looked clean), and the Sample Account for Entitlements was still present. Also found and removed 17 sample products, 10 sample solutions, and a sample price book. All fixed and re-verified.
- ☑ 4 sample campaigns (2001–2002) deleted. The first attempt failed with insufficient access: deleting campaigns requires the **Marketing User** checkbox on the user record, which was then enabled.
- ☐ Reword four validation rule error messages to name the fix rather than the problem, per `conventions.md` (e.g. "Enter a due date on or after the statement date"). `VR_Adjustment_RejectionReason` already complies.
- ☐ Remaining Phase 5 screenshots if not yet taken: `phase05-duplicate-rule-config.png`, `phase05-duplicate-alert-in-action.png`, `phase05-data-loader-success.png`
- ☐ `data-plan.md` — add the after numbers to the measurement table (duplicates 0, roles 0, statement dates 0)

### Phase 6 — service ☑ closed 2026-10-08
- ☑ **Account record types created** (2026-10-03): `Residential_Agreement` (88 accounts) and `Organization` (12 accounts, ACC-0089 to ACC-0100). Available on System Administrator (default Residential Agreement) and through `PS_Sales_Core` only. Collections doesn't need an assignment, because record type assignment governs create and change, not view or edit. Accounts bulk-assigned through the API and verified by count.
- ☑ **Page layouts per record type** deployed from source and assigned for every profile (verified for System Administrator and Minimum Access): Residential Agreement (Collections section with balance, days past due, bucket, priority score, broken promises), Organization (no collections fields), Billing Dispute (dispute, SLA entitlement, Resolution with Root Cause), Default Review (threshold date, on-time flag, outcome). Sample fields are left off every layout.
- ☑ Lesson from the deploy: some standard fields must be on every layout whether used or not. Account needs Parent Account; Case needs Contact, Case Origin, and the four Web fields. Salesforce reports one per layout per deploy, so it took three rounds.
- ☑ Case sharing rule `Billing_Disputes_to_Collections`: criteria-based, Billing Dispute record type, Read Only to the Collections Rep role. Supervisors already see disputes through the hierarchy; Default Review cases stay private.
- ☑ **Role hierarchy cleanup** (2026-10-07): nine Developer Edition sample roles deleted (VP North American Sales, VP International Sales, VP Marketing, two sales directors, four sales and marketing teams). Three of them sat directly under Dispute Specialist, which would have given dispute specialists upward visibility into any sales or marketing records. No users held them. Hierarchy is now Executive → VP Customer Operations → Collections Supervisor → (Collections Rep, Dispute Specialist), and Executive → VP Sales → Sales Manager → Sales Rep.
- ☑ **Queues** Dispute Specialists and Default Reviews (Case), with roles as members rather than named users: Dispute Specialist role and Collections Supervisor role.
- ☑ **Case assignment rule** `Accord Case Routing`: Billing Dispute → Dispute Specialists queue, Default Review → Default Reviews queue. Assignment checkbox defaulted on and hidden on Case Layout so it can't be bypassed. Verified by creating one test case of each type through the API (both landed in the right queue), then deleting them.
- ☑ **Found and fixed while testing:** the Collections Rep could not see a Billing Dispute case even though the sharing rule had created a Read share. `PS_Collections_Core` had no Read permission on Case, so sharing had nothing to open. Added Case Read (no create, edit, or delete) plus read on `Dispute_Reason__c` and `Root_Cause__c`. Retested: Billing Dispute readable, not editable; Default Review not visible. Case access across personas is now: Collections Rep Read · Collections Supervisor and Dispute Specialist Read/Create/Edit · Sales Rep Read (for case teams, US-18) · no Delete anywhere.
- ☑ **Entitlement process `Billing Dispute SLA`** deployed from source, active, on Lumenfield Support Hours (Mon–Fri 8–6 ET, so one business day = 600 minutes). Milestones: Acknowledge Dispute 600 min, Request Evidence 1800, Resolve Dispute 6000. Clock stops when the case closes. Sample process Standard Case and its three sample milestone types deleted.
- ☑ **88 entitlements**, one per Residential Agreement account, each pointing at Billing Dispute SLA.
- ☑ **SLA verified with a test case** created Wednesday 8:26 PM ET: targets landed Thu 6 PM, Mon 6 PM (weekend skipped), and Wed Oct 21 6 PM (10 business days). Proves US-09 criterion 4. Test case deleted.
- ☑ Field-level security gap found: `Case.EntitlementId` was hidden from System Administrator, so cases couldn't be linked to entitlements even through the API. Granted Read/Edit to System Administrator and Read to `PS_Dispute_Management`.
- ☑ **Milestone alerts (US-14)**: email templates `Dispute Milestone Warning` and `Dispute Milestone Violation` (folder Accord Case SLA) and matching email alerts, deployed from source. Warning goes to the case owner at 75% of each milestone (150 / 450 / 1500 minutes before target); violation goes to the owner and the Collections Supervisor role at the target. Both queues set to email their members. The "flagged as breached" criterion is met by the standard Milestone Status field (Open Violation).
- ☑ **Lesson: an entitlement process locks once any case has used it, even a deleted test case.** The Metadata API refused the update with "Cannot update SLA process that is in use"; detaching all 88 entitlements and emptying the Recycle Bin didn't release it. Milestone actions were added through Setup instead, which allows actions on in-use processes. In production, enable entitlement versioning before go-live so later changes become new versions.
- ☑ Org Recycle Bin emptied (123 items: test cases, sample data, merged duplicate contacts)
- ☑ **Collections Console** (Lightning console app) and **five object tabs** (Billing Statement, Payment, Promise to Pay, Adjustment, Commitment) deployed from source. The root cause of the empty home page was that the custom objects had no tabs, so no app could show them. Accounts open as workspace tabs; related records open as subtabs.
- ☑ App access and 10 tab settings (Default On) granted to `PS_Collections_Core` and `PS_Dispute_Management` through the API. Verified the app flows through `PSG_Collections_Rep` to the Test Persona user.
- ☑ **Found while testing as Test Persona:** persona users landed in Salesforce Classic, where console apps don't exist. Minimum Access doesn't include the Lightning Experience User permission, so with D-07 it has to come from a permission set. Added it to `PS_Collections_Core`, `PS_Dispute_Management`, and `PS_Sales_Core`, and set Test Persona's interface preference to Lightning.
- ☑ **Dispute evidence requirements complete**: 10 new records deployed from source, two per reason, for Duplicate or Unauthorized Draft, Payment Not Posted, Annual Escalator Increase, Home Sale or Transfer, and Outage or Repair Credit. All 8 dispute reasons now have a checklist (16 records). The org had 6 before this, not 7 as previously noted.
- ☑ **`Lumenfield Outbound Contact Window`** business hours: Mon–Fri 8 AM–8 PM, Sat 9 AM–5 PM, Sunday closed, Eastern. Inside the FDCPA 8 AM–9 PM limit with an end-of-day buffer. Not the default; support hours still run the SLA clock.
- ☑ **Case record types deployed from source** (2026-10-07): Billing Dispute and Default Review, each with its own support process. Seven new Case Status values added (Acknowledged, Awaiting Evidence, Under Review, Pending Credit Approval, Resolved, Cured, Default Confirmed). Available on System Administrator (default Billing Dispute) and on `PS_Dispute_Management` (Billing Dispute only, since default reviews are opened by automation). Status paths verified per record type through the UI API.
- ☑ **Test cases loaded** (CASE-0001 to CASE-0018): 13 billing disputes covering all 8 dispute reasons and every status (3 New, 2 Acknowledged, 2 Awaiting Evidence, 2 Under Review, 1 Pending Credit Approval, 2 Resolved with root cause, 1 Closed as withdrawn), each linked to its statement, contact, service contract, originating deal and SLA entitlement; 5 default reviews on the five 90+ accounts. Verified: disputes routed to Dispute Specialists with 3 milestones each, reviews routed to Default Reviews. All 5 reviews show Opened On Time = false, which is correct — those accounts crossed 90 days before any automation existed. That's the US-15 "before" number for Phase 7.
- ☑ **Negative test (US-08, US-18), deferred since Phase 4.** Test Persona was switched temporarily to Sales Rep (Developer Edition has two full licenses, so one persona user stands in for each role in turn). Not on the case team: no access to the dispute about their own deal, an unrelated dispute, or a default review. Added to the case team as Sales Input: read access to that one case, no edit — the team role grants Edit, but `PS_Sales_Core` has Read on Case, so the object permission caps it. Team member removed and Test Persona restored to Collections Rep; access rechecked afterward.
- ☑ Retrieves for each step committed as the phase went

**Loose ends carried forward (small)**
- ☐ Setup → Deliverability is **All email**, or milestone alerts fire but never send
- ☑ System Administrator access to Collections Console (verified)
- ☑ Email alert descriptions shortened (verified)
- ☐ Retrieve `CustomField:Billing_Statement__c.Balance__c` (formula fix) and commit `data/regen/`, excluding the `del_*.csv` scratch files
- ☑ `--line-ending LF` added to the runbook import commands
- ☐ Sales persona app — Phase 8

### Phase 7 — automation ☑ built and tested 2026-10-09
- ☑ **Promises (US-03, US-04):** `Promise_AfterSave_ApplyPolicy`, `Promise_Daily_Evaluate`, `Account_Daily_BrokenPromiseCount`. Tested: second active promise blocked; in-policy promise set a hold to grace end; short promise went to Pending Approval with no hold.
- ☑ **Credits (US-11, US-13):** `Adjustment_AfterSave_Lifecycle`, Credit Approval process, `VR_Adjustment_ApprovalRequired`, `VR_Adjustment_AmountLockedAfterApproval`. Tested: $75 posted on its own; $250 blocked from manual approval, approved through the process, posted, dispute back to Under Review; approved amount locked.
- ☑ **Welcome and reminder (US-19, US-20, US-21):** `ServiceContract_AfterSave_WelcomeAndReminder`. Tested: welcome sent and stamped on activation; reminder scheduled. Fires only when a contract becomes active, so the existing 88 customers weren't emailed.
- ☐ **Confirm the first scheduled runs** (Oct 10, 1:00 and 1:30 AM ET): ACC-0002 and ACC-0003 move to Delinquent; nothing else changes status; broken-promise counts unchanged (the regenerated data already matches); no Active promise past grace yet
- ☐ Test a Default Review opening automatically: let an account cross 90 days with no open review, or debug the status flow on one after closing its review
- ☐ **Rejection reason can't be enforced on approval-process rejections**: approval field updates skip `VR_Adjustment_RejectionReason`. Options: a flow that creates a task for the approver to record the reason, or make rejection a manual status change. Decide and document (US-11 criterion 3)
- ☐ **Self-approval by admins**: System Administrators can submit any approval regardless of allowed submitters. Document in `security-model.md`; in production the admin isn't a supervisor
- ☐ Approval threshold ($100) duplicates `Rep_Credit_Limit`; reminder offset (7 days) duplicates `Pre_Due_Offset_Days`. Note both in the automation inventory
- ☑ **`VR_Case_RootCauseRequired`** (US-10): billing disputes can't be Resolved without a root cause; Closed (withdrawn) doesn't need one. Found missing while filling in traceability; built through the Tooling API and tested on CASE-0001.
- ☐ **US-06 contact attempt action** (Should): a quick action or screen flow to log an outcome from the Contact Outcome value set, chaining into a promise when the outcome is Promise to Pay. Not built in Phase 7; carry to Phase 8 or 9.
- ☐ Commitment Status picklist has a stray value "Check" — remove or deactivate
- ☐ Retrieve and commit: everything in `phase7-automation.zip` is already local; also retrieve `ValidationRule:Account.VR_Account_PrimaryContactRequired` and `ValidationRule:Case.VR_Case_RootCauseRequired`
- ☑ **Dispute lifecycle tested end to end** on a throwaway case (Paid statement STM-00452, ACC-0060): created with no entitlement → entitlement attached, routed to Dispute Specialists, 3 milestones started, statement In Dispute. Acknowledged → only Acknowledge completed. Sales rep added to case team, then jumped straight to Resolved → team member removed, both remaining milestones completed, statement back to Paid with Dispute Open cleared. Test case deleted.
- ☑ **Backfilled the 13 Phase 6 test disputes**: 12 passed milestones completed on open cases, 10 open disputes' statements flagged In Dispute.
- ☑ **Lesson: milestones lock once their case exits the entitlement process.** Completing milestones on the 3 already-closed test disputes was refused ("can't change the completion date on a milestone that's already exited an entitlement process"). The flow completes them inside the closing save, before they lock, so this only affects cases closed before the flow existed; their milestones stay as an honest record.
- ☑ **`Account_Daily_Collections_Status`** (scheduled, daily 1 AM ET) deployed from source and active. Sets Account Status from Days Past Due (Current / Delinquent / Default Review at the `Default_Threshold_DPD` policy setting), stamps Threshold Crossed Date, opens a Default Review case owned by the Default Reviews queue when none is open. Skips Closed and Hardship Review. Debug-tested on three accounts: ACC-0082 (14 DPD, Delinquent) and ACC-0060 (0 DPD, Current) took "Already correct" with no update; ACC-0001 (43 DPD, marked Current) moved to Delinquent.
- ☑ **Proved the security effect (D-08):** right after the debug run, Test Persona (Collections Rep) could read ACC-0001 and still could not read ACC-0002, the other mismatch account not yet run. Status drives visibility; the flow is what makes it accurate.
- ☐ Confirm the first scheduled run (Oct 10, 1 AM ET) moved ACC-0002 and ACC-0003 to Delinquent and changed nothing else
- ☑ **Case team removed on close** in `Case_AfterSave_DisputeLifecycle`. Done.
- ☑ **Disputed statement flagged** (Dispute Open, In Dispute) while the case is open; restored on close to Paid / Past Due / Open from its real balance and due date. Done.
- ☐ Confirm a case team member with Read can add case comments (US-08 says "read the case and add comments"); if comments need Edit, decide between a Sales Input permission and a quick action
- ☐ Account record types: the 12 Organization accounts each still have a service contract, though Organization is described as "not a lease holder." Remove those contracts or revise the description.
- ☑ **`Case_BeforeSave_StampEntitlement`**: new Billing Disputes without an entitlement get the account's active one, so the SLA starts. Done.
- ☑ **Milestones complete from status** in `Case_AfterSave_DisputeLifecycle`: Acknowledged → Acknowledge; Awaiting Evidence or later → Request Evidence; Resolved/Closed → Resolve; skipped stages complete too. Done.
- ☐ New Residential Agreement accounts need a Billing Dispute SLA entitlement; create it when the account is created or activated.
- ☐ **Flow can't run assignment rules.** The default review flow must set the case owner to the Default Reviews queue directly; the assignment rule only covers cases people create.
- ☑ **Primary contact backfill**: all 100 accounts set to their Primary-role contact through the API. The Data Quality "no one to contact" tile should now read 0 (was 88).
- ☑ **`VR_Account_PrimaryContactRequired` active**: residential, not Closed, primary contact required. Refined from the Phase 5 plan to skip the first save (`NOT(ISNEW())`), because an account has to exist before its contact can be added. Tested: clearing a primary contact is blocked with the field-level message.
- ☑ **`Contact_AfterSave_StampPrimaryContact`** deployed and active. A Primary-role contact becomes the account's primary; an account with no primary takes its first contact as a stand-in. Tested end to end on a throwaway household: saved with no contacts, co-signer stamped as stand-in, Primary-role contact took over. Test records deleted (still in the Recycle Bin).
- ☑ **`Opportunity_AfterSave_CreateServiceContract`** + `VR_Opp_ConcessionNeedsCommitment` (US-02). Tested: close blocked without a commitment; after adding one, service contract created and commitment linked.
- ☑ Status flow documented and demonstrated as a security control (see CHANGELOG v0.6)
- ☐ **Design constraint from Winter '27 review:** no flow may assume sharing is recalculated in the same transaction as a role or group change (Spring '27 release update; D-08 depends on sharing)
- ☐ Consider Winter '27 mass screen flow action (`ids` collection) for bulk collections outcomes, and rely on Flow's row-lock auto-retry for the backfill
- ☐ Note the `Dispute_Reason__c` weakness in the automation inventory: it's plain text on the custom metadata type because custom metadata picklists can't inherit from a global value set, so the match to the value set is convention rather than enforcement

### Phase 8 — sales
- ☐ **Default record type for lead conversion.** Permission sets can grant record types but can't set a default; defaults come only from the profile. Sales reps on Minimum Access have no default Account record type, and lead conversion depends on one. Resolve before building conversion: test it, then decide whether the profile gets Residential Agreement as its default or the conversion process handles it.
- ☐ Lead-to-Contact matching rule on email (listed in `data-plan.md`, not yet built)
- ☐ Enable Quotes (Setup → Quote Settings), then add Quote, Product, and Price Book access to `PS_Sales_Core`
- ☐ Load forecast quotas via Data Loader

### Phase 9 additions
- ☐ **Collections Console home page.** The console currently shows the default Sales home (Quarterly Performance, Key Deals, an opportunity-access message). Replace it with a Lightning home page for the app: the rep's prioritized work list (US-05) and open disputes.

### Phase 10 — release
- ☐ README limits section: business hours use a single time zone, so the outbound contact window doesn't protect a customer in another time zone from an early call. A production build would check the customer's local time in the contact automation.
- ☐ README limits section — write up the payment allocation gap, the business-day simplification on the default review window, and the Developer Edition persona testing constraint
- ☐ Recruit 3–5 outside UAT testers, run scripts, collect written sign-off
- ☐ Root cause analysis write-up on one defect found during UAT
- ☐ Training kit: five-minute video, one-page quick reference, in-app guidance prompt
- ☐ Walkthrough video

---

## Recorded results

- ☑ **Data load: six distinct failure modes, all diagnosed from error files.** State and Country picklists rejecting plain values · Data Loader caching the schema before new fields existed · relationship columns needing different syntax per tool (colon for Data Loader, dot for Bulk API 2.0) · Legacy Id columns on objects that had no such field · picklist values entered with trailing commas or two values on one line · standard duplicate rules active by default and blocking API inserts. Full write-up in `data-plan.md`.

- ☑ **Metadata retrieve lessons.** Validation rules come back inside `CustomObject`, not as a standalone type. Folder-based metadata (reports, dashboards) needs exact `Folder/DeveloperName` names, found with `sf org list metadata --folder`, and private folders can't be retrieved at all. The dashboard's own XML is the source of truth for which reports it uses — that's how two unused copies were found and deleted.

- ☑ Security Health Check: **66% (Poor) → 96% (Excellent)** in one sitting. The single remaining Critical is trusted IP ranges, left unfixed deliberately and documented in `security-model.md`.
- ☑ Enabled "Require permission to view record names in lookup fields" — closes a leak where users who can't see a record can still see its name through a lookup.

---

## Time-sensitive

- ☑ **Winter '27 readiness review** written: `docs/release-readiness-winter27.md`. Instance USA838 upgrades **Oct 9, 2026, 11:00 PM CDT**.
- ☐ Before Oct 9: enable Profile Filtering (overdue, currently off) and verify records, reports, and dashboard still work
- ☐ Before Oct 9: test runs for the three overdue accessibility updates and Update Instanced URLs; check dashboard, a record page, and New Payment / New Billing Statement modals at 200%+ zoom
- ☐ Before Oct 9: screenshots `release-winter27-updates-before.png`, `release-winter27-overdue-before.png`, `release-winter27-profile-filtering-before.png`
- ☐ After Oct 9: run the post-upgrade checklist in the readiness doc, screenshot `release-winter27-after.png`

---

## Found while preparing test cases (2026-10-08)

- ☑ **`Billing_Statement__c.Balance__c` formula was `Amount_Paid__c - Amount_Paid__c`** — always zero. Every statement showed a $0 balance, statement Days Past Due read 0, and the account roll-ups Current Balance and Past Due Balance summed to $0 across the whole book. Corrected to `Amount_Due__c - Amount_Paid__c` through the Tooling API; roll-ups recalculated to about $10,088 owed. Retrieve `CustomField:Billing_Statement__c.Balance__c` into the repo. Worth a line in the Phase 5 write-up: the data quality dashboard couldn't have caught it, because nothing measured balances.
- ☑ **Delinquency distribution doesn't match `data-plan.md`.** Fixed 2026-10-08: billing data regenerated with `data/regen/generate_billing.py` anchored to today and reloaded with the CLI (632 statements, 545 payments, 60 promises, 12 adjustments). Verified in the org: Current 52 · 1–30 14 · 31–60 10 (including the 3 seeded status mismatches) · 61–90 7 · 90+ 5. Original note: Plan: 14 accounts at 1–30 DPD, 10 at 31–60, 7 at 61–90, 5 at 90+. Org: 29 accounts at 146+ DPD (up to 484) and 1 at 64. Each account's statement series stops months or a year before today, so unpaid statements age past 90 days. Needs the billing data (statements, payments, promises) regenerated against today's date before Phase 7, since status stamping, default reviews, and the priority list all depend on it.
- ☑ Re-age routine exists: `data/regen/generate_billing.py` + `RUNBOOK.md`. Rerun before UAT and demos. Still document the drift in the README. Original note: **Static seed data drifts.** Days Past Due uses TODAY(), so even correct data ages a day every day and every account eventually lands in 90+. Plan a re-age routine to run before UAT and demos, and document the limit in the README.

## Org cleanup

- ☐ Delete stray field `Production_estimate_given_at_signing_Wh__c` on Service Contract — a description pasted into a label on a second attempt at Est Annual Production
- ☐ Relabel custom `Payment__c` to **Lease Payment**. It shares a label with the standard Payment object, so the org shows two objects named Payment. API name stays `Payment__c`; nothing breaks.
- ☐ `Legacy_Id__c` on Lead isn't referenced by anything. Delete it, or document it as unused.
- ☑ `PS_Payment_Detail` label had a double space (`Payment  Detail`); corrected.
- ☐ **Developer Edition sample fields still on standard objects.** Case: `Product__c` (GenWatt model codes), `PotentialLiability__c`, `SLAViolation__c`, plus sample Type and Case Reason values (Mechanical, Electrical, Installation…). Account: `Active__c`, `CustomerPriority__c`, `NumberofLocations__c`, `SLA__c`, `SLASerialNumber__c`, `SLAExpirationDate__c`, `UpsellOpportunity__c`. Contact: `Languages__c`, `Level__c`. Lead: `CurrentGenerators__c`, `NumberofLocations__c`, `Primary__c`, `ProductInterest__c`, `SICCode__c`. Opportunity: `CurrentGenerators__c`, `DeliveryInstallationStatus__c`, `MainCompetitors__c`, `OrderNumber__c`, `TrackingNumber__c`. Delete, and replace Case Type and Reason values with ones that fit solar servicing.
- ☐ Delete Developer Edition sample layouts now that per-record-type layouts are assigned: Case (Marketing), Case (Sales), Case (Support), Account (Marketing), Account (Sales), Account (Support)
- ☐ Household names repeat (three "Boone Household" accounts, ACC-0001, 0060, 0082). Make them unique so search and record pickers aren't ambiguous.
- ☐ `Experience_Profile_Manager` standard permission set is in the repo from a wildcard retrieve. Delete the local file and retrieve only `PS_` permission sets going forward.
- ☐ Dashboard API name is auto-generated (`KBzhEuJNWsMpcbnMzmuwzHqwlGrEtH`). Cosmetic; document it as a platform default rather than chase a rename.

---

## Doc updates pending

- ☐ `security-model.md` — add the Case sharing rule and record the sample-role cleanup, including why roles parented under Dispute Specialist were a visibility problem

- ☑ `requirements.md` rewritten: acceptance criteria for all 21 stories, a summary table, and traceability filled in for what's built. US-21 retitled to match D-05 (consent gates promotional messages only).

- ☐ `README.md` — add a line explaining that field descriptions reference user stories (US-xx) and decisions (D-xx), both in `/docs`
- ☐ `security-model.md` — add a note that activity access can't be granted or restricted through permission sets, so Task visibility follows access to the parent record. Also note the Quotes deferral.
- ☐ `data-model.md` — the object list at the bottom still describes the plan rather than what was built; reconcile after Phase 5
- ☐ `security-model.md` — add the lookup-name permission to the org-level settings table, and record the Health Check before-and-after scores
- ☐ `README.md` — Health Check row in the results table can be filled in now: 66% → 96%

---

## Deliberately not doing

Written down so nobody mistakes these for oversights.

- ⊘ **Payment allocation object.** A payment spanning two statements can't be split. A production build would add a junction; this one documents the limit.
- ⊘ **Business-day math on the default review window.** Uses three calendar days, because business-day calculation in a formula needs Apex or a workaround. Deliberate simplification.
- ⊘ **Restriction rules.** Considered for tightening dispute visibility further; more than this build needs given the sharing model already in place (D-08).
- ⊘ **Custom Lightning components.** Three were candidates and all three use standard equivalents instead (D-04).
- ⊘ **Login IP ranges.** A remote workforce makes them impractical. MFA plus session timeout is the compensating control.
- ⊘ **Custom profiles.** Everything runs on Minimum Access plus permission set groups (D-07).
