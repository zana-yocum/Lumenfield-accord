# Accord — Lead to Cash for a Residential Solar Servicer

A Salesforce Administrator portfolio project. Accord is built for **Lumenfield Home Energy**, a fictional company that leases solar systems to homeowners and services the leases for 20 years. It runs from website inquiry to closed deal, activation, billing, disputes and collections, on Sales Cloud and Service Cloud.

**The idea:** every concession a sales rep offers at signing becomes a governed record that follows the customer into collections. When a customer says "I was told my first two payments were covered," the collections rep can see whether that's true.

Declarative only — flows, validation rules, approvals, sharing, entitlements and reports. No Apex, no custom Lightning components (D-04).

**Start here:** [Case study](docs/case-study.md) · [Requirements](docs/requirements.md) · [UAT scripts](docs/uat-scripts.md)

---

## Results

| Measure | Before | After |
|---|---|---|
| User stories delivered | 21 written | 20 delivered, 1 cut on purpose (US-17) |
| Duplicate contact pairs | 7 | 0 |
| Accounts hidden from collections by a stale status | 3 | 0, corrected nightly |
| Residential accounts with no one to contact | 88 | 0, enforced by validation rule |
| Statement date errors | 2 | 0, enforced by validation rule |
| Security Health Check | 66% (Poor) | 96% (Excellent) |

## What's in the org

| Area | Built |
|---|---|
| Data model | Commitment, Billing Statement, Payment, Promise to Pay, Adjustment; Policy Setting and Dispute Evidence Requirement custom metadata |
| Security | Minimum Access profile + 4 permission set groups (Collections Rep, Collections Supervisor, Dispute Specialist, Sales Rep); criteria-based sharing on Account Status; case teams for sales input |
| Service | Billing Dispute and Default Review case record types, two queues, assignment rules, a 3-milestone entitlement process on business hours, warning and breach alerts, Collections Console app |
| Automation | 12 flows (record-triggered, scheduled and one screen flow), credit approval process, 12 validation rules |
| Sales | Web-to-lead form, lead routing to a queue, duplicate alert against existing customers, concession-to-commitment enforcement at Closed Won |
| Analytics | 8 collections reports, Collections Supervisor dashboard, Data Quality dashboard, console home page |

Personas, stories and the components that implement each one: [`docs/requirements.md`](docs/requirements.md#traceability).

## How to explore it

1. Read the [case study](docs/case-study.md) — ten minutes, the whole project.
2. Pick a story in [`requirements.md`](docs/requirements.md) and follow its traceability row to the flow or rule in `force-app/`.
3. Read a changelog entry to see how a phase actually went, including what broke: `CHANGELOG.md`.
4. Read the [root cause analysis](docs/rca-balance-formula.md) for the defect that made every balance $0.

Field and rule descriptions reference user stories (`US-xx`) and decisions (`D-xx`). Both are in `/docs`, so any component can be traced back to why it exists.

## Repository

```
force-app/            Metadata retrieved from the org (source format)
manifest/             Retrieve manifests and destructive-change packages
data/                 Seed CSVs, load runbook, billing re-age generator (data/regen)
web/                  Web-to-lead inquiry form
docs/
  brief.md            The business problem
  requirements.md     21 user stories, acceptance criteria, traceability
  decision-log.md     D-01 to D-10
  conventions.md      Naming and configuration standards
  data-model.md       ERD and relationship rationale
  data-dictionary.md  Every field
  security-model.md   Personas, sharing, field-level security
  data-plan.md        Dataset, load failures, data quality before and after
  release-readiness-winter27.md
  uat-scripts.md      One script per story
  rca-balance-formula.md
  quick-reference.md  One page per role
  case-study.md
  open-items.md       Everything deferred, flagged, or deliberately not done
CHANGELOG.md
```

## Known limits

Written down so they're read as decisions, not oversights.

- **Static data drifts.** Days Past Due counts from `TODAY()`, so the dataset ages every day and accounts slide into 90+. Run `data/regen/generate_billing.py` before any demo or UAT session (see `data/regen/RUNBOOK.md`).
- **One time zone for outbound contact.** The contact-window business hours are Eastern. A customer in another time zone isn't protected from an early call. Production would check the customer's local time.
- **Credits don't carry forward.** A posted credit reduces its own statement's balance down to $0; any excess isn't applied to the next statement. Deleting a posted credit doesn't recalculate the statement (no persona can delete one).
- **No payment allocation.** A payment that covers two statements can't be split between them. Promise evaluation counts payments on the promise's related statement only. Production would add a junction object.
- **Default review window is calendar days.** Three calendar days, not business days — business-day math in a formula needs Apex or a workaround.
- **Fixed values duplicated from policy settings.** Approval entry criteria and scheduled-path offsets can't read custom metadata, so the $100 credit limit and 7-day reminder offset are duplicated from `Policy_Setting__mdt`.
- **Two-license persona testing.** Developer Edition has two full licenses, so one test user is switched between roles. In this org the admin is also the supervisor and can approve their own submissions; in production the admin wouldn't approve credits.
- **Entitlement process can't be edited once used.** Versioning should be enabled before go-live.
- **New households need an entitlement.** The 88 seeded accounts each have one. A new Residential Agreement account doesn't get one automatically, so its first dispute has no SLA clock until an entitlement is added. Production would create it on activation.
- **Evidence checklist matches by text.** `Dispute_Evidence_Requirement__mdt` stores the dispute reason as text, because custom metadata picklists can't use a global value set. Renaming a Dispute Reason value means updating the matching records by hand.
- **Volume.** About 1,650 records, using 3 of the org's 5 MB. Sharing recalculation, roll-ups and report performance behave differently at production scale.

## Built with

Salesforce Developer Edition (Winter '27, API 68.0) · Salesforce CLI · Data Loader · Python (data generation) · GitHub

All data is invented. No real customer information appears anywhere in this repository or the org.
