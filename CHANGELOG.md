# Release notes — Accord

Versions run v0.x through the build and hit v1.0 at UAT sign-off. One entry per phase, written the day the phase closes.

---

## v0.1 — Org baseline · 2026-09-24

**Org setup**
- Developer Edition org created and named Lumenfield Home Energy
- Company information set: Eastern time zone, US locale, USD, fiscal year starting January
- Business hours configured Monday–Friday, 8:00 AM–6:00 PM Eastern, set as default
- US holidays created as recurring and associated with the business hours record, so escalation rules and entitlement milestones suspend when the office is closed
- Email deliverability set to All email, so flow email alerts can actually send
- Administrator account secured with phishing-resistant MFA

**Documentation**
- Project brief: problem, personas, scope, success metrics, constraints
- D-01: customer data model — Account + Contact over Person Accounts
- D-02: concession capture point — at signing, on the Opportunity
- Conventions and configuration standards

**Notes**
- Sample data shipped with the Developer Edition org is still present and gets removed in Phase 5 before the Lumenfield dataset loads.
- Data storage at baseline: 7% of the 5 MB cap.

---

## v0.2a — Requirements · 2026-09-24

- 21 user stories with Given/When/Then acceptance criteria across four personas plus automation-served customers
- Policy values table, traceability matrix, and object list feeding Phase 3
- D-03, D-04, D-05 recorded

---

## v0.2 — Data model · 2026-09-26

**Foundations**
- Four global value sets: Contact Outcome, Dispute Reason, Root Cause, Commitment Type
- Two custom metadata types with 16 records — nine policy thresholds and seven dispute evidence requirements
- Data Protection and Privacy enabled, exposing the Individual and consent objects

**Custom objects**
- Commitment, master-detail to Opportunity
- Billing Statement, master-detail to Account with a Service Contract lookup
- Payment, master-detail to Billing Statement
- Promise to Pay, master-detail to Account
- Adjustment, master-detail to Account
- Field history tracking on the fields that carry money or status

**Standard objects**
- Fields added to Account, Opportunity, Service Contract, Case, Contact, and Lead
- Roll-up summaries on Account and Opportunity
- Formulas for aging, bucketing, priority scoring, and policy compliance

**Decisions**
- D-03: disputes are Cases with a record type rather than a custom object
- D-04: declarative only, no custom Lightning components in this build
- D-05: consent gates promotional messages, not servicing messages
- D-06: billing statements are master-detail to Account rather than Service Contract, so balance and aging roll up to where reps work. Forces statement status to be a stamped picklist rather than a formula.

**Notes**
- Test records used to verify the formula chain were deleted before close.
- Object and field definitions retrieved to `force-app` and committed.

---

## Next

**v0.3 — Security model (Phase 4):** personas, permission set groups, org-wide defaults, role hierarchy, sharing rules, and the case team design behind temporary sales rep access.
