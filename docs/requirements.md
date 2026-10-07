# Requirements — Accord

User stories by persona, each with acceptance criteria in Given / When / Then form.

Every story has an ID. That ID is referenced in the configuration that implements it, the UAT script that tests it, and the commit that ships it. When a reviewer asks "how do you know this requirement was met," the chain is right there.

**Priority:** Must / Should / Could. Could items are candidates to cut if time tightens. Cutting one deliberately is worth more than shipping everything half-built.

**Every story includes at least one negative or edge case:** the user who *shouldn't* be allowed to do something, or the record where data is missing. A rule that only gets tested on the happy path hasn't been tested.

---

## Summary

| ID | Story | Persona | Priority | Phases |
|---|---|---|---|---|
| US-01 | One screen for a past-due account | Collections rep | Must | 3, 8 |
| US-02 | A concession can't go unrecorded | Sales rep | Must | 3, 7 |
| US-03 | Log a promise to pay within policy limits | Collections rep | Must | 3, 5, 7 |
| US-04 | See which promises were kept or broken, and when | Collections rep | Must | 3, 5, 7 |
| US-05 | Work a prioritized list instead of searching | Collections rep | Must | 3, 7, 9 |
| US-06 | Record a contact attempt in a structured way | Collections rep | Should | 3, 7 |
| US-07 | Open a dispute through guided intake | Dispute specialist | Must | 6, 7 |
| US-08 | Request the sales rep's side, with access that ends at close | Dispute specialist | Should | 4, 6 |
| US-09 | See the SLA clock and what's due next | Dispute specialist | Must | 6 |
| US-10 | Resolve a dispute and record the root cause | Dispute specialist | Must | 6, 7 |
| US-11 | Request a credit above my approval limit | Dispute specialist | Must | 5, 7 |
| US-12 | See queue health without building a report | Collections supervisor | Should | 9 |
| US-13 | Approve or reject credits with account context | Collections supervisor | Must | 7 |
| US-14 | Get alerted when a dispute breaches a milestone | Collections supervisor | Should | 6 |
| US-15 | See default threshold crossings and review timeliness | Collections supervisor | Must | 6, 7, 9 |
| US-16 | Capture website leads without rekeying | Sales rep | Should | 8 |
| US-17 | See pipeline and forecast against quota | Sales rep | Could | 8 |
| US-18 | Respond to a dispute that names my deal | Sales rep | Should | 4, 6 |
| US-19 | Welcome touch after activation | New customer | Should | 7 |
| US-20 | Reminder before the first payment | New customer | Should | 7 |
| US-21 | No promotional contact without consent | New customer | Must | 3, 7 |

---

## Collections rep

### US-01 — One screen for a past-due account
**Priority:** Must · **Phases:** 3, 8

**As a** collections rep, **I want** the whole picture of a past-due account on one screen, **so that** I can make the call without opening six tabs and still sound informed.

**Acceptance criteria**
- **Given** an account with at least one unpaid statement past its due date, **when** I open the account record, **then** I see current balance, days past due, the primary contact, open promises to pay, open disputes, and any commitments recorded at signing, without navigating away.
- **Given** an account with no past-due balance, **when** I open it, **then** the collections panel shows a current status rather than empty space.
- **Given** I don't have access to payment detail fields, **when** I open any account, **then** those fields are hidden rather than shown blank.

**Notes:** The third criterion is the field-level security from Phase 4, tested here rather than assumed.

---

### US-02 — A concession can't go unrecorded
**Persona:** Sales rep · **Priority:** Must · **Phases:** 3, 7

**As a** sales rep, **I want** a fast way to record what I promised at signing, **so that** collections isn't blindsided later and I'm not the one explaining it six months on.

**Acceptance criteria**
- **Given** an opportunity where I've marked that a concession was offered, **when** I try to move it to Closed Won with no Commitment record attached, **then** it's blocked with a message naming exactly what to add.
- **Given** an opportunity with at least one Commitment record, **when** I move it to Closed Won, **then** it saves and a Service Contract is created with the commitments related to it.
- **Given** no concession was offered, **when** I move the opportunity to Closed Won, **then** nothing blocks me.

**Notes:** The third criterion is the one people forget. A rule that stops the honest path is worse than no rule.

---

### US-03 — Log a promise to pay within policy limits
**Priority:** Must · **Phases:** 3, 5, 7

**As a** collections rep, **I want** to log a customer's promise to pay quickly, with policy checked for me, **so that** I don't have to remember the limits on every call, and a promise I'm not allowed to grant doesn't quietly become a hold.

**Acceptance criteria**
- **Given** an account with a past-due balance, **when** I log a promise with an amount and a date inside the limits in `Policy_Setting__mdt`, **then** it saves as Active and the account's Collection Hold Until date is set to the promise's grace end.
- **Given** a promise whose date is further out than policy allows, **when** I save it, **then** it saves as Pending Approval and is flagged Out of Policy. It does not place the account on hold until a supervisor approves it.
- **Given** a promise amount of zero or less, **when** I save it, **then** it's blocked with a message telling me to enter an amount greater than zero.
- **Given** an account already holding an Active promise, **when** I try to log a second one, **then** I'm told to update or close the existing promise first.

**Notes:** The third criterion is `VR_Promise_AmountPositive`, already built in Phase 5. A zero-dollar promise would put an account on hold with nothing committed.

---

### US-04 — See which promises were kept or broken, and when
**Priority:** Must · **Phases:** 3, 5, 7

**As a** collections rep, **I want** each promise's outcome recorded automatically from actual payments, **so that** I'm not judging it from memory and the customer's track record is there before I dial.

**Acceptance criteria**
- **Given** an Active promise, **when** payments received by the grace end date total at least the promised amount, **then** the promise moves to Kept and Amount Received shows the total.
- **Given** an Active promise, **when** the grace end date passes with less than the promised amount received, **then** the promise moves to Broken, the hold is released, and the account's Broken Promises (90 days) count goes up by one.
- **Given** a payment dated in the future, **when** someone tries to save it, **then** it's blocked, so a promise can't be marked Kept for money not yet received.
- **Given** an account, **when** I open it, **then** I can see every promise from the last 90 days with its outcome and outcome date, newest first.

**Notes:** The third criterion is `VR_Payment_DateNotFuture` from Phase 5. Partial payments count toward the total; there's no allocation across statements (see the payment allocation limit in the README).

---

### US-05 — Work a prioritized list instead of searching
**Priority:** Must · **Phases:** 3, 7, 9

**As a** collections rep, **I want** my accounts ranked by who most needs a call today, **so that** I start the day working instead of deciding what to work.

**Acceptance criteria**
- **Given** past-due accounts shared with me, **when** I open my work list, **then** they're sorted by Priority Score, highest first, with days past due, past-due balance, and broken promises in the last 90 days visible on each row.
- **Given** an account marked Do Not Contact, **when** the list loads, **then** it doesn't appear.
- **Given** an account with an Active promise whose hold hasn't expired, **when** the list loads, **then** it doesn't appear until the hold ends.
- **Given** an account that is past due but still marked Current, **when** the status-stamping flow runs, **then** its status corrects and it appears on the list for the reps who should be working it.

**Notes:** The fourth criterion is the status mismatch defect from the Phase 5 baseline. Because the sharing rule depends on Account Status (D-08), a stale status hides an account from collections entirely.

---

### US-06 — Record a contact attempt in a structured way
**Priority:** Should · **Phases:** 3, 7

**As a** collections rep, **I want** to log each call or message with a picked outcome, **so that** the next rep knows what happened without reading my notes, and outcomes can be reported on.

**Acceptance criteria**
- **Given** an account I'm working, **when** I log a contact attempt, **then** I choose an outcome from the Contact Outcome value set, and the attempt is saved to the account's activity history with my name and the time.
- **Given** the outcome "Promise to Pay," **when** I save the attempt, **then** I'm taken straight into logging the promise (US-03) rather than doing it as a separate step.
- **Given** no outcome selected, **when** I try to save, **then** it's blocked with a message asking me to pick one.

---

## Dispute specialist

### US-07 — Open a dispute through guided intake
**Priority:** Must · **Phases:** 6, 7

**As a** dispute specialist, **I want** a guided intake that shows the evidence required for the dispute reason, **so that** cases don't stall waiting on documents nobody asked for up front.

**Acceptance criteria**
- **Given** a customer disputing a statement, **when** I open a Billing Dispute case and choose a dispute reason, **then** I see the evidence checklist for that reason from `Dispute_Evidence_Requirement__mdt`.
- **Given** a dispute is opened against a statement, **when** the case saves, **then** the statement is flagged Dispute Open and its balance is excluded from collections priority until the case closes.
- **Given** a dispute reason with no evidence requirements configured, **when** I select it, **then** I see a message saying none are defined and can still proceed, rather than a blank checklist.
- **Given** no related statement, **when** I try to save a Billing Dispute case, **then** it's blocked. A dispute has to name what's being disputed.

**Notes:** Disputes are Cases with a record type, not a custom object (D-03). Seven evidence requirement records exist for the top three reasons; the rest are on the Phase 6 open items.

---

### US-08 — Request the sales rep's side, with access that ends at close
**Priority:** Should · **Phases:** 4, 6

**As a** dispute specialist, **I want** to bring the original sales rep onto a dispute case, **so that** I get their account of what was promised without giving them standing access to collections data.

**Acceptance criteria**
- **Given** a dispute about a commitment made at signing, **when** I add the sales rep to the case team, **then** they can read the case and add comments.
- **Given** the sales rep is on the case team, **when** the case closes, **then** their access to the case is removed.
- **Given** a sales rep who isn't on the case team, **when** they try to open the dispute case, **then** they can't see it.

**Notes:** The third criterion is the negative test deferred from Phase 4 for lack of cases.

---

### US-09 — See the SLA clock and what's due next
**Priority:** Must · **Phases:** 6

**As a** dispute specialist, **I want** to see each milestone's deadline and how much time is left, **so that** I work the case closest to breaching rather than the one that came in first.

**Acceptance criteria**
- **Given** a new Billing Dispute case, **when** it saves, **then** the entitlement process starts three milestones: acknowledge within 1 business day, evidence within 3, resolve within 10.
- **Given** an open case, **when** I open it, **then** I see the next milestone, its target time, and time remaining.
- **Given** a case moved to Acknowledged, Awaiting Evidence, or Resolved, **when** it saves, **then** the matching milestone completes.
- **Given** a case opened late on a Friday, **when** the targets calculate, **then** they count business hours only, not the weekend.

---

### US-10 — Resolve a dispute and record the root cause
**Priority:** Must · **Phases:** 6, 7

**As a** dispute specialist, **I want** to record why a dispute happened when I resolve it, **so that** the pattern behind disputes can be fixed rather than worked one case at a time.

**Acceptance criteria**
- **Given** a dispute case, **when** I set the status to Resolved, **then** a root cause from the Root Cause value set is required before it saves.
- **Given** the root cause is an undocumented concession, **when** the case resolves, **then** it can be reported by the sales rep who made the original deal.
- **Given** a dispute that was withdrawn or a duplicate, **when** I close it as Closed rather than Resolved, **then** no root cause is required and it's excluded from root cause reporting.

**Notes:** The second criterion is what makes US-10 matter. The seeded data concentrates undocumented concessions on one rep, so the report shows a pattern rather than noise.

---

### US-11 — Request a credit above my approval limit
**Priority:** Must · **Phases:** 5, 7

**As a** dispute specialist, **I want** to submit a credit over my limit for approval, **so that** I can resolve the case properly without needing someone else to enter it.

**Acceptance criteria**
- **Given** a credit adjustment within my limit, **when** I submit it, **then** it posts without approval.
- **Given** a credit adjustment above my limit, **when** I submit it, **then** it goes to a supervisor for approval, the case moves to Pending Credit Approval, and the adjustment can't post until it's approved.
- **Given** a supervisor rejects the adjustment, **when** they save the rejection, **then** a rejection reason is required.
- **Given** an adjustment that's been approved, **when** anyone tries to change its amount, **then** it's blocked.

**Notes:** The third criterion is `VR_Adjustment_RejectionReason` from Phase 5. It exists because native approval comments can't be made mandatory.

---

## Collections supervisor

### US-12 — See queue health without building a report
**Priority:** Should · **Phases:** 9

**As a** collections supervisor, **I want** a dashboard showing open cases, SLA compliance, and aging, **so that** I can see where the team is falling behind before a customer tells me.

**Acceptance criteria**
- **Given** open dispute cases, **when** I open the supervisor dashboard, **then** I see open cases by status, milestone compliance for the last 30 days, and cases closest to breaching.
- **Given** past-due accounts, **when** I open the dashboard, **then** I see balances by days-past-due bucket and promise kept rate.
- **Given** a user without supervisor access, **when** they open the dashboard, **then** they see only the records their own sharing allows.

**Notes:** The third criterion tests that the dashboard's running user is set deliberately, not left as the admin.

---

### US-13 — Approve or reject credits with account context
**Priority:** Must · **Phases:** 7

**As a** collections supervisor, **I want** the account's history in front of me when I approve a credit, **so that** I'm not approving the fourth credit this year without knowing about the other three.

**Acceptance criteria**
- **Given** a credit waiting for my approval, **when** I open the approval request, **then** I see the amount, the dispute reason, the account's balance, and prior adjustments in the last 12 months.
- **Given** I approve the credit, **when** the approval completes, **then** the adjustment posts and the case moves back to Under Review.
- **Given** I'm the specialist who submitted the credit, **when** I try to approve it, **then** I can't. Approval goes to someone else.

---

### US-14 — Get alerted when a dispute breaches a milestone
**Priority:** Should · **Phases:** 6

**As a** collections supervisor, **I want** to be told before and when a milestone is missed, **so that** I can step in while it's still fixable.

**Acceptance criteria**
- **Given** an open milestone, **when** 75% of its time has passed, **then** the case owner gets a warning.
- **Given** a milestone passes its target without completing, **when** the violation fires, **then** I get notified and the case is flagged as breached.
- **Given** a case that completed its milestone on time, **when** the target time passes, **then** no alert is sent.

---

### US-15 — See default threshold crossings and review timeliness
**Priority:** Must · **Phases:** 6, 7, 9

**As a** collections supervisor, **I want** to know which accounts crossed the default threshold and whether each got a review in time, **so that** no account defaults without a decision.

**Acceptance criteria**
- **Given** an account reaching 90 or more days past due, **when** its status updates, **then** Threshold Crossed Date is stamped and a Default Review case opens automatically.
- **Given** a Default Review case, **when** three calendar days pass without it moving to Under Review, **then** it's flagged as late.
- **Given** an account that already has an open Default Review case, **when** it's re-evaluated, **then** no second case opens.
- **Given** an account that drops back below 90 days past due before the review completes, **when** the review is worked, **then** it can close as Cured.

**Notes:** Three calendar days, not business days, is a deliberate simplification (see "Deliberately not doing" in `open-items.md`).

---

## Sales rep

### US-16 — Capture website leads without rekeying
**Priority:** Should · **Phases:** 8

**As a** sales rep, **I want** website inquiries to arrive as leads automatically, **so that** I'm calling the customer instead of copying their form into Salesforce.

**Acceptance criteria**
- **Given** a prospect submits the website inquiry form, **when** it's received, **then** a lead is created with name, contact details, service address, and inquiry detail, and is assigned to a sales rep.
- **Given** an inquiry from someone whose email matches an existing contact, **when** the lead is created, **then** the duplicate is flagged rather than silently creating a second person.
- **Given** a form submitted without an email or phone number, **when** it's received, **then** no lead is created, because there would be no way to follow up.

---

### US-17 — See pipeline and forecast against quota
**Priority:** Could · **Phases:** 8

**As a** sales rep, **I want** my pipeline and forecast against quota in one view, **so that** I know where I stand for the month without exporting to a spreadsheet.

**Acceptance criteria**
- **Given** open opportunities I own, **when** I open forecasts, **then** I see commit, best case, and pipeline totals against my quota for the period.
- **Given** an opportunity with a concession and an attached commitment, **when** it's in my pipeline, **then** its commitment value is visible alongside the deal amount.
- **Given** another rep's opportunities, **when** I view forecasts, **then** I don't see their numbers unless I'm above them in the role hierarchy.

---

### US-18 — Respond to a dispute that names my deal
**Priority:** Should · **Phases:** 4, 6

**As a** sales rep, **I want** to be asked directly when a dispute is about something I sold, **so that** my side is on record and the dispute isn't decided without it.

**Acceptance criteria**
- **Given** I'm added to a dispute case team, **when** it happens, **then** I'm notified with a link to the case.
- **Given** I'm on the case team, **when** I open the case, **then** I can see the dispute and the commitments from my opportunity, but not the account's payment detail.
- **Given** the case has closed, **when** I try to open it, **then** I no longer have access.

**Notes:** US-08 from the sales rep's side. The second criterion confirms field-level security still applies inside a case team.

---

## New customer

Indirect stories: these are served by automation, not by a user doing something.

### US-19 — Welcome touch after activation
**Priority:** Should · **Phases:** 7

**As a** new customer, **I want** a welcome message when my system is activated, with how to set up payment, **so that** my first bill isn't a surprise.

**Acceptance criteria**
- **Given** a service contract reaching activation, **when** the activation date is set, **then** a welcome email goes to the account's primary contact and Welcome Sent On is stamped.
- **Given** the primary contact's email is missing or malformed, **when** the welcome would send, **then** nothing sends, and a task is created for follow-up instead of the failure going unnoticed.
- **Given** a welcome has already been sent, **when** the contract is edited again, **then** no second welcome goes out.
- **Given** an account with no primary contact, **when** the contract activates, **then** a follow-up task is created rather than the flow failing.

**Notes:** The second and fourth criteria are why the Phase 5 data includes malformed emails and accounts with no primary contact.

---

### US-20 — Reminder before the first payment
**Priority:** Should · **Phases:** 7

**As a** new customer, **I want** a reminder a few days before my first payment is due, **so that** a missed first payment isn't how I find out billing started.

**Acceptance criteria**
- **Given** a service contract with a first due date, **when** the configured number of days before it arrives, **then** a reminder goes to the primary contact.
- **Given** the first statement is already paid, **when** the reminder date arrives, **then** no reminder is sent.
- **Given** the first due date changes, **when** it's updated, **then** the reminder reschedules to the new date.

**Notes:** First-payment misses are the 1–30 days-past-due population in the dataset. This story is aimed at preventing them.

---

### US-21 — No promotional contact without consent
**Priority:** Must · **Phases:** 3, 7

**As a** new customer, **I want** to receive promotional messages only if I agreed to them, **so that** I'm not marketed to without permission, while still getting the messages about my account that I need.

**Acceptance criteria**
- **Given** a contact with no consent recorded, **when** any automated promotional message would send, **then** it doesn't send.
- **Given** a contact with no promotional consent, **when** a servicing message is due (welcome, payment reminder, statement), **then** it still sends.
- **Given** an account marked Do Not Contact, **when** any automated message would send, servicing or promotional, **then** nothing sends.

**Notes:** Consent gates promotional messages, not servicing ones (D-05). The second criterion is the important one. Blocking servicing messages would stop customers from hearing about their own bills.

---

## Traceability

Filled in as the build progresses. This table turns a pile of config into a delivered project.

| Story | Built in | Implemented by | Tested by |
|---|---|---|---|
| US-01 | Phase 3, 8 | Account Lightning page, related lists | UAT-01 |
| US-02 | Phase 3, 7 | `VR_Opportunity_ConcessionRequiresCommitment`, `Opportunity_AfterSave_CreateServiceContract` | UAT-02 |
| US-03 | Phase 3, 5, 7 | `Promise_to_Pay__c`, `Policy_Setting__mdt`, `VR_Promise_AmountPositive` · promise policy flow (Phase 7) | UAT-03 |
| US-04 | Phase 3, 5, 7 | `Broken_Promises_90d__c`, `VR_Payment_AmountPositive`, `VR_Payment_DateNotFuture` · promise evaluation flow (Phase 7) | UAT-04 |
| US-05 | Phase 3, 7, 9 | `Priority_Score__c`, sharing rule (D-08) · status-stamping flow (Phase 7) | UAT-05 |
| US-06 | Phase 3, 7 | Contact Outcome value set · contact attempt action (Phase 7) | UAT-06 |
| US-07 | Phase 6, 7 | Billing Dispute record type, `Dispute_Evidence_Requirement__mdt` | UAT-07 |
| US-08 | Phase 4, 6 | Case team roles | UAT-08 |
| US-09 | Phase 6 | Entitlement process, Billing Dispute support process | UAT-09 |
| US-10 | Phase 6, 7 | Root Cause value set | UAT-10 |
| US-11 | Phase 5, 7 | `Adjustment__c`, `VR_Adjustment_RejectionReason` · approval process (Phase 7) | UAT-11 |
| US-12 | Phase 9 | | UAT-12 |
| US-13 | Phase 7 | | UAT-13 |
| US-14 | Phase 6 | | UAT-14 |
| US-15 | Phase 6, 7, 9 | Default Review record type, `Threshold_Crossed_Date__c` | UAT-15 |
| US-16 | Phase 8 | | UAT-16 |
| US-17 | Phase 8 | | UAT-17 |
| US-18 | Phase 4, 6 | Case team roles | UAT-18 |
| US-19 | Phase 7 | `Welcome_Sent_On__c` | UAT-19 |
| US-20 | Phase 7 | `First_Due_Date__c` | UAT-20 |
| US-21 | Phase 3, 7 | `Do_Not_Contact__c`, consent model (D-05) | UAT-21 |
