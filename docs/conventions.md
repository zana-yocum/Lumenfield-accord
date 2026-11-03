# Conventions & Configuration Standards

Written before the build, not after. Every rule here is one a reviewer can check against the org. Checked against the org on 2026-11-03: where the build settled on a different pattern than first written, the pattern below is the one the org actually follows, and the change is noted.

---

## Repo map

```
lumenfield-accord/
├─ README.md                  front door — the thing a hiring manager reads first
├─ CHANGELOG.md               release notes, one entry per version
├─ sfdx-project.json
├─ .gitignore
├─ docs/
│  ├─ brief.md                problem, personas, scope, metrics
│  ├─ decision-log.md         D-01 onward
│  ├─ conventions.md          this file
│  ├─ requirements.md         user stories, acceptance criteria, traceability
│  ├─ data-model.md           ERD and relationship decisions, as built
│  ├─ data-dictionary.md      every custom field
│  ├─ data-plan.md            seed data design and load results
│  ├─ security-model.md       access by persona, as built
│  ├─ uat-scripts.md          21 scripts, one or more per story
│  ├─ system-test-results-2026-10-14.md   evidence and defects (DEF-xx)
│  ├─ persona-checks.md       what a role can't see or do
│  ├─ rca-balance-formula.md  root cause analysis
│  ├─ support-runbook.md      symptom → check → fix
│  ├─ quick-reference.md      one page for reps
│  ├─ case-study.md
│  └─ open-items.md
├─ media/screenshots/         named by phase, see below
├─ data/                      seed data, load results, and the re-age routine (data/regen)
├─ manifest/                  retrieve and cleanup manifests
├─ scripts/                   check_personal_details.sh
├─ web/                       the web-to-lead form
└─ force-app/main/default/    org metadata, retrieved from the org
```

The ERD lives in `data-model.md` as Mermaid, which GitHub renders, rather than as exported images.

---

## Metadata naming

**Objects.** Singular, plain English: `Billing Statement`, `Promise to Pay`, `Commitment`. API names follow automatically; don't hand-edit them into abbreviations.

**Fields.** Descriptive over short. `Days_Past_Due__c`, not `DPD__c`. A field nobody can read is a field nobody maintains.

**Descriptions are mandatory.** Every object, field, flow, validation rule, permission set, and report type gets a Description explaining *why it exists*, not what it is. "Stores the promise date" is useless. "Date the customer committed to pay; drives the scheduled path that marks the promise kept or broken" is the standard. This one habit is the clearest signal of an admin who has cleaned up someone else's org.

**Flows.** `Object_Trigger_Purpose` for every flow, so the flow list sorts by the object it works on. The label reads the same in words.
- Record-triggered: `Case_BeforeSave_StampEntitlement`, `Adjustment_AfterSave_Lifecycle`
- Scheduled: `Account_Daily_Collections_Status` (label *Account - Daily - Collections Status*), `Billing_Statement_Daily_Status`
- Screen: `Account_Screen_LogContactAttempt`
- Subflows, if one is ever needed: `Sub_Purpose`
- The first draft of this file gave scheduled and screen flows their own prefixes (`Scheduled_`, `Screen_`). The build led with the object instead, and this is the pattern the org follows.
- One record-triggered flow per object per trigger type unless there's a documented reason. Trigger order set explicitly.

**Validation rules.** `VR_Object_Condition` → `VR_Account_PrimaryContactRequired`, `VR_Payment_DateNotFuture`. Error messages name the fix, not the rule. (One exception slipped through: `VR_Opp_ConcessionNeedsCommitment` abbreviates Opportunity.)

**Permission sets and groups.** `PS_Function` → `PS_Dispute_Management`. Groups: `PSG_Persona` → `PSG_Collections_Rep`. Words separated by underscores, as the org has them.

**Custom metadata.** `Policy_Setting__mdt` records named for what they control (`Default_Threshold_DPD`, `Promise_Grace_Days`), never a raw number in a flow.

**Queues, record types, report folders.** Named for the business function, not the object.

---

## No hardcoding

No record IDs, email addresses, thresholds, or date offsets inside flows. Thresholds live in custom metadata; recipients live in queues, groups, or custom metadata. If a value would change when the business changes its mind, it doesn't belong in the automation.

---

## Testing

- **Pass or fail comes from evidence in the org**, never from a summary of what should have happened. A test result names the record, the query or the run that proves it.
- **Test as the persona.** An admin login proves nothing about what a rep can see or do. Check through the persona, by logging in as the user or querying `UserRecordAccess` and `UserFieldAccess` for them.
- **Every formula gets a known-answer test:** one record where the expected result is worked out by hand first, then compared. (From `rca-balance-formula.md`: the balance formula was checked with throwaway records but no hand-worked expected value, and returned $0 on every statement until someone looked at one unpaid bill.)
- **Clock-dependent behavior gets checked when the clock gets there.** Scheduled runs, milestone violations and promise grace periods are recorded as open until a real run produces the evidence.
- **Throwaway test records are deleted after the test**, and the test write-up says so.

---

## Commits

One commit per meaningful change, message written like a release note:

```
phase-04: add permission set groups for the four personas
phase-06: entitlement process with 1-day acknowledge / 30-day resolve milestones
docs: D-03 — case record type over custom dispute object
```

Never commit credentials, security tokens, `.env` files, or org auth URLs.

---

## Screenshots

`media/screenshots/phase04-permission-set-group-supervisor.png`

- Prefix with the phase so the folder sorts in build order.
- Crop to the panel that matters. No full desktop, no browser chrome, no taskbar.
- Nothing on screen but Lumenfield: no other org tabs, no personal email in the header.
- Capture the *before* state too when you're about to change something. You can't go back for it later.

---

## Capture as you go

At the end of every phase, before you move on:

- Screenshots of what you built, named as above
- Any decision made, written into the decision log the same day
- Time spent on the phase
- One thing that surprised you or went wrong

That last one matters most. The case study needs friction to be believable — a build where nothing went sideways reads as fiction, and reviewers say the biggest red flag in a portfolio is a project where every step worked.

---

## Definition of done, per phase

A phase isn't finished until:

1. It's built in the org and works when you test it as the persona who'll use it.
2. Descriptions are filled in on everything you created.
3. Documentation in `/docs` is updated.
4. Screenshots are captured and named.
5. Metadata is retrieved and committed, with a CHANGELOG entry.
