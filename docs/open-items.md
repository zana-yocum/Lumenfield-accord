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

### Phase 6 — service
- ☑ **Account record types created** (2026-10-03): `Residential_Agreement` (88 accounts) and `Organization` (12 accounts, ACC-0089 to ACC-0100). Available on System Administrator (default Residential Agreement) and through `PS_Sales_Core` only. Collections doesn't need an assignment, because record type assignment governs create and change, not view or edit. Accounts bulk-assigned through the API and verified by count.
- ☐ Retrieve Account record types and `PS_Sales_Core`, `PS_Payment_Detail` into the repo
- ☐ Page layouts per Account record type (currently both use Account Layout)
- ☑ Case sharing rule `Billing_Disputes_to_Collections`: criteria-based, Billing Dispute record type, Read Only to the Collections Rep role. Supervisors already see disputes through the hierarchy; Default Review cases stay private.
- ☑ **Role hierarchy cleanup** (2026-10-07): nine Developer Edition sample roles deleted (VP North American Sales, VP International Sales, VP Marketing, two sales directors, four sales and marketing teams). Three of them sat directly under Dispute Specialist, which would have given dispute specialists upward visibility into any sales or marketing records. No users held them. Hierarchy is now Executive → VP Customer Operations → Collections Supervisor → (Collections Rep, Dispute Specialist), and Executive → VP Sales → Sales Manager → Sales Rep.
- ☐ Retrieve Case sharing rules and roles into the repo; delete local role files for the nine removed roles
- ☐ Assign app and tab visibility to each permission set group. Minimum Access users currently land on an empty home page with no tabs, reachable only through search and the App Launcher
- ☐ Negative test: sales rep opening a dispute case they aren't on the team for. Deferred from Phase 4 for lack of cases to test against
- ☐ Load dispute and default review cases into the dataset once record types exist
- ☐ Add the remaining `Dispute_Evidence_Requirement__mdt` records. Seven exist covering the top three reasons; still needed: Duplicate or Unauthorized Draft, Payment Not Posted, Annual Escalator Increase, Home Sale or Transfer, Outage or Repair Credit
- ☐ Read the Winter '27 Case Milestone fix in the Service release notes before building the entitlement process
- ☐ Second business hours record for outbound contact windows, which are narrower than support hours in collections
- ☑ **Case record types deployed from source** (2026-10-07): Billing Dispute and Default Review, each with its own support process. Seven new Case Status values added (Acknowledged, Awaiting Evidence, Under Review, Pending Credit Approval, Resolved, Cured, Default Confirmed). Available on System Administrator (default Billing Dispute) and on `PS_Dispute_Management` (Billing Dispute only, since default reviews are opened by automation). Status paths verified per record type through the UI API.
- ☐ Retrieve `PS_Dispute_Management` so its Case record type access is in the repo

### Phase 7 — automation
- ☐ **Activate `VR_Account_PrimaryContactRequired` only after the primary contact backfill runs.** Activated now, it would block every edit to all 88 residential accounts, since none have a primary contact yet. Also depends on Account record types existing.
- ☐ **Flow: stamp Primary Contact on Account** when the first contact is created. Replaces seed file 03, which couldn't load because Data Loader didn't expose the relationship by External ID. The flow is better anyway — it covers every new account, not just the seed set.
- ☐ **Flow: link Commitments to their Service Contract** at Closed Won. Replaces seed file 07 for the same reason, and it's the automation US-02 already requires.
- ☐ Document that the account status-stamping flow functions as a security control, not just a convenience — the delinquent-account sharing rule depends on status being accurate (D-08)
- ☐ **Design constraint from Winter '27 review:** no flow may assume sharing is recalculated in the same transaction as a role or group change (Spring '27 release update; D-08 depends on sharing)
- ☐ Consider Winter '27 mass screen flow action (`ids` collection) for bulk collections outcomes, and rely on Flow's row-lock auto-retry for the backfill
- ☐ Note the `Dispute_Reason__c` weakness in the automation inventory: it's plain text on the custom metadata type because custom metadata picklists can't inherit from a global value set, so the match to the value set is convention rather than enforcement

### Phase 8 — sales
- ☐ **Default record type for lead conversion.** Permission sets can grant record types but can't set a default; defaults come only from the profile. Sales reps on Minimum Access have no default Account record type, and lead conversion depends on one. Resolve before building conversion: test it, then decide whether the profile gets Residential Agreement as its default or the conversion process handles it.
- ☐ Lead-to-Contact matching rule on email (listed in `data-plan.md`, not yet built)
- ☐ Enable Quotes (Setup → Quote Settings), then add Quote, Product, and Price Book access to `PS_Sales_Core`
- ☐ Load forecast quotas via Data Loader

### Phase 10 — release
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

## Org cleanup

- ☐ Delete stray field `Production_estimate_given_at_signing_Wh__c` on Service Contract — a description pasted into a label on a second attempt at Est Annual Production
- ☐ Relabel custom `Payment__c` to **Lease Payment**. It shares a label with the standard Payment object, so the org shows two objects named Payment. API name stays `Payment__c`; nothing breaks.
- ☐ `Legacy_Id__c` on Lead isn't referenced by anything. Delete it, or document it as unused.
- ☑ `PS_Payment_Detail` label had a double space (`Payment  Detail`); corrected.
- ☐ **Developer Edition sample fields still on standard objects.** Case: `Product__c` (GenWatt model codes), `PotentialLiability__c`, `SLAViolation__c`, plus sample Type and Case Reason values (Mechanical, Electrical, Installation…). Account: `Active__c`, `CustomerPriority__c`, `NumberofLocations__c`, `SLA__c`, `SLASerialNumber__c`, `SLAExpirationDate__c`, `UpsellOpportunity__c`. Contact: `Languages__c`, `Level__c`. Lead: `CurrentGenerators__c`, `NumberofLocations__c`, `Primary__c`, `ProductInterest__c`, `SICCode__c`. Opportunity: `CurrentGenerators__c`, `DeliveryInstallationStatus__c`, `MainCompetitors__c`, `OrderNumber__c`, `TrackingNumber__c`. Delete, and replace Case Type and Reason values with ones that fit solar servicing.
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
