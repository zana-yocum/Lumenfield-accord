# Security model — additions from Phases 6–10

Append these sections to the end of `docs/security-model.md`, then delete this file.

---

## Case sharing

| Rule | Type | Criteria | Shared with | Access |
|---|---|---|---|---|
| `Billing_Disputes_to_Collections` | Criteria-based | Record Type = Billing Dispute | Collections Rep role | Read Only |

Collections supervisors already see disputes through the role hierarchy. Default Review cases are not shared: they belong to the Default Reviews queue and the supervisor.

**Object access has to exist before sharing does anything.** The rule above created Read shares from day one, but reps still couldn't open a dispute because `PS_Collections_Core` had no Read on Case. Sharing decides *which* records; object permissions decide *whether* the object is reachable at all. Case access by persona: Collections Rep Read · Supervisor and Dispute Specialist Read/Create/Edit · Sales Rep Read (for case teams) · Delete for no one.

## Role hierarchy cleanup

Nine Developer Edition sample roles were deleted in Phase 6. Three of them sat directly **under** Dispute Specialist, which would have given dispute specialists visibility into any sales or marketing records owned by users in those roles. No users held them, so there was no live exposure, but the hierarchy was wrong by construction.

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

## Case teams

Sales reps reach a dispute only through the case team role **Sales Input**. The team role grants Edit, but `PS_Sales_Core` has Read on Case, so the object permission caps it at Read. `Case_AfterSave_DisputeLifecycle` removes the team when the case closes, so access ends without anyone remembering to remove it (US-08, US-18). Field-level security still applies inside the team: payment detail stays hidden.

## Activities

Task and Event access can't be granted or restricted through permission sets. Activity visibility follows access to the parent record, so a rep sees contact attempts on accounts they can see, and none on accounts they can't. `Task.Contact_Outcome__c` field-level security is granted per permission set like any other field.

## Reports and dashboards

| Folder | View | Edit |
|---|---|---|
| Collections (reports) | VP Customer Operations and subordinates | Collections Supervisor role |
| Collections Dashboards | VP Customer Operations and subordinates | Collections Supervisor role |
| Data Quality, Data Quality Dashboard | Admin only | Admin only |

**Run Reports** is granted through `PS_Collections_Core` and `PS_Dispute_Management`. Creating and customizing reports and dashboards stays with the supervisor group and `PS_Collections_Reporting`.

The Collections Supervisor dashboard **runs as the supervisor**, chosen deliberately rather than left as whoever built it. Anyone who can open the folder sees the supervisor's view of the numbers. That's acceptable here because everyone with folder access is in the collections chain; a dashboard for a wider audience would be dynamic (run as the viewer) instead.

## Exceptions to D-07

| Exception | Why |
|---|---|
| Minimum Access profile has **Residential Agreement** as default Account record type | A profile is the only place a default record type can be set. Lead conversion and new-account creation need one |
| **Lightning Experience User** granted through permission sets | Minimum Access doesn't include it, so persona users landed in Classic, where console apps don't exist |

## Approvals

System Administrators can submit and approve any approval regardless of the allowed-submitter list. In this two-license org the admin is also the supervisor, so self-approval is technically possible. In production the admin isn't a credit approver. Recorded as a known limit, not a control.

## Org-level settings added

| Setting | Value | Why |
|---|---|---|
| Require permission to view record names in lookup fields | On | Closes a leak where a user who can't see a record can still read its name through a lookup |
| Use Any API Auth | Deliberately not granted | Nothing in Accord logs in with a username and password (see `release-readiness-winter27.md`) |
| Profile Filtering | Enabled ahead of Winter '27 enforcement | Nothing depended on seeing other users' profiles |

## Health Check

**66% (Poor) → 96% (Excellent)** in Phase 4. The one remaining Critical is login IP ranges, left open deliberately: a remote workforce makes them impractical, and MFA plus session timeout are the compensating controls.
