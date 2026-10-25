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
| Step 4 (mismatch account hidden from a rep) | Needs persona login. Status correction itself was proven in Phase 7 |

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

---

## Still to run

| Script | Who / when | What to check |
|---|---|---|
| 01, 05 step 4, 06, 08, 12 negative, 13 criterion 3, 18 | You, as Test Persona (≈15 min) | What each persona can and can't see; case comment as a Sales Input team member |
| 14 | Thu Oct 15, business hours | Dispute **00001049** left untouched: warning email ≈ 3:30 PM ET, violation at 6:00 PM ET. Delete the case afterward |
| 15 | ≈ Oct 18–19 | Default Review opens on its own for the first account past 90 DPD |
| 04, 20 | After a promise's grace date / Oct 21 | Promise judged Kept/Broken on schedule; reminder fires 7 days before first due |
| All | 3–5 outside testers | Actual UAT |
