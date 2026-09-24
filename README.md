# Accord — Collections & Concessions on Salesforce

> Every promise made at the sale follows the customer from first click to final payment.

A self-directed Salesforce build for **Lumenfield Home Energy**, a fictional residential solar servicer. Built solo in a Developer Edition org with synthetic data, September–October 2026. This is not a production system and isn't presented as one.

**Zana Yocum** · Salesforce Administrator
[Trailhead profile](TODO) · [LinkedIn](TODO) · [Portfolio](TODO)

---

## The problem

Sales reps promise things at closing: a promotional credit, a delayed billing start, the first couple of payments covered. When none of it gets recorded in Salesforce, the customer's first past-due notice turns into a dispute. The collections rep can't confirm what was promised, the customer feels lied to, and the balance ages while both sides hunt for proof.

In the seeded dataset, **[__]%** of open disputes trace back to a commitment nobody wrote down.

---

## What I built

| Area | What's in it |
|---|---|
| **Sales** | Web-to-Lead capture, assignment rules, Flow-based lead scoring, campaigns with influence, conversion mapping, Products and Price Books, Quotes, forecasts with quotas |
| **Concessions** | Commitment object in master-detail to Opportunity, roll-up summary, validation rule blocking Closed Won when a concession isn't recorded, auto-created Service Contract at close |
| **Service** | Dispute cases with their own record type and support process, queues, assignment and escalation rules, entitlement process with milestones on real business hours |
| **Collections** | Billing statements, payments, promises to pay with automatic kept/broken evaluation, consent-gated onboarding touches, nightly default reviews, tiered credit approvals |
| **Security** | Four personas on permission set groups over a minimum-access profile, private org-wide defaults, role hierarchy, sharing rules, field-level security on payment data, expiring case-team access |
| **Data** | ~2,000 synthetic records seeded with deliberate defects, duplicate and matching rules, validation rules, data quality dashboard |
| **Analytics** | Custom report types and dashboards per persona: funnel, SLA compliance, DPD aging, promise-kept rate, data health |

---

## Results

Measured in the seeded dataset. Baselines captured before the build, after-numbers on release.

| Metric | Baseline | After | Target |
|---|---|---|---|
| Disputes with a commitment on file before the dispute opened | TBD | TBD | 90% |
| Dispute cycle time | TBD | TBD | ≤ 7 days |
| Dispute SLA compliance | No SLA existed | TBD | 90% |
| First-payment default rate (last 60 days) | TBD | TBD | < 5% |
| Default reviews opened in policy window | TBD | TBD | 95% |
| Promise-to-pay kept rate | TBD | TBD | 80% |
| Duplicate contact rate | TBD | TBD | < 2% |
| Security Health Check score | TBD | TBD | — |

---

## Walkthrough

**[3-minute narrated tour of the org](TODO)** — the fastest way to see it.

---

## How it's put together

- [Project brief](docs/brief.md) — problem, personas, scope, metrics, constraints
- [Decision log](docs/decision-log.md) — every design decision, the options rejected, and when to revisit
- [Requirements](docs/requirements.md) — user stories with acceptance criteria
- [Data model](docs/data-model.md) — ERD and object-by-object rationale
- [Data dictionary](docs/data-dictionary.md) — every custom field, its purpose, and its source
- [Security model](docs/security-model.md) — personas, access matrix, sharing design
- [Automation inventory](docs/automation-inventory.md) — every flow, its trigger, its order, its fault path
- [UAT results](docs/uat-results.md) — test scripts, defects found, sign-off
- [Release notes](CHANGELOG.md) — what shipped, when
- [Conventions](docs/conventions.md) — naming and configuration standards

---

## Deploy it yourself

```bash
git clone TODO
sf org login web -a lumenfield
sf project deploy start -o lumenfield
sf data import tree -p data/plan.json -o lumenfield
```

Everything here is synthetic. No real customer data exists in this repo.

---

## Limits, and what I'd do differently in production

<!-- Written at release. Be specific and honest — this section is read closely. -->

- Built in Developer Edition: 5 MB of data storage, so volumes are small and nothing was tested at production scale.
- Outreach is email and tasks only. SMS would require a messaging channel and consent handling beyond what's modeled here.
- TODO
- TODO

---

**Environment:** Salesforce Developer Edition · API version TODO · built September–October 2026
