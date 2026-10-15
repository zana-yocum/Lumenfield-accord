# Case Study — Accord

**A promise made at signing shouldn't surprise collections six months later.**

Accord is a Salesforce build for Lumenfield Home Energy, a fictional residential solar lease servicer. It covers lead to cash across Sales and Service Cloud, with one idea running through it: every concession a sales rep offers becomes a governed record that follows the customer into billing, disputes and collections.

Declarative only. No Apex, no custom Lightning components. 21 user stories, 20 delivered, 1 cut on purpose.

---

## The problem

In residential solar, the sale and the bill are months apart and handled by different teams. A rep tells a customer their first two payments are covered. Nobody writes it down where billing can see it. Six months later the customer is "past due," disputes the bill, and the collections rep calling them has no idea a promise was ever made.

That one gap produces most of what goes wrong downstream:

- **Disputes** that shouldn't exist, and that take weeks because nobody can find the evidence
- **Collections calls** made blind — no history of promises, no view of open disputes
- **Credits** approved one at a time, with no one seeing that it's the fourth this year
- **Defaults** decided late, or not at all, because no one is told an account crossed the line

## Approach

Ten phases, each closed with a changelog and an open-items review before the next one started.

| Phase | Delivered |
|---|---|
| 1–2 | Brief, 21 user stories with Given/When/Then criteria, each with a negative case |
| 3 | Data model: 5 custom objects, roll-ups, policy limits and evidence checklists in custom metadata |
| 4 | Security: Minimum Access + permission set groups, criteria-based sharing. Health Check 66% → 96% |
| 5 | About 1,650 synthetic records loaded with seeded defects, measured, cleaned, measured again |
| 6 | Disputes as Cases: record types, queues, 3-milestone entitlement process, console app |
| 7 | 10 flows, credit approval, 5 validation rules |
| 8 | Web-to-lead, duplicate alerting, structured contact attempts |
| 9 | 8 reports, supervisor dashboard, console home page |
| 10 | UAT scripts, root cause analysis, training reference, this document |

## Five decisions that shaped it

**Concessions are captured on the Opportunity, and closing is blocked without one (D-02, US-02).** A validation rule fires only on the move to Closed Won, only when Concession Offered is Yes. The honest path — no concession — is never slowed down. A rule that stops the honest path is worse than no rule.

**Disputes are Cases, not a custom object (D-03).** That choice bought entitlements, milestones, queues, assignment rules, case teams and the console for free. The dispute SLA — acknowledge in 1 business day, evidence in 3, resolve in 10 — runs on business hours and skips weekends without a line of code.

**Collections reaches accounts through a sharing rule on Account Status, not ownership (D-08).** It means status is a security control. The Phase 5 baseline found three accounts that were 45 days past due but still marked Current. That isn't a data hygiene issue — those accounts were invisible to the reps who should have been calling them. The nightly status flow fixed them, and the test proved it: the first account processed became visible to a rep immediately; the second stayed hidden until its turn.

**Minimum Access plus permission set groups, no custom profiles (D-07).** Four personas, each a group of small permission sets. It held with one documented exception: a profile is the only place a default record type can live, and lead conversion needs one.

**Consent gates promotional messages, not servicing ones (D-05).** A customer who never opted into marketing still gets their welcome email and payment reminder. Blocking those would stop people hearing about their own bills. Do Not Contact stops everything.

## What went wrong, and what it taught

**Every balance in the org was $0.** A formula subtracted a field from itself. It was valid syntax, passed every check, and made every collections number wrong. It was found by looking at one unpaid statement and asking whether $0 made sense. The data quality dashboard couldn't have caught it, because nothing on it measured balances. Full write-up: [`rca-balance-formula.md`](rca-balance-formula.md).

**Static data ages.** Days past due counts from today, so a seed file that was right in September had 29 of 30 delinquent accounts past 90 days by October. The fix was a generator that re-ages billing data to any anchor date, now part of the runbook before every demo or UAT session.

**The platform has edges, and they're worth writing down.** An entitlement process locks the moment any case uses it. Approval field updates skip validation rules — which turned out to be useful: it makes the approval process the *only* way a large credit can be approved. Flows can't run assignment rules, scheduled paths can't read custom metadata, and approval criteria can't either. Each is recorded in a changelog with what was done about it.

**Verification beats memory.** Connecting to the org and checking found three cleanup items marked done that weren't, a permission set that gave reps Case sharing but no Case read (so sharing did nothing), and a role hierarchy where sample roles sat under Dispute Specialist and would have handed specialists upward visibility into sales records.

## Results

| Measure | Before | After |
|---|---|---|
| Duplicate contact pairs | 7 | 0 |
| Accounts invisible to collections | 3 | 0, kept at 0 nightly |
| Residential accounts with no one to contact | 88 | 0, enforced by rule |
| Statement date errors | 2 | 0, enforced by rule |
| Security Health Check | 66% | 96% |
| Stories delivered | — | 20 of 21 (US-17 cut) |

The supervisor dashboard on release day showed 35 accounts to work, $10,619 past due, 10 open disputes and 69% milestone compliance over 30 days. The 31% that missed were test disputes nobody worked between loads — which is exactly what that tile exists to make visible.

## What I'd do with more time

- **Payment allocation.** A payment covering two statements can't be split. Production needs a junction object.
- **Customer time zones.** The outbound contact window uses one time zone, so it can't protect a customer three zones west from an early call.
- **Entitlement versioning** turned on before go-live, so the SLA process can change after cases use it.
- **Outside UAT.** The scripts are written; the next step is three to five testers who didn't build it.

## Where to look

| | |
|---|---|
| Requirements and traceability | [`requirements.md`](requirements.md) |
| Every decision and why | [`decision-log.md`](decision-log.md) |
| Security model | [`security-model.md`](security-model.md) |
| Data plan and load history | [`data-plan.md`](data-plan.md) |
| UAT scripts | [`uat-scripts.md`](uat-scripts.md) |
| What's built, phase by phase | `CHANGELOG.md` |
