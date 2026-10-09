## v0.6 — 2026-10-09 — Phase 7: Automation

Ten flows, an approval process and five validation rules. Every story they serve was tested against the org through the API, and every test record was deleted afterward.

### Added — flows
| Flow | Type | Does | Stories |
|---|---|---|---|
| `Account_Daily_Collections_Status` | Scheduled, daily | Sets Account Status from Days Past Due; stamps Threshold Crossed Date; opens a Default Review case owned by the Default Reviews queue | US-05, US-15, D-08 |
| `Account_Daily_BrokenPromiseCount` | Scheduled, daily | Recounts broken promises in the last 90 days so the count rises and falls | US-04, US-05 |
| `Contact_AfterSave_StampPrimaryContact` | After save | Primary-role contact becomes the account's primary; first contact stands in until then | US-01, US-19 |
| `Case_BeforeSave_StampEntitlement` | Before save | Attaches the account's active entitlement to new Billing Disputes | US-09 |
| `Case_AfterSave_DisputeLifecycle` | After save | Flags and restores the disputed statement; completes milestones as status advances; removes the case team at close | US-07, US-08, US-09, US-18 |
| `Promise_AfterSave_ApplyPolicy` | After save | Blocks a second active promise; out-of-policy promises go to Pending Approval; in-policy promises set the collection hold | US-03 |
| `Promise_Daily_Evaluate` | Scheduled, daily | After grace, totals real payments and marks Kept or Broken; releases the hold | US-04 |
| `Opportunity_AfterSave_CreateServiceContract` | After save | At Closed Won, creates the service contract and links the deal's commitments | US-02 |
| `Adjustment_AfterSave_Lifecycle` | After save | Credits within the rep limit post immediately; submission, approval and rejection move the related dispute | US-11, US-13 |
| `ServiceContract_AfterSave_WelcomeAndReminder` | After save + scheduled path | Welcome email on activation, first-payment reminder 7 days before due, follow-up task when there's no email | US-19, US-20, US-21 |

### Added — rules and approvals
- `VR_Account_PrimaryContactRequired` — activated after backfilling all 100 accounts; skips the first save so new households can be created
- `VR_Opp_ConcessionNeedsCommitment` — fires only on the move to Closed Won, so historical deals aren't blocked
- `VR_Adjustment_ApprovalRequired` — credits over the limit can't be set to Approved or Posted by hand. Approval field updates skip validation rules, which makes the approval process the only route through
- `VR_Adjustment_AmountLockedAfterApproval`
- `VR_Case_RootCauseRequired` — a billing dispute can't be Resolved without a root cause (US-10)
- **Credit Approval** process: over $100 to the Collections Supervisor; only Dispute Specialists and Collections Reps can submit

### Data
- Primary Contact backfilled on all 100 accounts; the "no one to contact" data quality metric goes from 88 to 0
- The 13 test disputes brought in line with the new flows: 10 statements flagged In Dispute, 12 passed milestones completed

### Verified
- Status flow fixed a mismatch account and it became visible to collections immediately, while the other mismatch stayed hidden until processed — status is a security control
- New household: saves without contacts → co-signer stands in → Primary-role contact takes over; clearing the primary is blocked
- Dispute: entitlement attached, statement flagged, milestones completed in order and on skips, case team removed at close, statement restored to its real status
- Promise: second active promise blocked; full in-window promise held the account to the grace date; short promise went to Pending Approval with no hold
- Deal with a concession blocked at Closed Won until a commitment existed; then a service contract was created and the commitment linked
- Welcome email sent and stamped on activation; reminder scheduled for 7 days before first due
- Credits: $75 posted on its own; $250 blocked from manual approval, approved through the process, posted, dispute returned to Under Review; approved amount locked

### Lessons recorded
- Approval field updates skip validation rules. Used deliberately to make the approval process the only path for large credits — and it's why a rejection reason can't be enforced on a rejection that comes through the approval process
- System Administrators can submit any approval regardless of allowed submitters. In a two-license org where the admin is also the supervisor, self-approval is possible; in production, admins don't approve credits
- Approval entry criteria can't read custom metadata, so the $100 threshold is duplicated from `Rep_Credit_Limit`
- Milestones lock once their case exits the entitlement process
- Detail objects in a master-detail relationship can't be owned by queues
- Validation rule API names are limited to 40 characters

### Known limits
- Scheduled path offsets can't read custom metadata; the reminder is fixed at 7 days and duplicates `Pre_Due_Offset_Days`
- Promise evaluation counts payments on the promise's related statement only; promises without a related statement (5 seeded orphans) can only be marked Broken
- Approver is a named user, a Developer Edition license constraint
