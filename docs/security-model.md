# Security Model — Accord

Who can see what, why, and how it was verified. Updated for v1.0.3 (2026-10-26); the object and field tables were read from the org on 2026-10-25, and the sharing rules and record reach on 2026-10-26.

The guiding rule is least privilege: nobody gets access because it's convenient, and every grant traces to something a persona actually has to do in a user story.

---

## Personas

| Persona | What they do | The access question |
|---|---|---|
| **Collections rep** | Works past-due accounts, logs contact attempts and promises | Needs full context on delinquent accounts they don't own |
| **Dispute specialist** | Owns billing disputes end to end, gathers evidence, proposes credits | Needs cases, adjustments, and the commitments behind the sale |
| **Collections supervisor** | Watches queue health, approves credits, handles escalations and hardship | Needs everything the team sees, plus approval authority and overrides |
| **Sales rep** | Sells leases, records concessions at signing | Owns the account and opportunity, but has no business in payment data |

---

## Profiles and permission sets

Everyone sits on **Minimum Access - Salesforce**. No custom profiles exist in this org (D-07). The profile holds no object or field access to Accord's data; every grant lives in a permission set.

Access comes from function-based permission sets, assembled into persona-based groups:

| Permission set | Grants |
|---|---|
| `PS_Collections_Core` | Account and Contact read/edit · Billing Statement, Lease Payment, Service Contract, Opportunity, Commitment and Case read · Promise to Pay create/read/edit · the Log Contact Attempt flow (DEF-08) · Run Reports · the Collections Console app and tabs · read on the collections fields, edit only on Do Not Contact, Primary Contact, a promise's statement and a contact's role |
| `PS_Dispute_Management` | Case and Adjustment create/read/edit · Entitlement read · edit on the dispute fields and adjustment fields · Billing Dispute record type |
| `PS_Credit_Approval` | Adjustment read/edit for the approver · the approval authority itself is the Credit Approval process, which routes to the supervisor |
| `PS_Collections_Reporting` | Create and customize reports, manage dashboards, manage public list views |
| `PS_Payment_Detail` | Read on a payment's method and processor reference |
| `PS_Collections_Overrides` | Edit on the account fields automation maintains: Account Status, Collection Hold Until, High Value (DEF-09) |
| `PS_Sales_Core` | Lead, Opportunity, Account, Contact and Commitment create/read/edit · Case, Service Contract, Product and Price Book read · lead conversion · both account record types · edit on commitments, opportunity and lead fields, with no balances |

| Permission set group | Contains | Muted |
|---|---|---|
| `PSG_Collections_Rep` | `PS_Collections_Core` | Delete on Promise to Pay (`Mute_Rep_Promise_Delete`) |
| `PSG_Dispute_Specialist` | `PS_Collections_Core` + `PS_Dispute_Management` | — |
| `PSG_Collections_Supervisor` | `PS_Collections_Core` + `PS_Dispute_Management` + `PS_Credit_Approval` + `PS_Collections_Reporting` + `PS_Payment_Detail` + `PS_Collections_Overrides` | — |
| `PSG_Sales_Rep` | `PS_Sales_Core` | — |

Since Steward (2026-10-23), the three collections groups also hold Steward's rep-assistant permission sets, and those groups are maintained in Steward's repository. See the README's ownership note.

**Promise deletion, then and now.** The original design gave `PS_Collections_Core` delete on Promise to Pay for supervisors and muted it for reps, so one permission set could serve every persona. The system test found that deleting an active promise leaves the collection hold in place (OBS-01), so delete was removed from Collections Core and nobody can delete a promise; Cancelled is the supported exit. The rep group's muting permission set is still there. It no longer changes anything, but it would catch delete if it were ever granted again.

**Overrides are their own permission set.** Account Status drives the collections sharing rule, and Collection Hold Until and Broken Promises (90d) drive the work list, so automation sets them. A supervisor still has to move an account out of Hardship Review, close an account, or extend a hold. That edit lives in `PS_Collections_Overrides`, in the supervisor group only, instead of being folded into a permission set with another purpose.

### Exceptions to D-07

| Exception | Why |
|---|---|
| Minimum Access has **Residential Agreement** as its default Account record type | A profile is the only place a default record type can be set. Lead conversion and new-account creation need one |
| **Lightning Experience User** granted through permission sets | Minimum Access doesn't include it, so persona users landed in Classic, where console apps don't exist |

---

## Org-wide defaults

| Object | Default | Why |
|---|---|---|
| Account | Private | Financial and delinquency data. Access is granted deliberately, not inherited from everyone. |
| Contact | Controlled by Parent | A contact is only as visible as the account it belongs to. |
| Opportunity | Private | Sales data. Collections reads deals only through sharing rules: reps on accounts in collections, specialists on every closed deal. |
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

Nine Developer Edition sample roles were deleted in Phase 6. Three of them sat directly **under** Dispute Specialist, which would have given dispute specialists visibility into any sales or marketing records owned by users in those roles. No users held them, so there was no live exposure, but the hierarchy was wrong by construction.

---

## Sharing rules

The hard problem in this org: **sales owns the account, but collections has to work it.** A rep chasing a past-due balance doesn't own the record, isn't above the owner in the hierarchy, and can't be handed ownership without breaking the sales relationship.

| Rule | Shares | With | Access | Why |
|---|---|---|---|---|
| `Delinquent_Accounts_to_Collections` | Accounts where Account Status is Delinquent, Hardship Review, or Default Review | Public group Collections Team | Read/Write on the account, Read on its opportunities | Collections works accounts it doesn't own, and only once they're delinquent. The deal access shows reps the commitments on those accounts, and goes when the account leaves collections (DEF-10). |
| `Closed_Won_to_Dispute_Specialists` | Opportunities where Stage equals Closed Won | Dispute Specialist role (supervisors through the hierarchy) | Read Only | Commitments are master-detail children of Opportunity, so without this a dispute specialist can't see what was promised at signing when a current customer disputes a bill. |
| `Billing_Disputes_to_Collections` | Cases with the Billing Dispute record type | Collections Rep role | Read Only | Reps need to know a dispute is open before calling. Editing stays with the specialist who owns it. Supervisors already see disputes through the hierarchy. |

**Public groups:** `Collections_Team` is the Collections Supervisor role and its subordinates (supervisors, reps, specialists). It had no members from Phase 4 until Oct 14, 8:46 PM CT, so until then the rules that share with it reached nobody (DEF-10). `Sales_Team` is the sales chain. Default Review cases aren't shared: they belong to the Default Reviews queue, whose member is the Collections Supervisor role. Billing disputes route to the Dispute Specialists queue (the Dispute Specialist role).

The closed-deal rule is worth pausing on. Master-detail inheritance means a relationship decision made in Phase 3 created a security requirement in Phase 4. If commitments had been a lookup instead, they'd need their own sharing — and the validation rule in US-02 wouldn't work. The trade-off runs in both directions.

**Implicit sharing reaches the account.** Anyone who can read an opportunity, a case or a contact can read its account. Salesforce does this on its own, and no setting turns it off. As first built, the closed-deal rule (`Closed_Won_to_Collections`) shared every deal with the whole Collections Team, so every rep could read every customer account, including all the current ones D-08 keeps out of reach (DEF-10). That rule is deleted. Reps now get deal access through the account rule, so it follows Account Status: Test Persona reads 40 accounts, not 100. Two implicit paths remain on purpose:
- Dispute specialists, and supervisors through the hierarchy, read every customer account, through the closed deals. Any customer can dispute a bill.
- Reps read an account that has a billing dispute, read-only, through the case rule. Six current accounts had one on 2026-10-25. Narrowing that would mean copying the account's status onto every case.

To check one user and one record, query `UserRecordAccess`. To see why the access exists, query the account's `AccountShare` rows: a row cause of `ImplicitParent` means it came from a child record.

**Object access has to exist before sharing does anything.** The case rule created Read shares from day one, but reps still couldn't open a dispute because `PS_Collections_Core` had no Read on Case. Sharing decides *which* records; object permissions decide *whether* the object is reachable at all.

**Account Status is a security field.** Because the account rule reads it, whoever can edit Account Status can widen or narrow who sees the account. That's why it's read-only to everyone but supervisors (DEF-09) and set by the daily status flow.

---

## Field-level security

Record access and field access are separate layers, and both have to be right.

**Field access comes only from permission sets.** Setup's new-field wizard makes every field visible to every profile unless the boxes are cleared, and until v1.0.2 the Minimum Access profile granted access to 74 of Accord's fields, 58 of them editable (DEF-09). Reps and sales reps could edit Account Status. The fix moved each persona's fields into its permission sets and removed every Accord field from the profile. **For any new field: clear the profile boxes in the wizard, and grant the field through the persona's permission set.**

| Field | Rep | Specialist | Supervisor | Sales |
|---|---|---|---|---|
| Account: Current Balance, Past Due Balance, Days Past Due, DPD Bucket, Oldest Past Due Date | Read | Read | Read | **Hidden** |
| Account: Broken Promises 90d, Priority Score, Threshold Crossed Date | Read | Read | Read | **Hidden** |
| Account: Account Status | Read | Read | Edit | Read |
| Account: Collection Hold Until, High Value | Read | Read | Edit | **Hidden** |
| Account: Do Not Contact | Edit | Edit | Edit | Read |
| Account: Primary Contact | Edit | Edit | Edit | Edit |
| Billing Statement: all fields | Read | Read | Read | No object access |
| Payment: Method, External Reference | **Hidden** | **Hidden** | Read | No object access |
| Promise to Pay: statement | Edit | Edit | Edit | No object access |
| Promise to Pay: amount received, grace end, out of policy | Read | Read | Read | No object access |
| Case: dispute reason, root cause, resolution summary, disputed statement | Read | Edit | Edit | Read, except the statement |
| Adjustment: all fields (posted date read-only) | No access | Edit | Edit | No access |
| Commitment: all fields | Read | Read | Read | Edit (service contract read-only) |
| Service Contract: terms and dates | Read | Read | Read | Read |
| Lead: service area, address, inquiry detail | No object access | No object access | No object access | Edit |
| Legacy Id (every object) | **Hidden** | **Hidden** | **Hidden** | **Hidden** |

Required and master-detail fields, such as a promise's amount and date, are always visible to anyone who can see the record, so they aren't in the table.

Sales reps keep the account but lose the money. They have no operational need for a customer's balance or payment history, and every additional person who can see payment data is additional exposure if an account is ever compromised.

This is also what makes the second acceptance criterion in US-08 true: a sales rep added to a dispute case team gets record access to that case, but field-level security still hides payment detail on it. Record access opens the door; FLS decides what's visible once inside.

---

## Flows and who can run them

Record-triggered and scheduled flows run in system context and need no user access. Accord's one screen flow, **Log Contact Attempt**, is different: a user needs the Run Flows permission or access to that specific flow. Until v1.0.2 no persona had either, so Lightning hid the action from every collections persona (DEF-08). The flow now restricts access to enabled permission sets, and `PS_Collections_Core` grants it. Run Flows wasn't used, because it opens every current and future flow, and this flow runs in system mode with sharing so reps can set Do Not Contact and Hardship Review without broad edit rights.

---

## Case teams — access that expires

US-08 needs a sales rep to answer questions on a dispute naming their deal, then lose that access when the case closes.

**Case team role:** `Sales Input`. The team role grants Read/Write, but `PS_Sales_Core` has Read on Case, so the object permission caps it at Read.

- The dispute specialist adds the sales rep to the case team in that role when input is needed.
- When the case reaches Resolved or Closed, `Case_AfterSave_DisputeLifecycle` removes the team, so access ends without anyone remembering to remove it (US-08, US-18).
- Access exists only while the case is open, and it's visible to anyone looking at the case rather than buried in a sharing rule.

**What was rejected and why:**
- *Sharing sets* only apply to Experience Cloud external users. Not applicable to internal reps.
- *Criteria-based sharing rules* can't be revoked per record — a rule broad enough to grant access would grant it to every matching case, permanently.
- *Manual sharing* would work but relies on someone remembering to remove it, which is how orgs accumulate access nobody can explain.

**Open question:** US-08 also says the sales rep adds comments. Whether a team member with Read can add a case comment hasn't been confirmed in the console yet (`docs/persona-checks.md`, step 8).

---

## Activities

Task and Event access can't be granted or restricted through permission sets. Activity visibility follows access to the parent record, so a rep sees contact attempts on accounts they can see, and none on accounts they can't. `Task.Contact_Outcome__c` field-level security is granted per permission set like any other field.

---

## Reports and dashboards

| Folder | View | Edit |
|---|---|---|
| Collections (reports) | VP Customer Operations and subordinates | Collections Supervisor role |
| Collections Dashboards | VP Customer Operations and subordinates | Collections Supervisor role |
| Data Quality, Data Quality Dashboard | Admin only | Admin only |

**Run Reports** is granted through `PS_Collections_Core` and `PS_Dispute_Management`. Creating and customizing reports and dashboards stays with the supervisor group and `PS_Collections_Reporting`.

The Collections Supervisor dashboard **runs as a specified user**, chosen deliberately rather than left as whoever built it. Anyone who can open the folder sees that user's view of the numbers. That's acceptable here because everyone with folder access is in the collections chain; a dashboard for a wider audience would be dynamic (run as the viewer) instead. In the repository its running user is a placeholder on `example.com`.

---

## Approvals

System Administrators can submit and approve any approval regardless of the allowed-submitter list. In this two-license org the admin is also the supervisor, so self-approval is technically possible. In production the admin isn't a credit approver. Recorded as a known limit, not a control.

---

## Org-level security

| Setting | Value | Why |
|---|---|---|
| MFA | Required, all users | Salesforce requirement as of June 2026 |
| Admin MFA | Phishing-resistant (passkey or security key) | Required for System Administrator access |
| Session timeout | 2 hours, force logout on timeout | Collections workstations sit unattended |
| Login IP ranges | Not restricted | Documented deliberately: a remote workforce makes IP ranges impractical. Compensating control is MFA plus session timeout. |
| Password policy | 90-day expiry, 8 character minimum, 3 passwords remembered | |
| Require permission to view record names in lookup fields | On | Closes a leak where a user who can't see a record can still read its name through a lookup |
| Use Any API Auth | Deliberately not granted | Nothing in Accord logs in with a username and password |
| Profile Filtering | Enabled ahead of Winter '27 enforcement | Nothing depended on seeing other users' profiles |

**Health Check: 66% (Poor) → 96% (Excellent)** in Phase 4. The one remaining Critical is login IP ranges, left open deliberately for the reason above.

Naming the control you *didn't* implement, and what covers for it, is worth more than a clean list. Every real org has these.

---

## How it was tested

Developer Edition provides very few full Salesforce licenses, so four persona users aren't possible. One test user, Test Persona, stands in for each persona in turn.

1. **Through the API, as the admin:** object and field access read per persona from each group's own permissions, and per user through `UserFieldAccess`. This is fast and exact, and it's how DEF-09 was found and its fix counted field by field. Record reach is checked the same way, per user and record, through `UserRecordAccess`; that's how DEF-10 was found.
2. **In the console, as the persona:** Setup → Users → Test Persona → **Login**, with the group switched between rounds. This is the only test of what the persona actually sees. It's how DEF-08 was found: every API check had run as the admin, who can run any flow, so a missing action never showed.
3. **The negative test is the one that matters.** Confirming a dispute specialist can open a case proves little; confirming a sales rep hits an insufficient-privileges error opening someone else's dispute proves the model works. The Phase 6 negative test did exactly that for US-08 and US-18.

Results: `docs/system-test-results-2026-10-14.md`. The console checks still to run are in `docs/persona-checks.md`.

**In production this would be different:** persona test users in a full sandbox, run as part of every release rather than once at build time. Noted as a known limitation rather than glossed over.

---

## Access matrix

C = Create · R = Read · U = Update · D = Delete. Read from each group's permissions in the org on 2026-10-25. No persona can delete any of these records. Which records each persona reaches comes from sharing: reps edit accounts in collections and read accounts with a billing dispute; specialists and supervisors also read every customer account through the closed deals. Service contracts are private and no rule shares them, so the Read on Service Contract reaches no records for any persona but their owner (checked for Test Persona on 2026-10-25). No story needs a person to open one; the automation that uses them runs in system context.

| Object | Collections Rep | Dispute Specialist | Supervisor | Sales Rep |
|---|---|---|---|---|
| Account | R U | R U | R U | C R U |
| Contact | R U | R U | R U | C R U |
| Opportunity | R (accounts in collections) | R (Closed Won) | R (Closed Won) | C R U (own) |
| Commitment | R | R | R | C R U |
| Service Contract | R | R | R | R |
| Billing Statement | R | R | R | — |
| Lease Payment | R | R | R | — |
| Promise to Pay | C R U | C R U | C R U | — |
| Case — Billing Dispute | R | C R U | C R U | R (case team only, while open) |
| Case — Default Review | — (not shared) | — (not shared) | C R U (queue) | — |
| Adjustment | — | C R U | C R U + approve | — |
| Task | Follows the parent record | Follows the parent record | Follows the parent record | Follows the parent record |
| Lead | — | — | — | C R U |

---

## Build order

1. Public groups: `Collections_Team`, `Sales_Team`
2. Roles, top down
3. Org-wide defaults — set these *before* the sharing rules, since rules only make sense against a restricted baseline
4. The seven permission sets, object and field permissions from the tables above, with the profile boxes cleared on every new field
5. Permission set groups, then the muting permission set
6. Sharing rules
7. Case team role
8. Session and password settings, Health Check baseline
9. Test user, one persona at a time: through the API, then in the console
