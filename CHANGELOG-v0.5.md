## v0.5 — 2026-10-08 — Phase 6: Service

Disputes and default reviews now run as governed cases: their own record types and status paths, queue routing, a business-hours SLA with alerts, and a console for the people who work them. The phase also surfaced and fixed a formula bug and a dataset that didn't match its own plan.

### Added
- **Account record types** Residential Agreement (88) and Organization (12), granted through `PS_Sales_Core` only, since record type assignment governs create and change, not view
- **Case record types** Billing Dispute and Default Review, each with a support process. Seven Case Status values: Acknowledged, Awaiting Evidence, Under Review, Pending Credit Approval, Resolved, Cured, Default Confirmed (deployed from source)
- **Page layouts** for all four record types. Residential accounts lead with a Collections section; Billing Dispute carries reason, statement, originating deal, entitlement and resolution; sample fields left off every layout
- **Queues** Dispute Specialists and Default Reviews, with roles as members rather than named users
- **Case assignment rule** `Accord Case Routing`; the assignment checkbox is defaulted on and hidden so it can't be bypassed
- **Case sharing rule** `Billing_Disputes_to_Collections`: Read Only on billing disputes to Collections Reps (US-01). Default reviews stay private
- **Entitlement process** `Billing Dispute SLA` on Lumenfield Support Hours: acknowledge in 1 business day, request evidence in 3, resolve in 10 (600 / 1800 / 6000 minutes). 88 entitlements, one per residential account
- **Milestone alerts (US-14)**: warning to the case owner at 75% of each milestone, violation to the owner and Collections Supervisors at the target
- **Dispute evidence requirements** for the remaining five reasons; all 8 reasons now have a checklist (16 records)
- **Outbound contact business hours**: Mon–Fri 8 AM–8 PM, Sat 9 AM–5 PM, Eastern; inside the FDCPA 8 AM–9 PM window
- **Collections Console** (Lightning console app) and object tabs for Billing Statement, Payment, Promise to Pay, Adjustment and Commitment, granted through permission sets with tab defaults
- **Test cases**: 13 billing disputes across every status and all 8 reasons, and 5 default reviews on the 90+ accounts
- `data/regen/generate_billing.py` and runbook: regenerates billing history anchored to a given date; rerun to re-age the book before UAT or a demo
- `requirements.md` rewritten with acceptance criteria for all 21 user stories

### Fixed
- **`Billing_Statement__c.Balance__c` was `Amount_Paid__c - Amount_Paid__c`** and always zero, so every account's Current Balance and Past Due Balance read $0. Corrected to `Amount_Due__c - Amount_Paid__c`; about $10,088 in balances appeared. The Phase 5 dashboard couldn't have caught it, since nothing measured balances
- **Delinquency distribution**: 29 accounts sat at 90+ days past due against a plan of 5, because each statement series ended months before the load. Billing data regenerated against today: Current 52 · 1–30 14 · 31–60 10 · 61–90 7 · 90+ 5
- `PS_Collections_Core` had no Read on Case, so the dispute sharing rule had nothing to open. Added Case Read and read on Dispute Reason and Root Cause
- Persona users landed in Salesforce Classic; Minimum Access lacks Lightning Experience User. Added to the three persona permission sets
- `Case.EntitlementId` was hidden from System Administrator, so cases couldn't be linked to an SLA
- Developer Edition leftovers removed: nine sample roles (three sat under Dispute Specialist, giving upward visibility into sales records), the Standard Case entitlement process and its milestones, Developer Edition sample campaigns, solutions, products and price book
- `PS_Payment_Detail` label double space

### Verified
- SLA counts business hours only: a case opened Wednesday evening targeted Thursday 6 PM, Monday 6 PM (weekend skipped) and ten business days out (US-09)
- Collections Rep reads billing disputes, can't edit them, can't see default reviews
- Sales rep not on a case team can't open a dispute, including one about their own deal; added to the team, they can read it and nothing more (US-08, US-18)

### Lessons recorded
- An entitlement process locks once any case has used it, even a deleted one. Milestone actions were added in Setup instead. In production, enable entitlement versioning before go-live
- Some standard fields are required on every layout (Account: Parent Account; Case: Contact, Origin, Web fields)
- Static seed data with TODAY() formulas drifts a day every day; a re-age routine is part of the dataset, not an afterthought

### Known, deliberately deferred to Phase 7
- New disputes don't yet stamp their entitlement, complete milestones on status change, flag the disputed statement, or remove case team members at close
- Default reviews are opened by hand; the flow that opens them on the threshold crossing (and sets the owner, since Flow can't run assignment rules) comes next
