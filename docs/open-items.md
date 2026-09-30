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

### Phase 5 — data load
- ☐ Delete the sample data that ships with Developer Edition (Edge Communications, Burlington Textiles, and so on) before loading the Lumenfield dataset. A reviewer clicking through should never see it.
- ☐ Seed 5–10% deliberate defects into the dataset so the data quality work has a real baseline to improve

### Phase 5 — data load
- ☑ `Legacy_Id__c` External ID fields on Account, Contact, Opportunity, Service Contract, Billing Statement (D-09)
- ☑ Dataset loaded via CLI bulk import: 100 accounts, 135 contacts, 100 opportunities, 31 commitments, 100 service contracts, 570 statements, 518 payments, 60 promises, 12 adjustments, 30 leads
- ☐ Delete "Sample Account for Entitlements" and the 22 Developer Edition sample leads
- ☐ Confirm no other sample data survived: Contact, Opportunity, Case counts with null Legacy Id should be zero
- ☐ Set record type to Organization on the twelve HOA and property-manager accounts
- ☐ Build the five data quality reports and capture the baseline **before** any cleanup
- ☐ Build matching rules, duplicate rules, and validation rules — then reactivate or replace the standard duplicate rules

### Phase 6 — service
- ☐ Case sharing rule `Billing_Disputes_to_Collections` — couldn't be built in Phase 4 because it filters on a record type that doesn't exist yet
- ☐ Assign app and tab visibility to each permission set group. Minimum Access users currently land on an empty home page with no tabs, reachable only through search and the App Launcher
- ☐ Negative test: sales rep opening a dispute case they aren't on the team for. Deferred from Phase 4 for lack of cases to test against
- ☐ Load dispute and default review cases into the dataset once record types exist
- ☐ Add the remaining `Dispute_Evidence_Requirement__mdt` records. Seven exist covering the top three reasons; still needed: Duplicate or Unauthorized Draft, Payment Not Posted, Annual Escalator Increase, Home Sale or Transfer, Outage or Repair Credit
- ☐ Second business hours record for outbound contact windows, which are narrower than support hours in collections
- ☐ Case record types (Billing Dispute, Default Review) with their own support processes and page layouts

### Phase 7 — automation
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

- ☑ Security Health Check: **66% (Poor) → 96% (Excellent)** in one sitting. The single remaining Critical is trusted IP ranges, left unfixed deliberately and documented in `security-model.md`.
- ☑ Enabled "Require permission to view record names in lookup fields" — closes a leak where users who can't see a record can still see its name through a lookup.

---

## Time-sensitive

- ☐ **Winter '27 readiness review.** Production upgrade weekends are October 3 and October 10, 2026. The review is worth more written *before* the upgrade hits the org, showing what was assessed and tested in advance. Covers the Flow Builder canvas redesign, pending Release Updates, and the release update ending username-and-password logins for integrations.

---

## Org cleanup

- ☐ Delete stray field `Production_estimate_given_at_signing_Wh__c` on Service Contract — a description pasted into a label on a second attempt at Est Annual Production
- ☐ Relabel custom `Payment__c` to **Lease Payment**. It shares a label with the standard Payment object, so the org shows two objects named Payment. API name stays `Payment__c`; nothing breaks.
- ☐ `Legacy_Id__c` on Lead isn't referenced by anything. Delete it, or document it as unused.

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
