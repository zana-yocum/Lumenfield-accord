# Open Items — Accord

Everything deferred, flagged, or half-finished. Updated at the end of every sitting. Nothing gets to live only in a chat log or someone's memory.

**Status key:** ☐ open · ☑ done · ⊘ deliberately not doing

---

## Release follow-up — 2026-10-24 and 25

Steward's Phase 5 hand check found that collections personas couldn't see **Log Contact Attempt** (DEF-08). Claude fixed it in the org and checked the clock-dependent results. Claude also found that `main` had been missing most of Accord's metadata since the Phase 6 commit, and retrieved it again from the org. Everything is in `CHANGELOG.md` v1.0.2 and `docs/system-test-results-2026-10-14.md`.

**Your steps**
- ☑ 1. **History (2026-10-25): rewritten**, your choice (b). Every commit now carries the placeholder instead of the org username, and GitHub's noreply address instead of your personal email; all 26 commits and their messages kept. `main` and `release/v1.0.2` replaced on GitHub. Optional: GitHub keeps the old commits reachable by their IDs until it cleans up. To have them removed sooner, open a ticket at support.github.com → **Removing sensitive data**, naming `zana-yocum/Lumenfield-accord`. Nobody has those IDs (no forks or pull requests), so this is low priority
- ☑ 2. **Public (2026-10-25).** The portfolio's Accord links work once v1.0.2 is merged into `main`
- ☐ **Your copy on your computer is out of date** since the rewrite: its commits no longer match GitHub's. In File Explorer, rename `C:\Lumenfield-accord` to `C:\Lumenfield-accord-old`. In GitHub Desktop: **File** → **Clone repository** → `zana-yocum/Lumenfield-accord` → local path `C:\Lumenfield-accord`. Copy back anything you made that isn't in the new copy (for example files in `data\regen`), then delete the old folder
- ☐ 3. **Persona checks:** `docs/persona-checks.md`, about 15 minutes as Test Persona. UAT-06 is possible now that DEF-08 is fixed. Steward's hand check covers Log Contact Attempt for the Collections Rep.
- ☐ 4. **UAT-14 email:** search the supervisor's inbox (yours) for **Dispute Milestone Violation**, around Oct 15, 5 PM CT and Oct 19, 5 PM CT, and tell Claude what's there. Then dispute 00001049 can be deleted.
- ☐ 5. If `docs/release-readiness-winter27.md` is still on your computer, add it to `docs/`. It was never committed, so the README no longer lists it.

**Mine (2026-10-24 and 25)**
- ☑ **DEF-08 fixed in the org:** `Account_Screen_LogContactAttempt` version 3 restricts access to enabled permission sets, and `PS_Collections_Core` grants it. Verified through the API on the three collections groups; Sales Rep excluded. Waiting on the console check.
- ☑ **Scheduled results:**
  - UAT-04 step 3 passed: six promises were broken on schedule.
  - UAT-14 passed on the org side.
  - UAT-15 steps 1–3 passed: two on-time Default Reviews, on Oct 18 and 19.
- ☑ **DEF-07 and the Oct 14 evening changes written up** from the Setup Audit Trail. DEF-02 to DEF-06 were never written down.
- ☑ **DEF-09 (High) fixed 2026-10-25:** the Minimum Access profile granted access to 74 Accord fields, 58 editable, so reps and sales reps could edit Account Status. Each persona's fields now come from its permission sets, with supervisor edit on Account Status, Collection Hold Until and High Value in the new `PS_Collections_Overrides`; the profile grants none. Counted per group against the plan in the org, checked field by field for Test Persona, and Steward's 159 tests passed against it (`0Afaj00000p4HeQCAU`). Details in the results doc
- ☑ **Permission set descriptions corrected in the org:** four had a stray "Description: ", and US-17 is gone from Sales Core and the Sales Rep group.
- ☑ **Metadata restored from the org** through Steward's retrieve workflow (`manifest/accord.xml`). Placeholders in the nine files that name a user; `scripts/check_personal_details.sh` added.
- ☑ **Repository tidied:**
  - The seven changelog files folded into `CHANGELOG.md`.
  - Bulk-load results moved to `data/load-results/`.
  - Steward's portal screenshots moved to Steward.
  - README counts corrected.
- ☑ **DEF-07's Commitments related list** is on the Residential Agreement layout: Steward's pull request #13, deployed 2026-10-25 (`0Afaj00000p7b8jCAA`) and checked in the org. The same deploy put `PS_Collections_Overrides` in the supervisor group's source.
- ☑ **Security model rewritten as built** (2026-10-25): object and field tables read from the org, the Phase 6–10 additions folded in, and the drifted claims corrected (case sharing goes to the Collections Rep role; no deletes on promises or cases; specialists don't see Default Reviews; a specialist, not a flow, adds sales input to a case team)
- ☑ `Mute_Rep_Promise_Delete` restored to source from v0.4, matching the org
- ☑ `Collection_Hold_Until__c`'s description, which repeated `Do_Not_Contact__c`'s, rewritten in the org and in source

---

## Release sitting — 2026-10-14

Built in the org through the API this sitting: Phase 9 reports, dashboard and home page; folder sharing; Run Reports for reps and specialists; `VR_Case_DisputeNeedsStatement`; four reworded error messages; 88 households renamed; Commitment Status cleaned; web-form test lead made fictional.

**Your steps to close the release** (PowerShell, from `C:\Lumenfield-accord`)
- ☑ Extract `accord-release.zip` into the repo root (overwrites README, requirements, data-plan, open-items; adds the new docs and manifests)
- ☑ `sf project retrieve start -o lumenfield --manifest manifest\phase9-retrieve.xml`
- ☑ Cleanup deploys done (fields, then layouts) — `--metadata-dir` failed with "No package.xml found"; the `--manifest` + `--post-destructive-changes` form worked
- ☑ `.\manifest\cleanup-local.ps1` — removes the deleted components from the repo
- ☑ Paste the three `CHANGELOG-v*.md` files into the top of `CHANGELOG.md` (newest first), then delete them. *(Correction 2026-10-24: `main` had the seven version files and no `CHANGELOG.md`. They were folded together in v1.0.2.)*
- ☑ Setup → Deliverability → Access level **All email**
- ☑ Setup → Object Manager → Payment (custom) → Edit → Label **Lease Payment**, Plural **Lease Payments**
- ☑ Commit: *"v1.0 — Phase 9 analytics, Phase 10 release docs, org cleanup"*

---

## System test — 2026-10-14

Admin-run system test through the API, with evidence: `docs/system-test-results-2026-10-14.md`. 11 scripts pass, two of them after a same-night fix. **Not UAT** — no outside users.
- ☑ `manifest/def01-retrieve.xml` retrieved and committed (in `main` since the StewardPhase5Updates push)

- ☑ **DEF-01 (High) fixed and retested 2026-10-14:** `Credits_Applied__c` + `Adjustment_AfterSave_ApplyCredits` + Balance formula; seeded credits backfilled. Was: posted credits don't reduce the statement balance. `Balance__c` = due − paid; adjustments look up to the statement, so no roll-up. A credited customer stays past due and on the work list. Fix: `Credits_Applied__c` on Billing Statement, summed by `Adjustment_AfterSave_Lifecycle` when an adjustment posts; `Balance__c` = due − paid − credits. Retest UAT-10/11.
- ☑ OBS-01 closed: Delete on Promise to Pay removed from `PS_Collections_Core`; no persona can delete a promise
- ☐ Persona checks as Test Persona: UAT-01, 05 step 4, 06, 08 (case comment), 12 negative, 13 criterion 3, 18 (your step 3 above)
- ☑ UAT-14: both milestones on **00001049** violated at their targets (checked 2026-10-24). The email arrival check is your step 4; delete the case after that
- ☑ UAT-04 step 3 confirmed on six promises (2026-10-24). ☐ Step 2 (Kept on a scheduled run) and UAT-20 (reminder) still have no example: the Oct 14 test contract was deleted before its reminder date
- ☑ UAT-15 steps 1–3: Default Reviews 00001051 and 00001052 opened on time by the nightly run (Oct 18, 19)
- ☑ An AI-written "all passed" UAT summary was checked against the org and rejected: no test records existed for the scripts it reported. Pass/fail in this repo comes only from evidence in the org.

---

## Verify before Phase 5

Quick confirmations, not real work. Each one is something that may or may not have been finished.

- ☑ Global value set descriptions — all four present (verified 2026-10-14)
- ☑ Service Contract org-wide default set to Private
- ☑ Admin user assigned to the Collections Supervisor role
- ☑ Test records gone — no account or statement without a Legacy Id (verified 2026-10-14)
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
- ☑ Four validation rule error messages reworded to name the fix (2026-10-14, through the Tooling API)
- ☐ Remaining Phase 5 screenshots if not yet taken: `phase05-duplicate-rule-config.png`, `phase05-duplicate-alert-in-action.png`, `phase05-data-loader-success.png`
- ☑ `data-plan.md` after numbers added — every target met (2026-10-14)

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
- ☑ Deliverability set to All email (2026-10-14)
- ☑ System Administrator access to Collections Console (verified)
- ☑ Email alert descriptions shortened (verified)
- ☐ Commit `data/regen/`, excluding the `del_*.csv` scratch files. (`Balance__c` is in `manifest/phase9-retrieve.xml`)
- ☑ `--line-ending LF` added to the runbook import commands
- ⊘ Separate sales persona app — sales reps use the standard Sales app; nothing in Accord's sales scope needs its own

### Phase 7 — automation ☑ built and tested 2026-10-09
- ☑ **Promises (US-03, US-04):** `Promise_AfterSave_ApplyPolicy`, `Promise_Daily_Evaluate`, `Account_Daily_BrokenPromiseCount`. Tested: second active promise blocked; in-policy promise set a hold to grace end; short promise went to Pending Approval with no hold.
- ☑ **Credits (US-11, US-13):** `Adjustment_AfterSave_Lifecycle`, Credit Approval process, `VR_Adjustment_ApprovalRequired`, `VR_Adjustment_AmountLockedAfterApproval`. Tested: $75 posted on its own; $250 blocked from manual approval, approved through the process, posted, dispute back to Under Review; approved amount locked.
- ☑ **Welcome and reminder (US-19, US-20, US-21):** `ServiceContract_AfterSave_WelcomeAndReminder`. Tested: welcome sent and stamped on activation; reminder scheduled. Fires only when a contract becomes active, so the existing 88 customers weren't emailed.
- ☑ **First scheduled runs confirmed** (Oct 10): ACC-0002 and ACC-0003 moved to Delinquent, modified by the automated process user; nothing else changed
- ☐ **Clock-dependent:** ACC-0051 (86 DPD) and ACC-0026 (85 DPD) cross 90 around Oct 18–19. Confirm the 1 AM run opens a Default Review for each, owned by the queue, and that Default Review Timeliness counts them on time. Screenshot the dashboard after.
- ☑ **Rejection reason on approval-process rejections** (US-11 criterion 3): approval field updates skip `VR_Adjustment_RejectionReason`, so `Adjustment_AfterSave_Lifecycle` now assigns the approver a high-priority task to record the reason when a credit is rejected without one. The task attaches to the account because activities aren't enabled on Adjustment. Tested: submit → reject with no reason → task created for the approver, dispute back to Under Review. Test records deleted.
- ☑ Admin self-approval documented (security model additions, README limits)
- ☑ Duplicated thresholds documented in README known limits
- ☑ **`VR_Case_RootCauseRequired`** (US-10): billing disputes can't be Resolved without a root cause; Closed (withdrawn) doesn't need one. Found missing while filling in traceability; built through the Tooling API and tested on CASE-0001.
- ☑ **US-06 contact attempt action** built in Phase 8: `Account_Screen_LogContactAttempt` + quick action
- ☑ Stray "Check" removed from Commitment Status (no records used it); description added
- ☑ Both validation rules added to `manifest/phase9-retrieve.xml`
- ☑ **Dispute lifecycle tested end to end** on a throwaway case (Paid statement STM-00452, ACC-0060): created with no entitlement → entitlement attached, routed to Dispute Specialists, 3 milestones started, statement In Dispute. Acknowledged → only Acknowledge completed. Sales rep added to case team, then jumped straight to Resolved → team member removed, both remaining milestones completed, statement back to Paid with Dispute Open cleared. Test case deleted.
- ☑ **Backfilled the 13 Phase 6 test disputes**: 12 passed milestones completed on open cases, 10 open disputes' statements flagged In Dispute.
- ☑ **Lesson: milestones lock once their case exits the entitlement process.** Completing milestones on the 3 already-closed test disputes was refused ("can't change the completion date on a milestone that's already exited an entitlement process"). The flow completes them inside the closing save, before they lock, so this only affects cases closed before the flow existed; their milestones stay as an honest record.
- ☑ **`Account_Daily_Collections_Status`** (scheduled, daily 1 AM ET) deployed from source and active. Sets Account Status from Days Past Due (Current / Delinquent / Default Review at the `Default_Threshold_DPD` policy setting), stamps Threshold Crossed Date, opens a Default Review case owned by the Default Reviews queue when none is open. Skips Closed and Hardship Review. Debug-tested on three accounts: ACC-0082 (14 DPD, Delinquent) and ACC-0060 (0 DPD, Current) took "Already correct" with no update; ACC-0001 (43 DPD, marked Current) moved to Delinquent.
- ☑ **Proved the security effect (D-08):** right after the debug run, Test Persona (Collections Rep) could read ACC-0001 and still could not read ACC-0002, the other mismatch account not yet run. Status drives visibility; the flow is what makes it accurate.
- ☑ **Case team removed on close** in `Case_AfterSave_DisputeLifecycle`. Done.
- ☑ **Disputed statement flagged** (Dispute Open, In Dispute) while the case is open; restored on close to Paid / Past Due / Open from its real balance and due date. Done.
- ☐ Confirm a case team member with Read can add case comments (US-08 says "read the case and add comments"); if comments need Edit, decide between a Sales Input permission and a quick action
- ☐ Account record types: the 12 Organization accounts each still have a service contract, though Organization is described as "not a lease holder." Remove those contracts or revise the description.
- ☑ **`Case_BeforeSave_StampEntitlement`**: new Billing Disputes without an entitlement get the account's active one, so the SLA starts. Done.
- ☑ **Milestones complete from status** in `Case_AfterSave_DisputeLifecycle`: Acknowledged → Acknowledge; Awaiting Evidence or later → Request Evidence; Resolved/Closed → Resolve; skipped stages complete too. Done.
- ⊘ Entitlement for new Residential Agreement accounts — recorded as a known limit in the README. `Case_BeforeSave_StampEntitlement` only attaches an existing one
- ☑ Default review flow sets the queue owner directly (flows can't run assignment rules)
- ☑ **Primary contact backfill**: all 100 accounts set to their Primary-role contact through the API. The Data Quality "no one to contact" tile should now read 0 (was 88).
- ☑ **`VR_Account_PrimaryContactRequired` active**: residential, not Closed, primary contact required. Refined from the Phase 5 plan to skip the first save (`NOT(ISNEW())`), because an account has to exist before its contact can be added. Tested: clearing a primary contact is blocked with the field-level message.
- ☑ **`Contact_AfterSave_StampPrimaryContact`** deployed and active. A Primary-role contact becomes the account's primary; an account with no primary takes its first contact as a stand-in. Tested end to end on a throwaway household: saved with no contacts, co-signer stamped as stand-in, Primary-role contact took over. Test records deleted (still in the Recycle Bin).
- ☑ **`Opportunity_AfterSave_CreateServiceContract`** + `VR_Opp_ConcessionNeedsCommitment` (US-02). Tested: close blocked without a commitment; after adding one, service contract created and commitment linked.
- ☑ Status flow documented and demonstrated as a security control (see CHANGELOG v0.6)
- ☑ Winter '27 sharing-recalculation constraint checked: no flow changes roles or groups, so none depends on same-transaction recalculation
- ☐ Consider Winter '27 mass screen flow action (`ids` collection) for bulk collections outcomes, and rely on Flow's row-lock auto-retry for the backfill
- ☑ `Dispute_Reason__c` text-match weakness recorded in README known limits

### Phase 8 — sales ☑ closed 2026-10-14
- ☑ Default record type for lead conversion: Minimum Access profile defaults to Residential Agreement (the one D-07 exception)
- ☑ Lead-to-Contact matching rule on email (`Contact_Match_Email_Only`) and alert duplicate rule; Standard Lead Duplicate Rule deactivated (verified inactive 2026-10-14)
- ☑ Web-to-lead form, `VR_Lead_EmailOrPhoneRequired`, lead routing to Inbound Leads — tested end to end
- ☑ US-06 contact attempt screen flow and quick action
- ☑ Real-looking email and phone on the web-form test lead replaced with fictional values
- ☑ CHANGELOG v0.7
- ⊘ Quotes — no story needs them
- ⊘ Forecast quotas — US-17 cut

### Phase 9 — analytics ☑ closed 2026-10-14
- ☑ 8 reports in `Collections`, Collections Supervisor dashboard, Collections Home page set as the console's home (replaces the default Sales home)
- ☑ Folders shared to the collections chain; Run Reports granted to reps and specialists
- ☑ Data Quality dashboard refreshed: 0 on every metric
- ☑ `VR_Case_DisputeNeedsStatement` built (US-07 criterion 4 was missing)
- ☑ CHANGELOG v0.8

### Phase 10 — release ☑ docs complete 2026-10-14
- ☑ README limits section: time zone, payment allocation, calendar-day review window, duplicated thresholds, two-license testing, entitlement versioning, volume
- ☑ UAT scripts, 21 (`docs/uat-scripts.md`)
- ☑ Root cause analysis — the $0 balance formula (`docs/rca-balance-formula.md`)
- ☑ One-page quick reference (`docs/quick-reference.md`)
- ☑ Case study (`docs/case-study.md`)
- ☑ CHANGELOG v1.0
- ☐ **Recruit 3–5 outside UAT testers**, run the scripts, collect sign-off. Re-age the data first.
- ☐ **Walkthrough video** (5 minutes: console home → work list → log contact attempt → promise → dispute → credit approval → dashboard)
- ☐ In-app guidance prompt (optional; the quick reference covers the same ground)
- ☐ Add to `conventions.md` under testing: *"Every formula gets a known-answer test: one record where the expected result is worked out by hand first, then compared."* (from the RCA)

---

## Recorded results

- ☑ **Data load: six distinct failure modes, all diagnosed from error files.** State and Country picklists rejecting plain values · Data Loader caching the schema before new fields existed · relationship columns needing different syntax per tool (colon for Data Loader, dot for Bulk API 2.0) · Legacy Id columns on objects that had no such field · picklist values entered with trailing commas or two values on one line · standard duplicate rules active by default and blocking API inserts. Full write-up in `data-plan.md`.

- ☑ **Metadata retrieve lessons.** Validation rules come back inside `CustomObject`, not as a standalone type. Folder-based metadata (reports, dashboards) needs exact `Folder/DeveloperName` names, found with `sf org list metadata --folder`, and private folders can't be retrieved at all. The dashboard's own XML is the source of truth for which reports it uses — that's how two unused copies were found and deleted.

- ☑ Security Health Check: **66% (Poor) → 96% (Excellent)** in one sitting. The single remaining Critical is trusted IP ranges, left unfixed deliberately and documented in `security-model.md`.
- ☑ Enabled "Require permission to view record names in lookup fields" — closes a leak where users who can't see a record can still see its name through a lookup.

---

## Time-sensitive

- ☑ **Winter '27 readiness review** written: `docs/release-readiness-winter27.md`. Instance USA838 upgrades **Oct 9, 2026, 11:00 PM CDT**.
- ☑ Profile Filtering enabled ahead of enforcement
- ☑ Upgrade landed; org on API 68.0 (confirmed 2026-10-14)
- ☐ Before Oct 9: screenshots `release-winter27-updates-before.png`, `release-winter27-overdue-before.png`, `release-winter27-profile-filtering-before.png`
- ☑ Post-upgrade checks through the API (2026-10-14): org on API 68.0, all 11 flows active, validation rules firing (new dispute rule tested), both dashboards refresh, duplicate rules in the right state
- ☐ Screenshot `release-winter27-after.png` (Release Updates page) and confirm Data Loader still logs in

---

## Found while preparing test cases (2026-10-08)

- ☑ **`Billing_Statement__c.Balance__c` formula was `Amount_Paid__c - Amount_Paid__c`** — always zero. Every statement showed a $0 balance, statement Days Past Due read 0, and the account roll-ups Current Balance and Past Due Balance summed to $0 across the whole book. Corrected to `Amount_Due__c - Amount_Paid__c` through the Tooling API; roll-ups recalculated to about $10,088 owed. Retrieve `CustomField:Billing_Statement__c.Balance__c` into the repo. Worth a line in the Phase 5 write-up: the data quality dashboard couldn't have caught it, because nothing measured balances.
- ☑ **Delinquency distribution doesn't match `data-plan.md`.** Fixed 2026-10-08: billing data regenerated with `data/regen/generate_billing.py` anchored to today and reloaded with the CLI (632 statements, 545 payments, 60 promises, 12 adjustments). Verified in the org: Current 52 · 1–30 14 · 31–60 10 (including the 3 seeded status mismatches) · 61–90 7 · 90+ 5. Original note: Plan: 14 accounts at 1–30 DPD, 10 at 31–60, 7 at 61–90, 5 at 90+. Org: 29 accounts at 146+ DPD (up to 484) and 1 at 64. Each account's statement series stops months or a year before today, so unpaid statements age past 90 days. Needs the billing data (statements, payments, promises) regenerated against today's date before Phase 7, since status stamping, default reviews, and the priority list all depend on it.
- ☑ Re-age routine exists: `data/regen/generate_billing.py` + `RUNBOOK.md`. Rerun before UAT and demos. Still document the drift in the README. Original note: **Static seed data drifts.** Days Past Due uses TODAY(), so even correct data ages a day every day and every account eventually lands in 90+. Plan a re-age routine to run before UAT and demos, and document the limit in the README.

## Org cleanup

- ☑ Stray field `Production_estimate_given_at_signing_Wh__c` deleted (2026-10-14)
- ☑ Custom `Payment__c` relabeled **Lease Payment** (verified 2026-10-14)
- ⊘ `Legacy_Id__c` on Lead kept: it ties the 30 seeded leads back to the source file, same reasoning as D-09
- ☑ `PS_Payment_Detail` label had a double space (`Payment  Detail`); corrected.
- ☑ **22 Developer Edition sample fields deleted** (2026-10-14; they sit in Deleted Fields for 15 days). Left on purpose: `Account.SLA__c` (used by sample Case assignment and escalation rule entries) and `Opportunity.TrackingNumber__c` + the Delivery Status link (on the four Opportunity layouts) — removing them means editing rules and layouts Accord doesn't use. Case Type and Case Reason sample values still need replacing in Setup. Original list: Case: `Product__c` (GenWatt model codes), `PotentialLiability__c`, `SLAViolation__c`, plus sample Type and Case Reason values (Mechanical, Electrical, Installation…). Account: `Active__c`, `CustomerPriority__c`, `NumberofLocations__c`, `SLA__c`, `SLASerialNumber__c`, `SLAExpirationDate__c`, `UpsellOpportunity__c`. Contact: `Languages__c`, `Level__c`. Lead: `CurrentGenerators__c`, `NumberofLocations__c`, `Primary__c`, `ProductInterest__c`, `SICCode__c`. Opportunity: `CurrentGenerators__c`, `DeliveryInstallationStatus__c`, `MainCompetitors__c`, `OrderNumber__c`, `TrackingNumber__c`. Delete, and replace Case Type and Reason values with ones that fit solar servicing.
- ☑ 6 sample Account and Case layouts deleted (2026-10-14)
- ☑ All 88 households renamed from their primary contact ("Patrick Boone Household"). 26 surnames had repeated, up to seven times
- ☑ `Experience_Profile_Manager` removed from the repo by `cleanup-local.ps1`
- ⊘ Dashboard API names are auto-generated (`KBzhEuJNWsMpcbnMzmuwzHqwlGrEtH`, and `…EtH1` for the supervisor dashboard, cloned from it). Cosmetic; recorded in CHANGELOG v0.8

---

## Doc updates

- ☑ `docs/security-model-additions.md` folded into `security-model.md` and deleted (2026-10-25)

- ☑ README rewritten for release (results incl. Health Check, US-xx/D-xx note, limits)
- ☑ `requirements.md` traceability complete (2026-10-14); US-17 marked cut
- ☑ `requirements.md` rewritten: acceptance criteria for all 21 stories, a summary table, and traceability filled in for what's built. US-21 retitled to match D-05 (consent gates promotional messages only).

- ☐ `data-model.md` — the object list at the bottom still describes the plan rather than what was built; reconcile after Phase 5

---

## Deliberately not doing

Written down so nobody mistakes these for oversights.

- ⊘ **Payment allocation object.** A payment spanning two statements can't be split. A production build would add a junction; this one documents the limit.
- ⊘ **Business-day math on the default review window.** Uses three calendar days, because business-day calculation in a formula needs Apex or a workaround. Deliberate simplification.
- ⊘ **Restriction rules.** Considered for tightening dispute visibility further; more than this build needs given the sharing model already in place (D-08).
- ⊘ **Custom Lightning components.** Three were candidates and all three use standard equivalents instead (D-04).
- ⊘ **Login IP ranges.** A remote workforce makes them impractical. MFA plus session timeout is the compensating control.
- ⊘ **Custom profiles.** Everything runs on Minimum Access plus permission set groups (D-07).
