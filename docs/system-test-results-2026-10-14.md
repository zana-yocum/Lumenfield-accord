# System Test Results — 2026-10-14

| | |
|---|---|
| Type | **System test, AI-executed through the Salesforce API, with evidence.** Not user acceptance testing — no outside users took part. |
| Executed by | Claude, via the org's REST and Tooling APIs, running as the System Administrator |
| Org | Lumenfield Developer Edition, Winter '27 (API 68.0) |
| Window | 2026-10-14, 8:04–8:15 PM CT |
| Scripts | `docs/uat-scripts.md` |
| Cleanup | All test records deleted afterward, except dispute 00001049, left open on purpose for UAT-14 |

**What "admin-run" means here:** these tests prove the automation, validation rules, routing and approvals behave as specified. They do not prove what a *persona* can see, because the admin sees everything. Visibility checks are listed separately below and still need a person logged in as Test Persona.

---

## Summary

| Result | Count | Scripts |
|---|---|---|
| Pass | 11 | 02, 03, 05, 07, 09, 10, 11, 13, 16, 19, 21 |
| Pass after fix | 1 | 10/11 — DEF-01 found, fixed and retested the same night |
| Partial — clock-dependent step pending | 3 | 04, 19 (reminder), 20 |
| Clock-dependent, scheduled | 2 | 14 (business hours, Oct 15), 15 (≈ Oct 18–19) |
| Needs persona login | 5 | 01, 06, 08, 12 negative, 18 |
| Not applicable | 1 | 17 (cut) |

The rows overlap: UAT-10 and 11 appear as Pass and as Pass after fix, and UAT-19 as Pass and Partial. **Distinct scripts passed: 11.** (The v1.0.1 changelog first said 12, counting DEF-01's retest twice; corrected 2026-10-24.) Later results, from the scheduled runs and from persona use, are below under *Confirmed after 2026-10-14*.

---

## Results

### UAT-02 — A concession can't go unrecorded · **Pass**
| Step | Result | Evidence |
|---|---|---|
| Concession = Yes, Closed Won, no Commitment | Blocked: "Add a Commitment record describing the concession before closing this deal as won." | Opp 006aj00000fKnEf |
| Add Commitment, then Closed Won | Saved; Service Contract created; commitment COM-00033 linked to it | SC 810aj0000XYHqDp |
| Concession = No, Closed Won | Saved, nothing blocked; Service Contract created | Opp 006aj00000fKnEg |

### UAT-03 — Promise within policy · **Pass**
| Step | Result | Evidence |
|---|---|---|
| $129.02 promise, 7 days out, Crystal Stinson | Active; Grace Ends Oct 24; account Collection Hold Until = Oct 24 | PTP-00139 |
| Second promise, same account | Blocked: "This account already has an active promise to pay…" | — |
| Promise 47 days out, Sandra Hargrove | Pending Approval, Out of Policy = true, **no hold set** | PTP-00141 |
| $0 promise | Blocked: "Enter a promise amount greater than zero." | — |

### UAT-04 — Kept or broken · **Partial**
| Step | Result |
|---|---|
| Payment dated tomorrow | Blocked: "Enter today's date or earlier…" |
| $0 payment | Blocked: "Enter an amount greater than zero. To reduce a balance, create a credit Adjustment instead." |
| Kept/Broken evaluation | **Pending.** `Promise_Daily_Evaluate` only judges a promise after its grace date. Verified by debug run in Phase 7; to confirm on a scheduled run, check any Active promise the morning after its grace date |

### UAT-05 — Prioritized work list · **Pass**
| Step | Result |
|---|---|
| Run Collections Work List | Sorted by Priority Score descending; DPD, past-due balance, broken promises on every row |
| After UAT-03's in-policy promise | Crystal Stinson gone from the list: 35 → 34 |
| Out-of-policy (pending) promise | Sandra Hargrove stays on the list — correct, no hold until approved |
| Do Not Contact on William Okafor | Gone from the list: 34 → 33 |
| Step 4 (mismatch account hidden from a rep) | Needs persona login. The Phase 7 check that seemed to prove it didn't: see DEF-10 |

### UAT-07 — Guided dispute intake · **Pass**
| Step | Result | Evidence |
|---|---|---|
| Billing Dispute on STMT-00917 | Owner = Dispute Specialists queue; entitlement Billing Dispute SLA attached; statement In Dispute, Dispute Open = true | Case 00001048 |
| Billing Dispute with no statement | Blocked: "Choose the disputed statement…" | — |
| Evidence checklist on screen | Not checkable through the API — UI step |

### UAT-09 — SLA clock · **Pass**
Case opened Wed Oct 14, 9:05 PM ET (after hours).
| Milestone | Target | Expected |
|---|---|---|
| Acknowledge (1 business day) | Thu Oct 15, 6:00 PM ET | ✓ |
| Request Evidence (3) | **Mon Oct 19**, 6:00 PM ET | ✓ weekend skipped |
| Resolve (10) | Wed Oct 28, 6:00 PM ET | ✓ |

Status → Acknowledged completed only Acknowledge. Status → Resolved completed the remaining two.

### UAT-10 — Root cause on resolve · **Pass**
| Step | Result |
|---|---|
| Resolved with no root cause | Blocked: "Choose a root cause before resolving this dispute." |
| Resolved with Concession Not Recorded at Signing | Saved; all milestones complete; statement Dispute Open cleared, status restored |

### UAT-11 — Credit above my limit · **Pass (defect found — DEF-01)**
| Step | Result | Evidence |
|---|---|---|
| $75 Billing Correction | Posted immediately, Posted Date = today | — |
| $250, set Approved by hand | Blocked: "Credits over the rep limit need supervisor approval…" | — |
| $250 Submit for Approval | Pending; dispute → Pending Credit Approval | — |
| Reject with no reason | Approver got a **High** priority task "Record why the Billing Correction of $250 was rejected"; dispute → Under Review | — |

### UAT-13 — Approve credits with context · **Pass**
| Step | Result |
|---|---|
| $139.29 submitted and approved | Status Posted, Posted Date today; dispute back to Under Review |
| Change amount after approval | Blocked: "This credit is already approved…" |
| Criterion 3, submitter can't self-approve | **Not testable as admin** — System Administrators can approve anything (documented limit). Needs Test Persona as Dispute Specialist |

### UAT-16 — Website leads · **Pass**
| Step | Result |
|---|---|
| No email, no phone | Blocked: "Enter an email address or phone number…" |
| Existing customer's email | Duplicate rule `Lead_Matches_Existing_Customer` matched contact at **100%**, `allowSave: true` |
| Saved | Owner = Inbound Leads; Service Address and Inquiry Detail populated |

Web form path itself was tested end to end in Phase 8.

### UAT-19 — Welcome after activation · **Pass**
Activating a contract stamped Welcome Sent On = today. Delivery to `example.com` isn't observable. Reminder (scheduled path, Oct 21) not observed — see UAT-20.

### UAT-21 — No promotional contact without consent · **Pass**
Activating a contract on a Do Not Contact account: Welcome Sent On stayed blank — nothing sent. No promotional automation exists (D-05). *Script corrected:* it expected a follow-up task here; US-21 doesn't require one and the flow doesn't create one.

---

## Confirmed after 2026-10-14

Checked through the API on 2026-10-24, from records the scheduled flows and the SLA clock changed on their own.

### UAT-04 step 3 — Broken promise · **Pass**
Six promises passed their grace date with nothing received between Oct 15 and Oct 24. Each was set to Broken by `Promise_Daily_Evaluate` the morning after grace ended, and the next day `Account_Daily_BrokenPromiseCount` raised the account's Broken Promises (90d) to 1. Each account's Collection Hold Until is empty, so the hold was released.

| Promise | Grace ended | Broken on | Account |
|---|---|---|---|
| PTP-00075 | Oct 14 | Oct 15 | Melissa Abernathy Household (ACC-0087) |
| PTP-00073 | Oct 16 | Oct 17 | Anthony Coffey Household (ACC-0006) |
| PTP-00078 | Oct 17 | Oct 18 | Tonya Boone Household (ACC-0082) |
| PTP-00076, PTP-00077 | Oct 20 | Oct 21 | Carla Vance Household (ACC-0047), Sandra Mabry Household (ACC-0061) |
| PTP-00079 | Oct 23 | Oct 24 | Derek Fitch Household (ACC-0065) |

Step 2 (a promise judged Kept on a scheduled run) still has no example: none of the promises that came due had a payment against them. The Kept branch was proven by a debug run in Phase 7.

### UAT-14 — Milestone alerts · **Pass in the org; email arrival not checked**
Dispute **00001049** was opened Oct 14 at 8:06 PM CT and left untouched. Acknowledge Dispute (target Oct 15, 6:00 PM ET) and Request Evidence (target Oct 19, 6:00 PM ET) are both flagged violated and not completed, so Milestone Status reads Open Violation. Resolve Dispute (target Oct 28) isn't violated yet. The warning and violation emails go to the owning queue's members and the Collections Supervisor role; an email alert leaves no record the API can read, so arrival is a check in the supervisor's inbox. For the negative step, the seven test disputes acknowledged before their target (00001032 to 00001038) show Acknowledge completed and not violated, so no violation alert was due for them.

### UAT-15 — Default threshold and review timeliness · **Pass (steps 1–3)**
| Account | Crossed 90 DPD | Default Review | Owner | Opened on time |
|---|---|---|---|---|
| Melissa Sanders Household (ACC-0051) | Oct 18 | 00001051, created by the nightly run Oct 18 | Default Reviews queue | ✓ |
| Brittany Abernathy Household (ACC-0026) | Oct 19 | 00001052, created by the nightly run Oct 19 | Default Reviews queue | ✓ |

Account Status moved to Default Review and Threshold Crossed Date was stamped on both. Each account has exactly one Default Review, after more nightly runs (step 3). These are the first two reviews opened on time; the five from before the automation stay as late. The scheduled runs are recorded as the org's default workflow user (OrgFarm EPIC). Step 4 (cured by payment) wasn't run.

**More runs, checked 2026-11-03.** Five more accounts crossed 90 days past due as the data aged, and the morning run opened a review for each, on time and owned by the queue: 00001055 and 00001056 (ACC-0009, ACC-0021) on Oct 28, 00001057 (ACC-0067) on Oct 31, 00001058 (ACC-0083) on Nov 1 and 00001059 (ACC-0084) on Nov 2. Each was created between 5:00 and 5:10 AM Eastern, which is how the run time was found to be 5 AM, not the 1 AM the docs said (DEF-12, below).


### Persona checks through the API (2026-10-26)
The scripts that need a persona login, checked as Test Persona (Collections Rep) without logging in: what it can read and edit, record by record (`UserRecordAccess`) and field by field (`UserFieldAccess`), the permissions and folder shares behind it, and, for the one question only an action can answer, a short Apex test run as Test Persona that saves in user mode, so object access and sharing apply as they do in the console. The test was created in the org, run once and deleted; nothing it saved was kept. Steward's hand check, the same day, covers the console itself.

| Script | Result | Evidence |
|---|---|---|
| UAT-01 — one screen for a past-due account | **Pass** | Residential Agreement accounts open on the Residential Agreement layout for Test Persona's profile. Balances, days past due, bucket, priority score and broken promises readable, read-only; Primary Contact and Do Not Contact editable; the layout lists promises, statements, cases and commitments, and commitments on accounts in collections are readable. A current account's fields read $0, 0 days and Current rather than blank (Jeffrey Naylor Household, reachable through dispute 00001049). Payment Method and External Reference not readable; amount and date readable. Steward's hand check opened a delinquent account in Collections Console as Test Persona |
| UAT-05 step 4 — a stale status hides the account | **Pass** | Patrick Boone Household (Delinquent) readable and editable; Regina Mundy Household (Current, no disputes) not readable, nor its contacts, statements or deal (DEF-10) |
| UAT-06 — structured contact attempt | **Partly** | Step 1 in the console: Test Persona logged a Left Voicemail attempt on Sandra Barnett Household (completed task, outcome recorded, owned by Test Persona, Oct 26). Steps 2–5 confirmed in the flow's definition: the outcome is required, Promise Made continues into the promise screen, Requested No Further Contact sets Do Not Contact and Hardship sets Hardship Review, in system mode with sharing. Not yet run as a rep |
| UAT-08 — the sales rep's side | **Fail at step 2a (DEF-11)** | A case comment needs edit access to the case. Test Persona, with Case Read, was refused a comment both with read-only sharing and as a Sales Input team member: "insufficient access rights on cross-reference id". A post to the case's feed saved. Steps 1, 2, 3 and 4 hold: the Sales Input team role exists; the Phase 6 negative test showed a team member reads the case and a non-member can't; the Phase 7 test showed the team is removed at close |
| UAT-12 step 4 — reps don't see default reviews | **Pass** | None of the 7 Default Review cases readable by Test Persona, so Default Review Timeliness shows it none. The Collections report folder is shared for viewing with VP Customer Operations and subordinates, and the rep group has Run Reports |
| UAT-13 criterion 3 — no approving your own credit | **Pass (configuration)** | The Credit Approval process takes submissions from the Collections Rep and Dispute Specialist roles and assigns every request to one named approver, the supervisor. A specialist who submits is never the approver |
| UAT-18 — a sales rep on a dispute naming their deal | **Pass** | The Sales Rep group has no access to Lease Payment, Billing Statement or Adjustment, so no payment detail can show inside a case team. Case fields are read-only to it, the disputed statement hidden. Team access ends at close (Phase 7) |

---

## Defects and observations

### DEF-01 — Posted credits don't reduce the statement balance · **High · Fixed and retested 2026-10-14**
**Found in:** UAT-10/11. STMT-00917 owed $214.29. Two credits totalling $214.29 posted against it. Balance afterward: **$214.29**. Statement status restored to Past Due.

**Cause:** `Balance__c = Amount_Due__c - Amount_Paid__c`. Nothing subtracts posted adjustments. Adjustment looks up to the statement rather than master-detail, so a roll-up summary isn't available.

**Effect:** a customer who wins a dispute and gets credited stays past due, keeps their priority score and stays on the work list. That's the opposite of what Accord promises.

**Fix:**
- New field `Billing_Statement__c.Credits_Applied__c` (currency, read-only to personas)
- New flow `Adjustment_AfterSave_ApplyCredits`: after any adjustment save, sums the statement's Posted adjustments into Credits Applied; marks the statement Paid when credits clear it and no dispute is open. A separate flow rather than a change to `Adjustment_AfterSave_Lifecycle`, so the credit math has one job and can be tested alone
- `Balance__c` = `MAX(0, Amount_Due__c - Amount_Paid__c - Credits_Applied__c)`. The floor keeps a credit larger than the statement from going negative; it doesn't carry forward (same no-allocation limit as payments)
- Backfill: the 5 seeded posted credits written to their statements. STMT-00806 ($221.60 due, $420 credited) became Paid

**Retest (same steps as UAT-10/11):**
| Step | Result |
|---|---|
| $75 credit posts on STMT-00917 ($214.29 owed) | Credits Applied 75, Balance **$139.29**, status stays In Dispute |
| $139.29 credit approved through the approval process | Credits Applied 214.29, Balance **$0** — approval-posted credits counted too |
| Dispute resolved | Statement **Paid**; account Past Due Balance $0, Days Past Due 0 — off the work list |

**Known limit:** deleting a posted adjustment doesn't recompute Credits Applied (record-triggered flows can't run after delete). No persona can delete adjustments.

### OBS-01 — Deleting an active promise leaves the hold in place · Low · **Closed 2026-10-14**
Deleting PTP-00139 left Crystal Stinson's Collection Hold Until = Oct 24, keeping her off the work list. Cleared by hand. **Fix:** Delete removed from Promise to Pay in `PS_Collections_Core`, the only permission set that granted it. Verified no persona can delete a promise; the Cancelled status is the way out of a promise.

### OBS-02 — Script corrections
- UAT-11 and the quick reference said Adjustment type "Credit." The real values are Billing Correction, Goodwill Credit and Production Guarantee.
- UAT-21 step 2 expected a follow-up task the requirement doesn't call for.

### DEF-07 — Commitments didn't show on the account page · Medium · **Fixed in the org Oct 14; written up 2026-10-24**
Made the evening of Oct 14, about 8:48 PM CT, after the v1.0.1 docs were written, and not recorded anywhere until now; the details come from the Setup Audit Trail and the components' own descriptions.

**Gap:** commitments are detail records of the opportunity, so collections and dispute staff working an account couldn't see what was promised at signing without opening the deal. That's the problem Accord exists to solve (US-01).

**Fix:** lookup `Commitment__c.Account__c` (read-only to every persona) and the before-save flow `Commitment_BeforeSave_StampAccount`, which copies the opportunity's account onto each commitment on every save, so the opportunity stays the source of truth. All 31 commitments were stamped. Steward's commitments read service filters on this field.

**Finished 2026-10-25:** the Residential Agreement layout never got the Commitments related list, so the goal wasn't met on the page. The layout is maintained in Steward's repository (Steward S-21), so the list went in through Steward's pull request #13 (deploy `0Afaj00000p7b8jCAA`). Checked in the org: the list shows each commitment's type, value and status.

**Numbering:** the flow cites DEF-07, but DEF-02 to DEF-06 were never written down. The same 20 minutes of the audit trail hold the four other changes below; they may be those defects, but the numbers can't be matched to them, so they're recorded without numbers.

### Changes made the same evening (recorded 2026-10-24 from the audit trail)
- **Minimum Access profile:** field-level security on Lease Payment Method and External Reference changed from Read/Write to No Access (8:30 PM CT). Before this, every persona on the profile could read payment details that only `PS_Payment_Detail` should grant (UAT-01's expectation). Rechecked 2026-10-24: only `PS_Payment_Detail` and the Collections Supervisor group read those two fields.
- **`PS_Sales_Core`:** Read, Create and Edit on Account and Contact, the Convert Leads and Edit Tasks permissions, and Delete removed from Opportunity (8:30–8:31 PM CT). Converting a lead creates an account, a contact and an opportunity, so a Sales Rep couldn't convert one without them.
- **Collections Team public group:** Collections Supervisor role and subordinates added (8:46 PM CT). Until then the group had no members, so neither sharing rule that shares with it reached anyone (DEF-10).

### DEF-08 — Collections personas couldn't see Log Contact Attempt · High · **Fixed 2026-10-24; confirmed in the console 2026-10-26**
**Found:** 2026-10-24, by Steward's Phase 5 hand check. Logged in as Test Persona (Collections Rep), Zana saw Steward's Briefing and Follow-up Draft on Sandra Barnett Household but not Log Contact Attempt, which sits between them in the layout's action list. It was the first time anyone had used the console as a collections persona since the action was built in Phase 8. The system test ran as the admin, who can run every flow, and UAT-06 was still on the persona-check list.

**Cause:** the action launches the screen flow `Account_Screen_LogContactAttempt`. A user can run a flow only with the Run Flows permission or with access to that flow, since Salesforce enforced its *Restrict User Access to Run Flows* release update. Minimum Access doesn't include Run Flows, no Accord permission set granted it, and the flow had no access list, so Lightning hid the action. Checked through the API: Run Flows false on the profile and on the Collections Rep group; the flow had no access entries.

**Effect:** no rep, specialist or supervisor could log a contact attempt, so US-06 and the promise path from a call (US-03) didn't work for the people they're for. Steward's Follow-up Draft waits for a logged attempt, so it was blocked too.

**Fix, least privilege:** the flow now restricts who can run it (version 3, *Override default behavior and restrict access to enabled profiles or permission sets*), and `PS_Collections_Core` grants access to that one flow. Run Flows wasn't granted: it opens every current and future flow to the holder, and this flow runs in system context with sharing, which Salesforce's own warning on save points out. Sales reps don't get the action, by design.

**Verified through the API (2026-10-24):** version 3 active with the restriction, version 2 obsolete, nothing else changed; flow access on `PS_Collections_Core` and, after recalculation, on the Collections Rep, Collections Supervisor and Dispute Specialist groups; none on Sales Rep. **In the console (2026-10-26):** confirmed by the rest of Steward's hand check. Logged in as Test Persona, a collections rep, Zana saw Log Contact Attempt and logged a Left Voicemail attempt on Sandra Barnett Household at 1:53 PM CT; the task is in the org, created by Test Persona.

### DEF-09 — The Minimum Access profile granted field access the design gives to permission sets · High · **Fixed 2026-10-25**
**Found:** 2026-10-24, while checking DEF-08's fix: the field permissions on Test Persona's profile, Minimum Access - Salesforce, were listed through the API.

**What was there:** the profile granted field-level security on **74 of Accord's custom fields, 58 of them Read/Edit**. Setup's new-field wizard makes a field visible to every profile unless the boxes are cleared, and Accord's fields were created in Setup. Accord's permission sets granted almost no field access of their own (`PS_Collections_Core` had 14 field permissions, mostly on activities), so nearly everything collections personas read reached them through the profile. D-07 says all access comes from permission sets; for objects that was true, for fields it wasn't.

**Effect, in order of risk**
- Reps could edit **Account Status**, the field the collections sharing rule reads (D-08). Sales reps could edit it too, through their Account access. Only automation and supervisors should set it.
- Reps and sales reps could edit **Broken Promises (90d)** and **Collection Hold Until**, which feed the priority score and the work list.
- Sales reps could read account balances, days past due and priority score. The security model's field table says those are hidden from sales.
- Sales reps could edit **Do Not Contact**, which the design gives them as read-only.

Payment Method and External Reference had been removed from the profile on Oct 14, so UAT-01's check held throughout.

**Fix (2026-10-25), in an order that never took away access a persona needed:**
1. **Granted through permission sets first.** `PS_Collections_Core`: 54 fields, read-only except Do Not Contact, Primary Contact, a promise's statement and a contact's role. `PS_Dispute_Management`: 14, the dispute fields and adjustment fields, with the posted date read-only. `PS_Sales_Core`: 29, commitments, opportunities and leads, with no balances, days past due or priority.
2. **A new supervisor-only permission set, `PS_Collections_Overrides`,** for the three account fields a supervisor still has to change by hand: Account Status (to release Hardship Review or close an account), Collection Hold Until and High Value. It's in the Collections Supervisor group. That group's source lives in Steward's repository, so its change is in Steward's pull request #13.
3. **Removed from the profile:** all 74 Accord field permissions. The eight Legacy Id fields now belong to no persona; they exist for data loads.

**Verified in the org (2026-10-25):**
- The profile holds no field permission on any Accord field; 109 permissions on standard objects remain, as Salesforce ships them.
- Each group's own field permissions on Accord's fields, counted against the plan, match exactly:

| Group | Accord fields readable | Of those, editable |
|---|---|---|
| Collections Rep | 56 | 4 |
| Dispute Specialist | 63 | 17 |
| Collections Supervisor | 63 | 20 |
| Sales Rep | 29 | 12 |

- Test Persona (Collections Rep), field by field through `UserFieldAccess`: every collections field on the account readable, with Account Status, Broken Promises (90d) and Collection Hold Until now read-only; Do Not Contact and Primary Contact editable; statement and commitment fields read-only; a promise's statement editable; adjustments and every Legacy Id unreadable; a case's description still unreadable, as designed.
- Steward's rep assistant reads many of these fields as the user. Test Persona still reads every field its templates read ([Steward's agent governance doc](https://github.com/zana-yocum/Lumenfield-steward/blob/main/docs/agent-governance.md)), and Steward's full test suite ran against the changed org in its pull request #13 validation (`0Afaj00000p4HeQCAU`): 159 of 159 tests passed.


### DEF-10 — Collections reps could read every customer account · High · **Fixed 2026-10-26**
**Found:** 2026-10-25, while checking the persona checks' expected results against the org before handing them over. UAT-05 step 4 expects a rep not to find an account in the *Current* bucket. `UserRecordAccess` said Test Persona (Collections Rep) could read Regina Mundy Household, which is Current and has no cases. Across all 100 accounts, Test Persona could read 100 and edit 34. The 34 are exactly the accounts in Delinquent, Hardship Review or Default Review.

**Cause:** `Closed_Won_to_Collections` shared every Closed Won opportunity, read-only, with the Collections Team group, so collections could see commitments, which are master-detail children of the deal. Salesforce gives anyone who can read an opportunity, case or contact read access to its account (implicit sharing), and no setting turns that off. Every account has a closed deal, so every member of Collections Team could read every account. `AccountShare` shows it: an `ImplicitParent` row for Collections Team on each account, created when the deals were loaded on Sep 30.

**History, from the Setup Audit Trail and the share tables**
- The audit trail shows Collections Team created on Sep 27 and one membership change since: the Collections Supervisor role and its subordinates added on Oct 14 at 8:46 PM CT, in the evening changes above. That's still its only member. Until then the group was empty, so neither rule that shares with it reached anyone: not the status rule (D-08), and not the closed-deal rule.
- So the Phase 7 check on Oct 9 didn't prove D-08. Test Persona could read ACC-0001 right after its status changed because billing dispute 00001038, loaded the evening before, is on that account. The case rule shares billing disputes with the Collections Rep role, and the dispute brings its account along. ACC-0002 had no dispute. Its closed deal would have given a rep read access too, if the group had had members, which fits the group being empty then.
- From Oct 14, 8:46 PM, the status rule gave reps edit on accounts in collections, and the closed-deal rule gave them read on all the rest. D-08's "a current account stays out of reach" was never true in the org.

**Effect:** any collections rep could open any customer's account, with its contacts (Contact is controlled by its parent), statements, balances and promises, whether or not the account was in collections. Field-level security still hid the payment method, and nobody could edit an account outside collections. Dispute specialists and supervisors are meant to read every customer, because a dispute can come from anyone, so for them nothing changes.

**Fix, in an order that never took away access a persona needed:**
1. **Done.** `Delinquent_Accounts_to_Collections` also grants read on the account's opportunities (Opportunity Access: Read Only). A rep sees the deal, and its commitments, on every account in collections, and loses them when the account leaves. Applied through the Metadata API at 8:45 PM CT; recalculation finished a few seconds later.
2. **Done.** New rule `Closed_Won_to_Dispute_Specialists`: closed deals, read-only, to the Dispute Specialist role. Supervisors get it through the role hierarchy. Specialists still need it for a dispute on an account that isn't in collections. Applied the same way at 8:46 PM CT.
3. **Done 2026-10-26.** `Closed_Won_to_Collections` deleted. The metadata API Claude uses can't delete a sharing rule, so Zana deleted it in Setup at 1:47 PM CT; recalculation finished seven seconds later.

**Verified after steps 1 and 2 (2026-10-25):** both rules read back from the org as written. `AccountShare` for Patrick Boone Household and Sandra Barnett Household shows Opportunity Access Read for Collections Team. `OpportunityShare` shows all 100 closed deals shared with the Dispute Specialist role. The org's 159 Apex tests, all Steward's, ran against the changed sharing: 159 passed (test run `05maj000001ZBRRAA4`).

**Verified after step 3 (2026-10-26), for Test Persona through `UserRecordAccess`:**

| What | Before (2026-10-25) | After (2026-10-26) |
|---|---|---|
| Accounts it can read | 100 | 40: the 34 in collections, and the 6 current accounts with a billing dispute |
| Accounts it can edit | 34 | 34, the accounts in collections |
| Regina Mundy Household (Current, no disputes), its contact and its deal | Readable | Not readable, nor its statements |
| Sandra Barnett Household (Delinquent): its contact, a statement and its deal | — | Readable; the contact editable |
| Commitments COM-00001 and COM-00002, on delinquent accounts | — | Readable |
| Commitments COM-00007 and COM-00004, on current accounts | — | Not readable |

The six read-only accounts are exactly the current accounts with a billing dispute: 00001030, 00001031, 00001037, 00001041, 00001049 and 00001053. In the share tables, Collections Team now holds 34 account shares, all from the status rule, and no implicit ones. Closed deals are shared only with the Dispute Specialist role: 100 of them. The old rule no longer exists in the org. The 159 Apex tests ran again after the deletion, and all 159 passed (test job `707aj00001O2HPx`).

**Accepted:** a billing dispute on a current account is visible to reps, and so is that account, read-only. Reps need to see disputes, and narrowing it would mean copying the account's status onto every case. Six accounts today.


### DEF-11 — A Sales Input team member can read a dispute but can't add a case comment · Medium · **Open: needs a decision**
**Found:** 2026-10-26, by the persona check for UAT-08 step 2a, which had been an open question since Phase 6 (US-08 says the sales rep can "read the case and add comments").

**What happens:** a case comment needs edit access to its case. Sales reps have Read on Case (`PS_Sales_Core`), so the Sales Input team role's Read/Write is capped at Read, and saving a comment is refused. The same is true for collections reps reading a dispute through the sharing rule. Posting to the case's feed only needs read access, and it saved.

**Effect:** the sales rep can see the dispute but can't put their account of the sale on it as a comment. Steward's dispute summary reads case comments, not feed posts, so feed posts wouldn't reach it either.

**Options**
1. **A Sales Input action (recommended):** a small screen flow on the Billing Dispute layout that saves the rep's text as a case comment, run in system mode with sharing and granted to the Sales Rep group only, the same pattern as Log Contact Attempt (DEF-08). Least privilege, and comments stay where the specialist and Steward's summary look.
2. **The case feed:** works today with read access, nothing to build. Steward's summary would need to read feed posts too, and the comment history is split across two places.
3. **Edit on Case for sales reps:** not recommended. Edit would let a sales rep change the dispute's status or close it.

Recorded in open items; the fix follows the decision.


### DEF-12 — Unpaid statements never became past due · High · **Fixed 2026-11-03; confirmed by the morning runs 2026-11-04**
**Found:** 2026-11-03, reconciling `data-model.md` with the org. The page said Billing Statement's `Status__c` is "stamped by a nightly flow," because the account roll-ups filter on it. No such flow existed. Two flows write a statement's status on specific events: `Adjustment_AfterSave_ApplyCredits` marks it Paid when posted credits clear it (DEF-01), and `Case_AfterSave_DisputeLifecycle` flags it In Dispute and restores it when the dispute closes. Nothing reacted to a due date passing, or to a payment clearing the balance.

**What happened:** a statement's status was whatever the data load gave it. The re-age on Oct 8 stamped each one correctly for that day, including the next month's bills as Open. When those due dates passed unpaid, nothing changed them. On Nov 3, 35 statements on 35 accounts were still Open past their due dates (Oct 10 to Oct 28), $6,235.80 unpaid.

**Effect:** Past Due Balance and Oldest Past Due Date only count statements marked Past Due, and Days Past Due, Account Status and the collections sharing rule all follow from them (D-06, D-08). For 12 of the 35 accounts the overdue bill was the only one, so they read 0 days past due and Current: off the work list and invisible to reps. For the other 23, already in collections, Past Due Balance was short by the open bill. A customer who stopped paying would never have reached collections, and one who paid a past-due bill in full would have stayed past due, because a payment didn't change the status either (no such payment exists in the data yet). It went unseen because every test started from loaded data, which was right on the day it was loaded; the account flow that was checked was working correctly on stale inputs.

**Fix:** `Billing_Statement_Daily_Status`, a scheduled flow on Open and Past Due statements, runs each morning at 4:30 AM Eastern, half an hour before `Account_Daily_Collections_Status`. Nothing owed → Paid; still owing after the due date → Past Due; otherwise unchanged. In Dispute and Written Off are left alone. The rule is the one the re-age generator and the dispute flow already use. Built through the Tooling API: version 1 was scheduled for one run at 9:20 AM ET on Nov 3 to produce evidence today, version 2 moved it to 4:30 AM.

**Verified (Nov 3, the 9:20 AM ET run):** the run started at 9:20:13 AM ET as the org's default workflow user (OrgFarm EPIC). It moved all 35 overdue Open statements to Past Due ($6,235.80) and left the 68 already past due alone; the field history shows 36 status changes, all at 9:20:14. Two throwaway statements on ACC-0053 tested the other branches: one marked Past Due but paid in full ($25 due, a $25 payment) became Paid, and one Open and due Nov 20 stayed Open. Both were deleted afterwards. The 12 Current accounts now read 7 to 24 days past due, each bill counted in Past Due Balance; the 5 AM account run on Nov 4 moves them to Delinquent, which puts them on the work list and in reps' reach. Version 2, at 4:30 AM, is active: `CronTrigger` shows it at 4:30, the account run at 5:00 and the promise runs at 5:30, all America/New_York.

**Confirmed by the morning runs (Nov 4, checked through the API at 5:30 AM ET):**
- **Statement run.** `Billing_Statement_Daily_Status` version 2 ran for the first time on schedule. `CronTrigger` shows it fired at 4:35:07 AM ET, five minutes after its 4:30 slot (a scheduled flow can start a few minutes late), and it's set for 4:30 AM on Nov 5. It had nothing to change: no statement was modified on Nov 4 and the status history shows no change. That's the expected answer, because the Nov 3 run had already moved the 35, and no other bill had come due unpaid overnight. The org has 0 Open statements past their due date with a balance, and 0 Past Due statements with nothing owed.
- **Account run.** `Account_Daily_Collections_Status` fired at 5:00:30 AM ET. All 12 accounts moved to Delinquent at 5:00:36 AM ET, saved by the org's default workflow user (OrgFarm EPIC), with Days Past Due and Past Due Balance filled:

| Account | Household | Days past due | Past due balance | Oldest past due |
|---|---|---|---|---|
| ACC-0004 | Vanessa Mercer | 25 | $167.34 | Oct 10 |
| ACC-0060 | Maria Boone | 23 | $199.99 | Oct 12 |
| ACC-0069 | Nicole Grissom | 21 | $164.90 | Oct 14 |
| ACC-0008 | William Radcliff | 20 | $120.27 | Oct 15 |
| ACC-0079 | William Bruner | 19 | $139.08 | Oct 16 |
| ACC-0018 | Douglas Coffey | 14 | $157.54 | Oct 21 |
| ACC-0017 | Michael Coffey | 12 | $187.36 | Oct 23 |
| ACC-0038 | Ryan Stiles | 12 | $127.31 | Oct 23 |
| ACC-0045 | Tanya Lattimore | 12 | $143.59 | Oct 23 |
| ACC-0072 | Tonya Bruner | 10 | $157.65 | Oct 25 |
| ACC-0080 | Jeffrey Naylor | 9 | $174.67 | Oct 26 |
| ACC-0081 | Stephanie Ballard | 8 | $183.74 | Oct 27 |

- **The rest of the chain.** No residential account reads Current with any days past due. The collections sharing rule (D-08) now gives Collections Team Edit on 46 accounts, up from 34 on Nov 3, and each of the 12 is among them, so they're in reps' reach. The households are 42 Current, 34 Delinquent and 12 Default Review.
- **One thing to know.** Tanya Lattimore is one of Steward's portal demo customers, shown in Phase 4 as current with a dispute. She now reads 12 days past due, because her October bill went unpaid in the aged data. The re-age before any recording resets her.

**Also found while checking this:** the scheduled flows don't run when the docs said. Their start times read `05:00:00.000Z` and `05:30:00.000Z` in the metadata, and the docs said 1 AM ET, but Salesforce reads the time in the org's time zone: `CronTrigger` shows 5:00 and 5:30 AM America/New_York, and every Default Review so far was created between 5:00 and 5:10 AM Eastern. Docs corrected; nothing depended on 1 AM.

---

## Still to run

| Script | Who / when | What to check |
|---|---|---|
| 06 steps 2–5 | You, as Test Persona (about 5 min, `docs/persona-checks.md`) | Promise Made, Requested No Further Contact and Hardship from the console, and the block with no outcome. Everything else that needed a persona login was checked through the API on Oct 26 (above) |
| 08 step 2a | After the DEF-11 decision | Sales input saved on the dispute by a Sales Rep |
| 14, email part | You, in the supervisor's inbox | "Dispute Milestone Violation" for 00001049 around Oct 15, 5 PM CT and Oct 19, 5 PM CT. Then delete 00001049 |
| 04 step 2, 15 step 4, 20 | When data allows | A promise kept on a scheduled run; a review cured by payment; the reminder 7 days before a first due date (the Oct 14 test contract was deleted before Oct 21, so its reminder never ran) |
| All | 3–5 outside testers | Actual UAT |
