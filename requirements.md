# Requirements — Accord

User stories by persona, each with acceptance criteria in Given / When / Then form.

Every story has an ID. That ID gets referenced in the flow description that implements it, the UAT script that tests it, and the commit that ships it. When a reviewer asks "how do you know this requirement was met," the chain is right there.

**Priority:** Must / Should / Could. Anything marked Could is a candidate to cut if the three weeks tighten — and cutting it deliberately is worth more than shipping everything half-built.

---

## Worked examples

Two are written out as the model. The rest are yours.

### US-01 — One screen for a past-due account
**Persona:** Collections rep
**Priority:** Must · **Phases:** 3, 8

**As a** collections rep, **I want** the whole picture of a past-due account on one screen, **so that** I can make the call without opening six tabs and still sound informed.

**Acceptance criteria**
- **Given** an account with at least one unpaid statement past its due date, **when** I open the account record, **then** I see current balance, days past due, the primary contact, open promises to pay, open disputes, and any commitments recorded at signing, without navigating away.
- **Given** an account with no past-due balance, **when** I open it, **then** the collections panel shows a current status rather than empty space.
- **Given** I don't have access to payment detail fields, **when** I open any account, **then** those fields are hidden rather than shown blank.

**Notes:** Third criterion is deliberate — it's the field-level security behavior from Phase 4, tested here rather than assumed.

---

### US-02 — A concession can't go unrecorded
**Persona:** Sales rep
**Priority:** Must · **Phases:** 3, 7

**As a** sales rep, **I want** a fast way to record what I promised at signing, **so that** collections isn't blindsided later and I'm not the one explaining it six months on.

**Acceptance criteria**
- **Given** an opportunity where I've marked that a concession was offered, **when** I try to move it to Closed Won with no Commitment record attached, **then** it's blocked with a message naming exactly what to add.
- **Given** an opportunity with at least one Commitment record, **when** I move it to Closed Won, **then** it saves and a Service Contract is created with the commitments related to it.
- **Given** no concession was offered, **when** I move the opportunity to Closed Won, **then** nothing blocks me.

**Notes:** The third criterion is the one people forget. A rule that stops the honest path is worse than no rule.

---

## Backlog to write

Write acceptance criteria for each. Aim for two to four per story, and include at least one negative or edge case — the case where the user *shouldn't* be allowed to do something, or where data is missing.

### Collections rep
- US-03 — Log a promise to pay within policy limits
- US-04 — See which promises were kept or broken, and when
- US-05 — Work a prioritized list of accounts rather than searching
- US-06 — Record the outcome of a contact attempt in a structured way

### Dispute specialist
- US-07 — Open a dispute through guided intake with the right evidence checklist
- US-08 — Request the sales rep's side of the story, with access that ends when the case closes
- US-09 — See the SLA clock and what's due next
- US-10 — Resolve a dispute and record the root cause
- US-11 — Request a credit above my approval limit

### Collections supervisor
- US-12 — See queue health and SLA compliance without building a report
- US-13 — Approve or reject credit requests with the account context attached
- US-14 — Get alerted when a dispute breaches its milestone
- US-15 — See which accounts crossed the default threshold and whether reviews opened in time

### Sales rep
- US-16 — Capture lead information from the website without rekeying
- US-17 — See my pipeline and forecast against quota
- US-18 — Respond to a dispute that names one of my deals

### New customer (indirect — served by automation, not a user)
- US-19 — Receive a welcome touch after activation with payment setup information
- US-20 — Receive a reminder before the first payment is due
- US-21 — Receive no automated contact when consent hasn't been recorded

---

## Traceability

Fill in as the build progresses. This table is what turns a pile of config into a delivered project.

| Story | Built in | Implemented by | Tested by |
|---|---|---|---|
| US-01 | Phase 3, 8 | Account Lightning page, related lists | UAT-01 |
| US-02 | Phase 3, 7 | `VR_Opportunity_ConcessionRequiresCommitment`, `Opportunity_AfterSave_CreateServiceContract` | UAT-02 |
| US-03 | | | |
