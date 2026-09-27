# Security Model — Accord

Who can see what, why, and how it was verified.

The guiding rule is least privilege: nobody gets access because it's convenient, and every grant traces to something a persona actually has to do in a user story.

---

## Personas

| Persona | What they do | The access question |
|---|---|---|
| **Collections rep** | Works past-due accounts, logs contact attempts and promises | Needs full context on delinquent accounts they don't own |
| **Dispute specialist** | Owns billing disputes end to end, gathers evidence, proposes credits | Needs cases, adjustments, and the commitments behind the sale |
| **Collections supervisor** | Watches queue health, approves credits, handles escalations | Needs everything the team sees, plus approval authority |
| **Sales rep** | Sells leases, records concessions at signing | Owns the account and opportunity, but has no business in payment data |

---

## Profiles and permission sets

Everyone sits on **Minimum Access - Salesforce**. No custom profiles exist in this org.

Access comes from function-based permission sets, assembled into persona-based groups:

| Permission set | Grants |
|---|---|
| `PS_Collections_Core` | Account and Contact read/edit · Billing Statement, Payment, Service Contract, Commitment read · Promise to Pay full · Task full |
| `PS_Dispute_Management` | Case create/read/edit · Adjustment create/read/edit · Entitlement read |
| `PS_Credit_Approval` | Adjustment edit including status · approval authority |
| `PS_Collections_Reporting` | Create and customize reports, manage dashboards, manage public list views |
| `PS_Payment_Detail` | Field-level read on payment method and processor reference fields |
| `PS_Sales_Core` | Lead, Opportunity, Product, Price Book, Quote full · Commitment full · Account and Contact read/edit · Service Contract read |

| Permission set group | Contains | Muted |
|---|---|---|
| `PSG_Collections_Rep` | `PS_Collections_Core` | Delete on Promise to Pay |
| `PSG_Dispute_Specialist` | `PS_Collections_Core` + `PS_Dispute_Management` | Delete on Promise to Pay |
| `PSG_Collections_Supervisor` | `PS_Collections_Core` + `PS_Dispute_Management` + `PS_Credit_Approval` + `PS_Collections_Reporting` + `PS_Payment_Detail` | — |
| `PSG_Sales_Rep` | `PS_Sales_Core` | — |

**The muting set is the interesting part.** `PS_Collections_Core` grants delete on Promise to Pay because supervisors need it — a promise logged against the wrong account has to go. Reps shouldn't have it, since a deleted promise erases evidence of what a customer committed to. Rather than splitting the permission set in two, the rep and specialist groups mute that one permission. One source of truth, adjusted per persona.

---

## Org-wide defaults

| Object | Default | Why |
|---|---|---|
| Account | Private | Financial and delinquency data. Access is granted deliberately, not inherited from everyone. |
| Contact | Controlled by Parent | A contact is only as visible as the account it belongs to. |
| Opportunity | Private | Sales data, with collections granted narrow read through a sharing rule. |
| Case | Private | Disputes name individual reps and carry payment detail. Private is what makes the expiring case team access in US-08 meaningful — without it, everyone sees every dispute anyway. |
| Service Contract | Private | Agreement terms. |
| Lead | Private | Owned by the assigned rep. |
| Individual | Platform default | Consent records are read by automation in system context; no user-facing sharing needed. |

**The five custom objects have no org-wide default setting at all.** Every one is a master-detail child, so their access is controlled by the parent — see a statement only if you can see its account, see a commitment only if you can see its opportunity. That inheritance is a direct consequence of the relationship choices in D-02 and D-06, and it's the reason this security model only has to secure Account, Case, and Opportunity.

---

## Role hierarchy

```
Executive
├── VP Customer Operations
│   └── Collections Supervisor
│       ├── Collections Rep
│       └── Dispute Specialist
└── VP Sales
    └── Sales Manager
        └── Sales Rep
```

The hierarchy does one job here: supervisors see their team's records without a sharing rule. Everything else is granted explicitly.

---

## Sharing rules

The hard problem in this org: **sales owns the account, but collections has to work it.** A rep chasing a past-due balance doesn't own the record, isn't above the owner in the hierarchy, and can't be handed ownership without breaking the sales relationship.

| Rule | Shares | With | Access | Why |
|---|---|---|---|---|
| Delinquent Accounts to Collections | Accounts where Account Status is Delinquent, Hardship Review, or Default Review | Public group Collections Team | Read/Write | Collections works accounts it doesn't own, and only once they're delinquent. A current account stays out of reach. |
| Closed Won Opportunities to Collections | Opportunities where Stage equals Closed Won | Public group Collections Team | Read Only | Commitments are master-detail children of Opportunity, so without this a dispute specialist literally cannot see what was promised at signing. |
| Billing Disputes to Collections Team | Cases with the Billing Dispute record type | Public group Collections Team | Read Only | Reps need to know a dispute is open before calling. Editing stays with the specialist who owns it. |

**Public groups:** `Collections_Team` (reps, specialists, supervisors) and `Sales_Team`.

That second rule is worth pausing on. Master-detail inheritance means a relationship decision made in Phase 3 created a security requirement in Phase 4. If commitments had been a lookup instead, they'd need their own sharing — and the validation rule in US-02 wouldn't work. The trade-off runs in both directions.

---

## Field-level security

Record access and field access are separate layers, and both have to be right.

| Field | Collections | Dispute | Supervisor | Sales |
|---|---|---|---|---|
| Account: Current Balance, Past Due Balance, Days Past Due, DPD Bucket | Read | Read | Read | **Hidden** |
| Account: Broken Promises 90d, Priority Score | Read | Read | Read | **Hidden** |
| Account: Do Not Contact | Edit | Edit | Edit | Read |
| Account: Collection Hold Until | Read | Read | Edit | **Hidden** |
| Payment: Method, External Reference | **Hidden** | **Hidden** | Read | No object access |
| Adjustment: all fields | No access | Edit | Edit | No access |
| Commitment: all fields | Read | Read | Read | Edit |

Sales reps keep the account but lose the money. They have no operational need for a customer's balance or payment history, and every additional person who can see payment data is additional exposure if an account is ever compromised.

This is also what makes the second acceptance criterion in US-08 true: a sales rep added to a dispute case team gets record access to that case, but field-level security still hides payment detail on it. Record access opens the door; FLS decides what's visible once inside.

---

## Case teams — access that expires

US-08 needs a sales rep to answer questions on a dispute naming their deal, then lose that access when the case closes.

**Case team role:** `Sales Input` — Read/Write on the case, visible in the case team related list.

- When a specialist requests sales input, a flow adds the account owner to the case team in that role and creates a task.
- When the case reaches Resolved or Closed, a flow removes them.
- Access exists only while the case is open, and it's visible to anyone looking at the case rather than buried in a sharing rule.

**What was rejected and why:**
- *Sharing sets* only apply to Experience Cloud external users. Not applicable to internal reps.
- *Criteria-based sharing rules* can't be revoked per record — a rule broad enough to grant access would grant it to every matching case, permanently.
- *Manual sharing* would work but relies on someone remembering to remove it, which is how orgs accumulate access nobody can explain.

---

## Org-level security

| Setting | Value | Why |
|---|---|---|
| MFA | Required, all users | Salesforce requirement as of June 2026 |
| Admin MFA | Phishing-resistant (passkey or security key) | Required for System Administrator access |
| Session timeout | 2 hours, force logout on timeout | Collections workstations sit unattended |
| Login IP ranges | Not restricted | Documented deliberately: a remote workforce makes IP ranges impractical. Compensating control is MFA plus session timeout. |
| Password policy | 90-day expiry, 8 character minimum, 3 passwords remembered | |
| Health Check | Baseline captured before, again after | Score and remediated items recorded in the case study |

Naming the control you *didn't* implement, and what covers for it, is worth more than a clean list. Every real org has these.

---

## How it was tested

Developer Edition provides very few full Salesforce licenses, so four persona users aren't possible.

**Approach:** one test user, with permission set groups swapped between rounds. For each persona:

1. Assign the group, remove the others
2. Log in as the user
3. Walk the access matrix — confirm what should be visible is visible, and what shouldn't be, isn't
4. Attempt one thing the persona should be blocked from, and screenshot the denial
5. Record the result in `uat-results.md`

The negative test is the one that matters. Confirming a dispute specialist can open a case proves little; confirming a sales rep hits an insufficient-privileges error opening someone else's dispute proves the model works.

**In production this would be different:** persona test users in a full sandbox, run as part of every release rather than once at build time. Noted as a known limitation rather than glossed over.

---

## Access matrix

C = Create · R = Read · U = Update · D = Delete

| Object | Collections Rep | Dispute Specialist | Supervisor | Sales Rep |
|---|---|---|---|---|
| Account | R U | R U | R U | R U (own) |
| Contact | R U | R U | R U | C R U |
| Opportunity | R (Closed Won) | R (Closed Won) | R (Closed Won) | C R U D (own) |
| Commitment | R | R | R | C R U |
| Service Contract | R | R | R | R |
| Billing Statement | R | R | R U | — |
| Payment | R | R | R U | — |
| Promise to Pay | C R U | C R U | C R U D | — |
| Case — Billing Dispute | C R | C R U | C R U D | R (case team only, while open) |
| Case — Default Review | R | R | C R U | — |
| Adjustment | — | C R U | C R U + approve | — |
| Task | C R U D (own) | C R U D (own) | C R U D (own) | C R U D (own) |
| Lead | — | — | — | C R U |

---

## Build order

1. Public groups: `Collections_Team`, `Sales_Team`
2. Roles, top down
3. Org-wide defaults — set these *before* the sharing rules, since rules only make sense against a restricted baseline
4. The six permission sets, object and field permissions from the matrix
5. Permission set groups, then the muting permission set
6. Sharing rules
7. Case team role
8. Session and password settings, Health Check baseline
9. Test user, one persona at a time
