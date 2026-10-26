# Conventions & Configuration Standards

Written before the build, not after. Every rule here is one a reviewer can check against the org.

---

## Repo map

```
lumenfield-accord/
├─ README.md                  front door — the thing a hiring manager reads first
├─ CHANGELOG.md               release notes, one entry per phase
├─ sfdx-project.json
├─ .gitignore
├─ docs/
│  ├─ brief.md                problem, personas, scope, metrics
│  ├─ decision-log.md         D-01 onward
│  ├─ conventions.md          this file
│  ├─ requirements.md         user stories with acceptance criteria
│  ├─ data-model.md           Phase 3
│  ├─ data-dictionary.md      Phase 3/5
│  ├─ security-model.md       Phase 4
│  ├─ automation-inventory.md Phase 7
│  ├─ uat-results.md          Phase 10
│  └─ diagrams/               ERD, process maps (export as PNG or SVG)
├─ media/
│  └─ screenshots/            named by phase, see below
├─ data/                      synthetic seed data + import plan
└─ force-app/main/default/    org metadata, retrieved from Phase 3 onward
```

---

## Metadata naming

**Objects.** Singular, plain English: `Billing Statement`, `Promise to Pay`, `Commitment`. API names follow automatically; don't hand-edit them into abbreviations.

**Fields.** Descriptive over short. `Days_Past_Due__c`, not `DPD__c`. A field nobody can read is a field nobody maintains.

**Descriptions are mandatory.** Every object, field, flow, validation rule, permission set, and report type gets a Description explaining *why it exists*, not what it is. "Stores the promise date" is useless. "Date the customer committed to pay; drives the scheduled path that marks the promise kept or broken" is the standard. This one habit is the clearest signal of an admin who has cleaned up someone else's org.

**Flows.**
- Record-triggered: `Object_TriggerType_Purpose` → `Case_BeforeSave_StampServiceContract`
- Scheduled: `Scheduled_Purpose` → `Scheduled_OpenDefaultReviews`
- Screen: `Screen_Purpose` → `Screen_DisputeIntake`
- Subflows: `Sub_Purpose` → `Sub_LogFault`
- One record-triggered flow per object per trigger type unless there's a documented reason. Trigger order set explicitly.

**Validation rules.** `VR_Object_Condition` → `VR_Opportunity_ConcessionRequiresCommitment`. Error messages name the fix, not the rule.

**Permission sets and groups.** `PS_Function` → `PS_DisputeManagement`. Groups: `PSG_Persona` → `PSG_CollectionsRep`.

**Custom metadata.** `Policy_Threshold__mdt` records named for what they control, never a raw number in a flow.

**Queues, record types, report folders.** Named for the business function, not the object.

---

## No hardcoding

No record IDs, email addresses, thresholds, or date offsets inside flows. Thresholds live in custom metadata; recipients live in queues, groups, or custom metadata. If a value would change when the business changes its mind, it doesn't belong in the automation.

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
