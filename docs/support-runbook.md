# Support Runbook — Accord

How to work the problems Accord's users are most likely to report. Every entry comes from something that actually happened in this org, during the build, the system test or a later check, and points to where it's written up. Use it like a support knowledge base: match the symptom, run the checks in order, apply the fix, then do the prevention step so the ticket doesn't come back.

**Before any check:** reproduce as the user, not as yourself. The admin can see and run everything, which is how DEF-08 went unnoticed. Setup → Users → find the user → **Login** (needs *Administrators can log in as any user* in Login Access Policies). Note the user's profile, role and permission set groups first.

| # | Symptom | Most likely cause |
|---|---|---|
| 1 | A button or action is missing for one group of users | The user can't run what the action launches (flow access), or a different layout is assigned |
| 2 | A user lands in Salesforce Classic, or can't find the Collections Console | Lightning Experience User or app visibility missing from their permission sets |
| 3 | A rep can't find an account a colleague can see | Account Status is stale, so the status-based sharing rule doesn't reach it |
| 4 | A rep has a case shared to them but gets "insufficient privileges" | Sharing grants record access, but the object permission is missing |
| 5 | A balance didn't go down after a credit | Credit not posted, posted to a different statement, or deleted after posting |
| 6 | Every balance shows $0 | The balance formula subtracts the wrong field |
| 7 | An account stays off the work list after a promise was broken or cancelled | The collection hold wasn't released |
| 8 | A new dispute has no SLA clock or milestones | The account has no active entitlement |
| 9 | Setup refuses a change to the entitlement process | The process is in use and versioning is off |
| 10 | A milestone can't be completed | The case already exited the entitlement process |
| 11 | Milestone alert emails never arrive | Deliverability is set to system email only |
| 12 | A rep can't open a report or sees an empty folder | Run Reports missing, or the folder isn't shared to their role |
| 13 | A sales rep can't convert a lead | Create on Account and Contact, or Convert Leads, missing |
| 14 | A data load rejects most rows | Restricted picklist mismatch, active duplicate rules or relationship column syntax |

---

## 1. A button or action is missing for one group of users

**Reported as:** "I don't have the Log Contact Attempt button. My supervisor does."

**Check, in order**
1. **Which layout does the user get?** Object Manager → Account → Page Layouts → **Page Layout Assignment**. Accord assigns by profile and record type: Minimum Access plus Residential Agreement gets the Residential Agreement Layout. Check the action is in that layout's *Salesforce Mobile and Lightning Experience Actions* section.
2. **What does the action launch?** Object Manager → Account → Buttons, Links, and Actions → the action. If it's a **Flow** action, the user needs either the **Run Flows** permission or access to that specific flow. Without either, Lightning hides the action; no error is shown.
3. **Does the user have flow access?** Setup → Flows → the flow → **Edit Access**: if *Override default behavior and restrict access to enabled profiles or permission sets* is on, only the listed permission sets can run it. Then check the user's groups for that permission set (Setup → Users → user → Permission Set Group Assignments).
4. **Other action types:** a Create action needs Create on the target object; a Lightning web component action needs access to its Apex classes (Steward's actions come from `PS_Steward_Rep_Assistant`).

**Fix:** grant access to the one flow through the persona's permission set (Permission Sets → the set → **Flow Access** → Edit → add the flow). Prefer this over Run Flows, which opens every current and future flow to the holder, including flows that run in system context.

**Prevent:** run every persona check as a logged-in persona before release, not only admin-run tests (`docs/persona-checks.md`).

**Happened:** DEF-08, found 2026-10-24 (`docs/system-test-results-2026-10-14.md`). No collections persona could log a contact attempt from the day the action was built, and Steward's Follow-up Draft was blocked behind it.

## 2. A user lands in Salesforce Classic, or can't find the Collections Console

**Check:** the user's profile is Minimum Access, which doesn't include **Lightning Experience User**. Accord grants it through `PS_Collections_Core`, `PS_Dispute_Management` and `PS_Sales_Core` (D-07: no custom profiles). Missing app in the App Launcher: the permission set needs the app's visibility (`Collections_Console`) and tab settings for the custom objects.

**Fix:** add the user to the right permission set group rather than editing the profile. If the user still lands in Classic once the permission is there, they can choose **Switch to Lightning Experience** from the Classic menu; Accord set Test Persona's preference to Lightning once.

**Happened:** Phase 6, 2026-10-07: the first login as Test Persona landed in Classic, where console apps don't exist (CHANGELOG v0.5).

## 3. A rep can't find an account a colleague can see

**Reported as:** "Global search doesn't find Melissa Sanders, but she's on the dashboard."

**Check**
1. Collections reps reach accounts only through the criteria-based sharing rule on **Account Status** (Delinquent or Default Review, D-08). Open the account as admin and look at Account Status and Days Past Due.
2. If Days Past Due says delinquent but Status says Current, the status is stale. `Account_Daily_Collections_Status` corrects it every night at 1 AM ET. Check Setup → Flows → the flow's recent runs, or the account's Last Modified By (the nightly run shows as the org's default workflow user).
3. Hardship Review and Closed accounts are skipped on purpose.

**Fix:** wait for the nightly run, or ask a supervisor to set the status (they reach accounts through the role hierarchy).

**Prevent:** don't change the sharing rule's criteria without changing the status flow with it; together they're the security control.

**Happened:** Phase 7, 2026-10-09: right after a debug run, Test Persona could read the corrected account and still not the one waiting for the nightly run (CHANGELOG v0.6).

## 4. A case is shared to a rep, but opening it says "insufficient privileges"

**Check:** sharing (rules, teams, queues) only opens records the user's object permissions allow. If the user's permission sets have no **Read** on Case, a Read share does nothing. Setup → Permission Set Groups → the group → **Object Settings** → Cases.

**Fix:** add Read on Case to the base permission set; add field-level security for the fields they need. Accord's case access: Collections Rep Read; Supervisor and Dispute Specialist Read, Create and Edit; Sales Rep Read (for case teams); no Delete anywhere.

**Happened:** Phase 6, 2026-10-07: the billing dispute sharing rule worked but reps still couldn't open disputes, because `PS_Collections_Core` had no Case access (CHANGELOG v0.5).

## 5. A balance didn't go down after a credit

**Check**
1. The adjustment's Status must be **Posted**. Adjustments over the rep's limit go through the Credit Approval process first and post on approval.
2. The adjustment must point at the right Billing Statement.
3. On the statement, **Credits Applied** should equal the sum of its posted adjustments, and **Balance** = due − paid − credits, never below $0.
4. If a posted adjustment was deleted, Credits Applied isn't recalculated: record-triggered flows can't run after delete. No persona can delete adjustments, so this is an admin action.

**Fix:** correct the adjustment, then save it again so `Adjustment_AfterSave_ApplyCredits` recomputes the statement.

**Happened:** DEF-01, 2026-10-14: before the fix, posted credits never reduced any balance (`docs/system-test-results-2026-10-14.md`).

## 6. Every balance shows $0

**Check:** open the formula: Object Manager → Billing Statement → Fields → **Balance**. It must subtract Amount Paid and Credits Applied from **Amount Due**. A formula that subtracts a field from itself returns 0 for every record, and every roll-up built on it reads $0 too.

**Prevent:** every formula gets a known-answer test: one record where the result is worked out by hand first.

**Happened:** 2026-10-08: `Amount_Paid__c - Amount_Paid__c` made the whole book read $0, and the data-quality dashboard couldn't catch it because nothing measured balances (`docs/rca-balance-formula.md`).

## 7. An account stays off the work list after a promise was broken or cancelled

**Check:** the account's **Collection Hold Until**. An in-policy promise sets it to the promise's grace end; `Promise_Daily_Evaluate` clears it the morning after grace, when it judges the promise Kept or Broken. The Collections Work List leaves out accounts on hold.

**Fix:** if the promise was deleted rather than cancelled, the hold stays: clear Collection Hold Until by hand. Cancelled is the supported way out of a promise; no persona can delete one.

**Happened:** OBS-01, 2026-10-14: a deleted promise left a customer on hold for ten more days (CHANGELOG v1.0.1). Confirmed working on schedule 2026-10-24: six broken promises released their holds.

## 8. A new dispute has no SLA clock or milestones

**Check:** the case's **Entitlement**. `Case_BeforeSave_StampEntitlement` attaches the account's active entitlement to a new billing dispute. The 88 seeded households each have one; a household created later doesn't get one automatically (README, known limits).

**Fix:** create an entitlement on the account pointing at **Billing Dispute SLA**, then set it on the case.

## 9. Setup refuses a change to the entitlement process

**Message:** "Cannot update SLA process that is in use."

**Cause:** once any case has used the process, even a deleted test case, it locks. Detaching entitlements and emptying the Recycle Bin doesn't release it.

**Fix:** milestone actions can still be added in Setup. For structural changes, enable entitlement versioning (Entitlement Settings) and create a new version. In production, enable versioning before go-live.

**Happened:** Phase 6 (CHANGELOG v0.5).

## 10. A milestone can't be completed

**Message:** "can't change the completion date on a milestone that's already exited an entitlement process."

**Cause:** milestones lock when their case exits the process (closed). `Case_AfterSave_DisputeLifecycle` completes them inside the closing save, before they lock; cases closed before that flow existed keep their incomplete milestones as an honest record.

## 11. Milestone alert emails never arrive

**Check:** Setup → **Deliverability** → Access level. *System email only*, the default in new sandboxes, silently drops workflow and flow emails; this org was moved to *All email* on 2026-10-14. Then check the alert's recipients: Accord's warning goes to the case owner (a queue, which emails its members) and the violation to the owner and the Collections Supervisor role.

**Note:** an email alert leaves no record the API can read. To confirm delivery, check a recipient's inbox, or request an email log (Setup → Email Log Files).

**Happened:** set to All email on 2026-10-14; UAT-14's violations on 2026-10-15 and 10-19 are the first real test.

## 12. A rep can't open a report, or sees an empty folder

**Check:** the **Run Reports** permission (Accord grants it through `PS_Collections_Core` and `PS_Dispute_Management`), then the folder's sharing (Reports → folder → Share): Collections folders give View to VP Customer Operations and subordinates, Edit to Collections Supervisor.

**Happened:** Phase 9, 2026-10-14: reps couldn't open their own work list until Run Reports was added (CHANGELOG v0.8).

## 13. A sales rep can't convert a lead

**Check:** converting creates an account, a contact and an opportunity, so the user needs Create on all three plus the **Convert Leads** permission. `PS_Sales_Core` grants them since 2026-10-14.

**Happened:** changed in the org on 2026-10-14 without a write-up; reconstructed from the Setup Audit Trail on 2026-10-24.

## 14. A data load rejects most rows

Read the job's error file before changing anything; it names the cause.

| Error in the file | Cause | Fix |
|---|---|---|
| `INVALID_OR_NULL_FOR_RESTRICTED_PICKLIST` | The value doesn't exactly match a picklist value. Once, the org's own value had a trailing comma | Correct the source or the picklist value |
| `DUPLICATES_DETECTED` | A duplicate rule set to Block fires on API inserts, which can't prompt | Change the rule to Allow with alert, or load before activating it |
| `MALFORMED_ID` on a lookup | The column maps to the ID field instead of the External ID relationship | Map `Account:Legacy_Id__c` (Data Loader) or `Account.Legacy_Id__c` (Bulk API 2.0) |
| Every account rejected on state | State and Country picklists are on | Use the `StateCode` and `CountryCode` columns |

**Happened:** Phase 5, six failure modes (`docs/data-plan.md`; error files in `data/load-results/`).

## 15. A user can edit or see a field their role shouldn't

**Check**
1. **Start with the profile, not the permission sets.** A field is visible if *anything* grants it: the profile or any permission set. Object Manager → the object → Fields & Relationships → the field → **Set Field-Level Security** shows every profile's access. Minimum Access should show none on Accord's fields.
2. Then the user's groups: Setup → Permission Set Groups → the group → **Object Settings** → the object, which shows the group's combined field access.
3. To check one user without logging in as them, the API answers directly: `UserFieldAccess` for that user and field returns readable and editable.

**Fix:** grant the field in the persona's permission set, then remove it from the profile, in that order so nobody loses access in between. Automation-maintained account fields (Account Status, Collection Hold Until, High Value) are editable only through `PS_Collections_Overrides`, in the supervisor group.

**Prevent:** in Setup's new-field wizard, clear every profile box on the field-level security step. The wizard ticks them all by default.

**Happened:** DEF-09, found 2026-10-24: the profile granted access to 74 Accord fields, so reps and sales reps could edit Account Status, which drives the collections sharing rule. Fixed 2026-10-25 (results doc).

---

## Writing up a fix

Every fix gets a line in `CHANGELOG.md` and, if it was a defect, a write-up with what was found, the cause, the effect, the fix and how it was verified (see DEF-01, DEF-08 and DEF-09 in the results doc). A change made in Setup is retrieved into `force-app/` the same day (`manifest/accord.xml`). A change with no record is how DEF-02 to DEF-06 were lost.
