# UAT Scripts — Accord

One script per user story. Each script names the persona to log in as, the record to start from, the steps, and what must be true for a pass. Every script includes the negative case from its story's acceptance criteria.

## How to run these

- **Org:** Lumenfield Developer Edition. Log in as **Test Persona** and switch the user's role and permission set group to the persona named in the script. Developer Edition has two full licenses, so one persona user stands in for each role in turn.
- **Data:** Before a UAT session, re-age the billing data with `data/regen/generate_billing.py` (see `RUNBOOK.md`). Days Past Due counts from today, so last week's data is already a week older.
- **Recording:** Mark each step Pass or Fail. On a fail, write what happened in the Notes column and log it in `open-items.md` with the script ID.
- **Clean up:** Delete test records you create, then empty the Recycle Bin.

| Field | Value |
|---|---|
| Tester | |
| Date | |
| Data re-aged on | |

---

## Collections rep

### UAT-01 — One screen for a past-due account (US-01)
**Persona:** Collections Rep · **Start:** any account on the Collections Work List

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Open Collections Console → Accounts → pick a Delinquent account | Opens as a workspace tab | | |
| 2 | Read the Collections section | Current balance, days past due, DPD bucket, priority score, broken promises, primary contact all visible | | |
| 3 | Check related lists | Promises to Pay, Billing Statements, Cases (disputes), Commitments shown without leaving the page | | |
| 4 | Open a Current account | Collections fields show $0 / 0 days / Current, not blanks | | |
| 5 | **Negative:** look for payment method and external reference on a Payment | Hidden for the rep (no Payment Detail permission set), not shown empty | | |

### UAT-02 — A concession can't go unrecorded (US-02)
**Persona:** Sales Rep · **Start:** an open opportunity

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Set Concession Offered = Yes, save | Saves | | |
| 2 | Move to Closed Won with no Commitment | Blocked; message says to add a Commitment | | |
| 3 | Add a Commitment (Payment Coverage, $500), then Closed Won | Saves; a Service Contract is created; the Commitment links to it | | |
| 4 | **Negative:** a second opportunity with Concession Offered = No → Closed Won | Saves with nothing blocking | | |

### UAT-03 — Log a promise to pay within policy (US-03)
**Persona:** Collections Rep · **Start:** a Delinquent account with no active promise

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | New Promise to Pay, amount ≥ minimum, date within policy | Saves as Active; account's Collection Hold Until = grace end | | |
| 2 | Log a second promise on the same account | Blocked: update or close the existing promise first | | |
| 3 | On another account, promise dated beyond the policy window | Saves as Pending Approval, Out of Policy checked, **no** hold set | | |
| 4 | **Negative:** amount 0 | Blocked: enter an amount greater than zero | | |

### UAT-04 — Kept or broken, and when (US-04)
**Persona:** Collections Rep · **Start:** the promise from UAT-03 step 1

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Record a payment on the promise's statement for the full amount, dated today | Saves | | |
| 2 | After the next 1:30 AM ET run (or a debug run of `Promise_Daily_Evaluate` once grace has passed) | Promise = Kept, Amount Received = payment total | | |
| 3 | A promise past grace with less received | Broken; hold released; account Broken Promises (90d) up by 1 | | |
| 4 | **Negative:** payment dated tomorrow | Blocked: payment date can't be in the future | | |
| 5 | Account → Promises related list | Last 90 days of promises with outcomes, newest first | | |

### UAT-05 — Prioritized work list (US-05)
**Persona:** Collections Rep · **Start:** Reports → Collections → Collections Work List

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Run the report | Sorted by Priority Score, highest first; DPD, past-due balance, broken promises on each row | | |
| 2 | Set Do Not Contact on one listed account, rerun | Account gone from the list | | |
| 3 | Give a listed account an Active in-policy promise, rerun | Gone until the hold date passes | | |
| 4 | **Negative:** an account past due but marked Current | Not visible to the rep. After the daily status flow runs, status = Delinquent and it appears | | |

### UAT-06 — Structured contact attempt (US-06)
**Persona:** Collections Rep · **Start:** a Delinquent account

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Click **Log Contact Attempt**, choose No Answer, save | Completed task in Activity History with outcome, rep name and time | | |
| 2 | Log again with Promise Made | Flow moves straight to the promise screen; promise saves and policy applies | | |
| 3 | Log with Requested No Further Contact | Account Do Not Contact = true | | |
| 4 | Log with Hardship or Bankruptcy | Account Status = Hardship Review; daily status flow leaves it alone | | |
| 5 | **Negative:** click Next with no outcome | Blocked; asked to pick one | | |

---

## Dispute specialist

### UAT-07 — Guided dispute intake (US-07)
**Persona:** Dispute Specialist · **Start:** a statement with a balance

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | New Case → Billing Dispute, choose a reason, link the statement | Evidence checklist for that reason shown | | |
| 2 | Save | Statement shows Dispute Open and In Dispute; case routed to Dispute Specialists | | |
| 3 | Close the case | Statement restored to Paid / Past Due / Open from its real balance | | |
| 4 | **Negative:** save a Billing Dispute with no statement | Blocked; a dispute must name what's disputed | | |

### UAT-08 — Sales rep's side, access ends at close (US-08)
**Persona:** Dispute Specialist, then Sales Rep · **Start:** an open dispute

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Add the deal's sales rep to the case team as Sales Input | Saves | | |
| 2 | As Sales Rep, open the case | Can read it | | |
| 2a | As Sales Rep, add a case comment with your account of the sale | Comment saves. If refused, log it — US-08 says "read and add comments" and Read-only team access may not allow it | | |
| 3 | Close the case; as Sales Rep, reopen the link | No access | | |
| 4 | **Negative:** a sales rep not on the team opens any dispute | No access | | |

### UAT-09 — SLA clock (US-09)
**Persona:** Dispute Specialist · **Start:** a new Billing Dispute

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Save the case | Entitlement attached; three milestones: 1, 3 and 10 business days | | |
| 2 | Open the Milestones component | Next milestone, target and time remaining shown | | |
| 3 | Status → Acknowledged, then Awaiting Evidence, then Resolved | Matching milestone completes at each step | | |
| 4 | **Edge:** a case opened Friday evening | Targets skip the weekend | | |

### UAT-10 — Root cause on resolve (US-10)
**Persona:** Dispute Specialist

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Set a dispute to Resolved with no root cause | Blocked: choose a root cause | | |
| 2 | Choose Concession Not Recorded at Signing, save | Saves | | |
| 3 | Run Resolved Disputes by Root Cause | Case counted under that root cause | | |
| 4 | **Negative:** close a withdrawn dispute as Closed | No root cause required; not on the root cause report | | |

### UAT-11 — Credit above my limit (US-11)
**Persona:** Dispute Specialist

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Adjustment, Billing Correction, $75, linked to a dispute and its statement | Posts with no approval; **statement balance drops by $75** (DEF-01, fixed 2026-10-14) | | |
| 2 | Adjustment, Billing Correction, $250 → Submit for Approval | Pending; dispute moves to Pending Credit Approval | | |
| 3 | Try to set the $250 adjustment to Approved by hand | Blocked: must go through approval | | |
| 4 | Supervisor rejects with no reason | Approver gets a high-priority task to record the reason | | |
| 5 | **Negative:** change the amount on an approved adjustment | Blocked | | |

---

## Collections supervisor

### UAT-12 — Queue health without building a report (US-12)
**Persona:** Collections Supervisor · **Start:** Collections Console home

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Open the console | Home shows the Collections Supervisor dashboard and the Default Reviews queue | | |
| 2 | Read the dashboard | Open disputes by status, 30-day milestone compliance, balance by DPD bucket, promise outcomes | | |
| 3 | Open Open Milestones Closest to Breach | Nearest target first | | |
| 4 | **Negative:** as Collections Rep, open the Default Review Timeliness report | Rep sees no default review cases — reviews are private to the queue and supervisors | | |

### UAT-13 — Approve credits with context (US-13)
**Persona:** Collections Supervisor

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Open the pending $250 approval | Amount, type, dispute and account visible; prior adjustments on the account's related list | | |
| 2 | Approve | Adjustment posts; dispute back to Under Review | | |
| 3 | **Negative:** as the submitting Dispute Specialist, try to approve | Not an approver; can't approve | | |

### UAT-14 — Milestone alerts (US-14)
**Persona:** Collections Supervisor · **Prerequisite:** Deliverability = All email

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Leave a new dispute unacknowledged past 75% of 1 business day | Case owner gets the warning email | | |
| 2 | Leave it past the target | Owner and supervisor get the violation email; Milestone Status = Open Violation | | |
| 3 | **Negative:** acknowledge a second dispute before target | No alert | | |

### UAT-15 — Default threshold and review timeliness (US-15)
**Persona:** Collections Supervisor · **Start:** an account at 85–89 DPD

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | After the account crosses 90 DPD and the 1 AM ET run | Status = Default Review; Threshold Crossed Date stamped; Default Review case owned by Default Reviews queue | | |
| 2 | Run Default Review Timeliness | New case counted as opened on time | | |
| 3 | **Negative:** run the status flow again on the same account | No second case | | |
| 4 | Payment brings it under 90; close the review as Cured | Saves | | |

---

## Sales rep

### UAT-16 — Website leads without rekeying (US-16)
**Persona:** anonymous (web form), then Sales Rep · **Start:** `web/lumenfield-solar-inquiry.html`

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Submit with name, email, phone, service address, area, detail | Lead created with every field; owned by Inbound Leads | | |
| 2 | Submit using an existing customer's email | Lead created and flagged as a duplicate of the contact | | |
| 3 | **Negative:** submit with no email and no phone | No lead created | | |

### UAT-17 — Pipeline and forecast (US-17) — **cut**
Not built. US-17 was the only Could story and was cut deliberately in Phase 8. Record as N/A.

### UAT-18 — Respond to a dispute naming my deal (US-18)
**Persona:** Sales Rep

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Specialist adds you to a case team | You can open the case | | |
| 2 | On the case, look for payment detail fields | Not visible; field-level security still applies inside the case team | | |
| 3 | **Negative:** after the case closes | No access | | |

---

## New customer (automation)

### UAT-19 — Welcome after activation (US-19)
**Persona:** System Administrator · **Start:** a new service contract on an account with a primary contact

| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Set Activation Date and status Active | Welcome email sent; Welcome Sent On stamped | | |
| 2 | Edit the contract again | No second welcome | | |
| 3 | **Negative:** primary contact has no email | No email; follow-up task created | | |

### UAT-20 — Reminder before first payment (US-20)
| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Activate a contract with First Due Date 10 days out | Reminder scheduled for 7 days before (Setup → Scheduled Jobs / Paused and Waiting Interviews) | | |
| 2 | Change First Due Date | Reminder reschedules | | |
| 3 | **Negative:** first statement paid before the reminder date | No reminder sent | | |

### UAT-21 — No promotional contact without consent (US-21)
| # | Step | Expected | Pass/Fail | Notes |
|---|---|---|---|---|
| 1 | Activate a contract for a contact with no promotional consent | Welcome (servicing) still sends | | |
| 2 | Activate one on a Do Not Contact account | Nothing sends; Welcome Sent On stays blank | | |
| 3 | Search automation for promotional sends | None exist (D-05) | | |

---

## Sign-off

| Tester | Role played | Scripts run | Passed | Failed | Signature / date |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |
