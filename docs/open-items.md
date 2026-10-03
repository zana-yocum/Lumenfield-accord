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
- ☐ Commit Phase 5 to GitHub
- ☐ Remaining Phase 5 screenshots if not yet taken: `phase05-duplicate-rule-config.png`, `phase05-duplicate-alert-in-action.png`, `phase05-data-loader-success.png`
- ☐ `data-plan.md` — add the after numbers to the measurement table (duplicates 0, roles 0, statement dates 0)

### Phase 6 — service
- ☐ **Create Account record types** — Residential Agreement and Organization. Listed in the data dictionary but never built in Phase 3. Assign through permission sets, set page layouts, then bulk-assign the twelve organization accounts with a CLI update. Until then, reports isolate residential accounts by name ("Household").
- ☐ Case sharing rule `Billing_Disputes_to_Collections` — couldn't be built in Phase 4 because it filters on a record type that doesn't exist yet
- ☐ Assign app and tab visibility to each permission set group. Minimum Access users currently land on an empty home page with no tabs, reachable only through search and the App Launcher
- ☐ Negative test: sales rep opening a dispute case they aren't on the team for. Deferred from Phase 4 for lack of cases to test against
- ☐ Load dispute and default review cases into the dataset once record types exist
- ☐ Add the remaining `Dispute_Evidence_Requirement__mdt` records. Seven exist covering the top three reasons; still needed: Duplicate or Unauthorized Draft, Payment Not Posted, Annual Escalator Increase, Home Sale or Transfer, Outage or Repair Credit
- ☐ Second business hours record for outbound contact windows, which are narrower than support hours in collections
- ☐ Case record types (Billing Dispute, Default Review) with their own support processes and page layouts

### Phase 7 — automation
- ☐ **Activate `VR_Account_PrimaryContactRequired` only after the primary contact backfill runs.** Activated now, it would block every edit to all 88 residential accounts, since none have a primary contact yet. Also depends on Account record types existing.
- ☐ **Flow: stamp Primary Contact on Account** when the first contact is created. Replaces seed file 03, which couldn't load because Data Loader didn't expose the relationship by External ID. The flow is better anyway — it covers every new account, not just the seed set.
- ☐ **Flow: link Commitments to their Service Contract** at Closed Won. Replaces seed file 07 for the same reason, and it's the automation US-02 already requires.
- ☐ Document that the account status-stamping flow functions as a security control, not just a convenience — the delinquent-account sharing rule depends on status being accurate (D-08)
- ☐ Note the `Dispute_Reason__c` weakness in the automation inventory: it's plain text on the custom metadata type because custom metadata picklists can't inherit from a global value set, so the match to the value set is convention rather than enforcement

### Phase 8 — sales
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

- ☐ **Winter '27 readiness review.** First production upgrade weekend is underway (October 3, 2026); the second is October 10. Check the org's current release version first (Setup → Company Information, or the release name at the top of Setup Home). If the org hasn't upgraded yet, write the review before October 10 so it shows what was assessed in advance. Covers the Flow Builder canvas redesign, pending Release Updates, and the release update ending username-and-password logins for integrations.

---

## Org cleanup

- ☐ Delete stray field `Production_estimate_given_at_signing_Wh__c` on Service Contract — a description pasted into a label on a second attempt at Est Annual Production
- ☐ Relabel custom `Payment__c` to **Lease Payment**. It shares a label with the standard Payment object, so the org shows two objects named Payment. API name stays `Payment__c`; nothing breaks.
- ☐ `Legacy_Id__c` on Lead isn't referenced by anything. Delete it, or document it as unused.
- ☐ Dashboard API name is auto-generated (`KBzhEuJNWsMpcbnMzmuwzHqwlGrEtH`). Cosmetic; document it as a platform default rather than chase a rename.

---

## Doc updates pending

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
