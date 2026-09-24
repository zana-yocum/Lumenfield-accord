# Accord — Project Brief

**Company:** Lumenfield Home Energy (fictional)
**Build:** Salesforce Developer Edition, synthetic data
**Owner:** Zana Yocum, Salesforce Administrator
**Dates:** started 2026-09-24, roughly a three-week build

---

## 1. Problem

Sales reps promise things at closing: a promotional credit, a delayed billing start, the first couple of payments covered. When none of it gets recorded in Salesforce, the customer's first past-due notice turns into a dispute. The collections rep can't confirm what was promised, the customer feels lied to, and the balance keeps aging while both sides hunt for proof.

Seeded baseline: **[__]%** of open disputes trace back to a commitment that was never recorded, and disputes take an average of **[__] days** to close. Both numbers are measured from the seeded dataset after the data load in Phase 5.

All data in this org is synthetic. No real customer information is used.

---

## 2. Who it's for

- **Collections rep.** Works past-due accounts. Needs the account's full history on one screen, and logs promises to pay.
- **Dispute specialist.** Owns billing disputes. Gathers evidence from the customer and the sales rep, and works to an SLA.
- **Collections supervisor.** Watches queue health and SLA compliance, and approves credits above the threshold.
- **Sales rep.** Closes leases, records any concession made at signing, and answers when a dispute names them.

---

## 3. In scope

- Lead through Closed Won, including concession capture at signing
- Service contract creation at close, with commitments carried forward
- Billing statements, payments, and promises to pay
- Disputes as cases, with queues, assignment and escalation rules, and entitlement SLAs
- Onboarding touches and payment reminders, gated on recorded consent
- Default reviews and tiered credit approvals, with thresholds in custom metadata
- Security model: org-wide defaults, role hierarchy, permission set groups, sharing rules, field-level security
- Reports and dashboards for each persona

---

## 4. Out of scope, deliberately

- **Live payment processing.** Payments are recorded, not taken. Processor integration is the next project.
- **Customer self-service portal.** Next project.
- **E-signature.** Next project.
- **SMS and omni-channel.** Email and tasks only. SMS is noted as a production dependency.
- **CPQ-style product configuration, multi-currency, multi-region.** Not needed by a single-market residential servicer.

---

## 5. Success metrics

Targets are set now so the build can be measured against something it's capable of failing. Baselines are filled in after the Phase 5 data load.

| Metric | Baseline | Target | Source |
|---|---|---|---|
| Disputes with a commitment on file before the dispute opened | TBD | 90% | Cases with Commitments custom report type |
| Dispute cycle time, opened to resolved | TBD | 7 days or less | Case age report by record type |
| Dispute SLA compliance | No SLA exists today | 90% of milestones met | Case entitlement milestone report |
| First-payment default rate, accounts activated in the last 60 days | TBD | Under 5% | Billing statement report by activation date |
| Default reviews opened inside the policy window | TBD | 95% within 3 business days of threshold | Default review case report |
| Promise-to-pay kept rate | TBD | 80% | Promise to Pay report |
| Duplicate contact rate | TBD | Under 2% | Data quality dashboard |
| Required-field completeness on active agreements | TBD | 98% | Data quality dashboard |

---

## 6. Constraints and assumptions

- **Platform.** Developer Edition: 5 MB of data storage, so the dataset is budgeted at roughly 2,000 records. Few full user licenses, and no sandboxes. Personas are tested by swapping permission set groups on a single test user.
- **Data.** All synthetic, and seeded with deliberate defects — duplicates, missing fields, inconsistent picklist values — so the data quality work has something real to measure and improve.
- **Channels.** Email and tasks only. Consent is recorded on the standard consent objects and checked before any automated outreach.
- **Configuration standard.** Policy thresholds — days past due, approval tiers, reminder offsets — live in custom metadata rather than hardcoded in flows.
- **Time.** Business hours and holidays drive every SLA clock, so they're configured before any automation is built.
- **Delivery.** Built solo, evenings and weekends, over roughly three weeks.

---

## 7. How it gets verified

- UAT scripts per persona, run by testers outside the build, with defects logged and written sign-off before release.
- Security Health Check score recorded before and after the security model is applied.
- Data quality measured before and after the cleanup rules go in.
- Every phase ends with a commit, so the build history matches the documentation.
