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

## Next

**v0.2 — Requirements (Phase 2):** user stories with acceptance criteria, current-state and future-state process maps.
