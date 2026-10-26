# Lumenfield Home Energy — Decision Log

**Project:** Accord — collections and concessions build
**Owner:** Zana Yocum, Salesforce Administrator
**Org:** Lumenfield Home Energy (Developer Edition, synthetic data)

Every entry uses the same format: context, options considered, decision, rationale, consequences, revisit if, decided by and date.

---

## D-01 — Customer data model: Account + Contact, not Person Accounts

**Context.** Lumenfield's customers are homeowners on 20–25 year residential solar leases. Most agreements carry two names, a spouse or a co-signer. Billing statements, payments, disputes, and service contracts all hang off the agreement and the service address, not off one individual. A smaller set of customers are HOAs and property managers, which are organizations rather than people.

**Options considered.**

1. **Person Accounts.** Built for consumer businesses. One record represents the individual.
2. **Account + Contact.** The Account is the agreement and service address. Contacts are the people named on it.

**Decision.** Account + Contact, with an Account record type of Residential Agreement.

**Rationale.** Two people on one lease model cleanly as two Contacts on one Account, with one flagged primary for billing and automation. The same structure handles HOA and property-manager customers without needing a second data model. Person Accounts cannot be turned off once they're enabled, and they add friction to sharing, Experience Cloud, and some managed packages later. Nothing in the requirements needs an individual to be an Account.

**Consequences.** Salesforce's own guidance for consumer businesses leans toward Person Accounts, so this choice has to be defensible out loud. Reporting on "customers" means reporting on Contacts with a role, not on Accounts. Every automation that contacts a customer needs a designated primary contact, so primary contact becomes a required field with a validation rule behind it.

**Revisit if.** Lumenfield starts selling products with no agreement behind them, or adopts a package that assumes Person Accounts.

**Decided by / date.** Zana Yocum, 2026-09-24.

---

## D-02 — Where concessions get captured: at signing, on the Opportunity

**Context.** Reps promise things at closing: a promotional credit, a delayed billing start, the first couple of payments covered. When none of it is written down, the first past-due call becomes a dispute and nobody can prove what was agreed. This is the problem the whole build exists to solve, so where the commitment gets captured shapes the data model, the automation, and the security around it.

**Options considered.**

1. **At signing, on the Opportunity.** A Commitment record is required before the deal can be marked Closed Won.
2. **At provisioning, on the Service Contract.** Operations records commitments when the agreement is set up, so sales isn't slowed down at close.
3. **At dispute time, as evidence on the Case.** Lightest build, no sales friction, no prevention.

**Decision.** Option 1. Commitments are captured on the Opportunity at signing, with a validation rule blocking Closed Won when a concession was offered and no Commitment record exists. Closed Won then creates the Service Contract and relates the commitments to it.

**Rationale.** Only option 1 prevents the proof gap instead of managing it after the fact. The rep who made the promise is the only person who reliably knows the terms, and the moment they still remember is at close. Option 2 hands the work to someone who wasn't in the conversation. Option 3 leaves collections doing archaeology on every dispute, which is the current state.

**Consequences.** Sales gets one more required step at the worst possible moment, right as they're closing, so the capture screen has to be fast and the error message has to name exactly what's missing. A roll-up summary on Opportunity is needed so the validation rule can count child Commitments, which forces the relationship to be master-detail rather than lookup. Deals closed before this rule existed have no commitments, so baseline reports have to exclude or flag them.

**Revisit if.** Sales cycle friction shows up in the numbers, or concessions start being approved after close often enough that the Opportunity is the wrong home for them.

**Decided by / date.** Zana Yocum, 2026-09-24.

---

## D-03 — Disputes are Cases with a record type, not a custom object

**Context.** Billing disputes are the center of this build. They need queues, assignment and escalation rules, SLA tracking, a way to pull other people in temporarily, and an activity history. The choice is whether they live on the standard Case object or on a custom Dispute object built for the purpose.

**Options considered.**

1. **Case with a Billing Dispute record type.** Standard object, standard everything around it.
2. **Custom `Dispute__c` object.** A data model shaped exactly to disputes, with nothing inherited that doesn't apply.

**Decision.** Case, with Billing Dispute and Default Review record types, each with its own support process and page layout.

**Rationale.** Entitlements and milestones only work on Case, and the SLA requirements in US-09 and US-14 are built entirely on them. Case teams — the mechanism behind the expiring sales rep access in US-08 — also only exist on Case. Queues, assignment rules, escalation rules, and email-to-case all come free. A custom object would mean rebuilding every one of those, and rebuilding an SLA engine in flow is the kind of decision that looks clever for a month and expensive for years.

**Consequences.** Cases carry fields that don't apply to a billing dispute, so page layouts and record types do the work of hiding them. Two very different processes now share one object, which means reporting has to filter by record type consistently or the numbers mix. Anyone with broad Case access sees disputes too, which is why org-wide default on Case is Private rather than Read.

**Revisit if.** Dispute volume or field count grows past what record types can keep clean, or a future process needs dispute records visible to people who shouldn't see cases at all.

**Decided by / date.** Zana Yocum, 2026-09-24.

---

## D-04 — Declarative only: no custom Lightning components in this build

**Context.** Three requirements pointed naturally at custom components: a prioritized work queue with auto-advance, a live SLA countdown on the dispute, and a unified approval context screen for supervisors. All three would be nicer with code than without.

**Options considered.**

1. **Build the three components.** Best user experience, most control.
2. **Use standard equivalents.** A formula field and console list views for the queue, the standard milestone tracker for the SLA clock, a compact layout and related lists for approval context.
3. **Build one component** where the standard equivalent is weakest, and use standard for the other two.

**Decision.** Option 2. Nothing custom in this build.

**Rationale.** The platform already does all three acceptably. Every custom component becomes something to test on each release and something the next admin has to understand, and the guidance is to exhaust standard functionality before building. There's also a scope reason: this project demonstrates configuration judgment, and the next project is where Apex and Lightning web components are the point. Choosing not to build is part of the work.

**Consequences.** The rep queue doesn't auto-advance, so reps move through list views in split view instead. The SLA display is the standard tracker rather than a color-changing countdown, which is a cosmetic loss. Supervisors get approval context through layout design rather than a purpose-built screen, which is the weakest of the three trade-offs and the one to revisit first.

**Revisit if.** Reps report that list views are slowing them down measurably, or approval decisions are being made without the context because it takes too many clicks to find.

**Decided by / date.** Zana Yocum, 2026-09-24.

---

## D-05 — Consent gates promotional messages, not servicing messages

**Context.** Every outreach flow in the build has to check consent before sending. The question is what consent covers. The first pass would have suppressed all automated communication — including past-due notices — whenever a marketing opt-in was missing.

**Options considered.**

1. **One consent flag governs everything.** Simplest to build, easiest to explain.
2. **Split by message purpose.** Promotional messages require recorded consent for that channel. Servicing messages — statement ready, payment past due, dispute resolution — send regardless, and stop only on an explicit do-not-contact request.

**Decision.** Option 2, using the standard consent objects rather than a checkbox on Contact.

**Rationale.** Option 1 would mean the company couldn't tell a customer their payment is late unless they'd opted into marketing, which breaks the business and isn't what consent regimes actually require. The standard consent data model carries an effective date and capture source per channel, so the org can show what someone agreed to and when — which is the part that matters if it's ever questioned. A checkbox can't do that.

**Consequences.** Every outreach flow calls a shared consent subflow and passes a message purpose, so the rule is enforced in one place rather than copied into each flow. Someone has to classify every message as promotional or servicing, and that classification is a business decision, not an admin one. In a real org the line would be confirmed with compliance rather than assumed.

**Revisit if.** Lumenfield adds a channel with different rules, like SMS, or a jurisdiction requires consent for servicing messages too.

**Decided by / date.** Zana Yocum, 2026-09-24.

---

## D-06 — Billing statements are master-detail to Account, not to Service Contract

**Context.** A billing statement logically belongs to the agreement it bills for. But collections reps work accounts, and US-01 requires balance, days past due, and aging visible on the account without navigating. Roll-up summaries only work across master-detail relationships, and a custom object can only have one master.

**Options considered.**

1. **Master-detail to Service Contract**, with Account balance derived some other way — a scheduled flow stamping totals, or a report.
2. **Master-detail to Account**, with Service Contract as a lookup on the statement.

**Decision.** Option 2. Statements are master-detail to Account with a lookup to Service Contract.

**Rationale.** The account is where the work happens and where the numbers need to be, and roll-ups are the platform's own answer for that — accurate on every save, no automation to maintain, no timing gap. Deriving account balance with a scheduled flow would mean the rep's screen is accurate as of last night, which is not acceptable when someone is on the phone about a payment they made this morning. The Service Contract lookup preserves everything reporting needs.

**Consequences.** A household with two agreements sees one combined balance at the account level, and contract-level totals require a report grouped by the lookup rather than a field. Statements inherit the account's sharing, which is what keeps the Phase 4 security model simple. It also forces a related decision: statement status has to be a stamped picklist rather than a formula, because roll-up filter criteria can't reference formulas containing `TODAY()`.

**Revisit if.** Multi-agreement households become common enough that a combined balance misleads reps, or contract-level roll-ups become a real requirement rather than a reporting preference.

**Decided by / date.** Zana Yocum, 2026-09-24.

---

## D-07 — Minimum Access profile plus permission set groups, no custom profiles

**Context.** Four personas need four different levels of access. The org has to grant it somehow, and profiles are the traditional answer.

**Options considered.**

1. **Custom profiles per persona.** One profile each, carrying object and field permissions directly.
2. **Minimum Access - Salesforce for everyone, with permission set groups.** Profiles hold almost nothing; every grant lives in a permission set.
3. **A hybrid** — a base custom profile with permission sets layered on top.

**Decision.** Option 2. Everyone sits on Minimum Access - Salesforce. All access comes from permission sets assembled into persona groups, with muting used where a persona needs slightly less than the group provides.

**Rationale.** A user has exactly one profile and can have many permission sets, so profile-based access forces a new profile every time a persona varies slightly, and orgs end up with a dozen near-identical profiles nobody dares consolidate. Permission sets are additive and reusable — `PS_Collections_Core` serves three personas here instead of being copied three times. Salesforce's own direction is away from profiles for access, and starting on that path costs nothing now and saves a migration later. Auditing is also simpler: "what can a dispute specialist do" is answered by opening one group rather than diffing profiles.

**Consequences.** Some settings still live only on the profile — login hours, IP ranges, default record types, page layout assignment — so the profile isn't empty and can't be ignored. Permission set groups add an indirection: troubleshooting "why can this person see that" means checking the group, its member sets, and any muting set rather than one page. Muting is powerful and easy to misuse; it's used exactly once here, for delete on Promise to Pay, and that use is documented.

**Revisit if.** The number of permission sets grows past what's readable, or a persona needs something only a profile can carry.

**Decided by / date.** Zana Yocum, 2026-09-26.

---

## D-08 — Collections reaches accounts through a sharing rule, not ownership

**Context.** Sales owns the account. Collections has to work it once it goes past due. Account org-wide default is Private, collections reps aren't above sales in the role hierarchy, and a delinquent account still belongs to the rep who sold it.

**Options considered.**

1. **Transfer ownership to collections** when an account goes delinquent, and back when it cures.
2. **Criteria-based sharing rule** granting the collections team read/write on accounts in a delinquent status.
3. **Open the org-wide default** to Public Read/Write and control access with page layouts and field-level security.

**Decision.** Option 2. A criteria-based rule shares accounts with Account Status of Delinquent, Hardship Review, or Default Review with the Collections Team public group, read/write. A second rule shares Closed Won opportunities read-only, because commitments are master-detail children and are otherwise invisible to collections.

**Rationale.** Option 1 breaks the sales relationship — the rep loses their own customer from their views and reports the moment a payment is late, and ownership churns every time an account cures and relapses. Option 3 is the common shortcut and it means every user in the org can see every customer's balance, which is exactly the exposure the field-level security design is trying to prevent. A criteria-based rule grants access on the condition that justifies it and withdraws it automatically when the condition ends.

**Consequences.** Access depends on Account Status being accurate, which makes a status-stamping flow a security control rather than a convenience — worth calling out in the Phase 7 automation notes. Sharing recalculation on criteria-based rules isn't instant at scale, so in a large org there's a lag between an account going delinquent and collections seeing it. Restriction rules were considered for tightening dispute visibility further and left out as more than this build needs; that's a documented omission, not an oversight.

**Revisit if.** Account volume makes sharing recalculation slow enough to affect reps, or a compliance requirement demands collections access be logged per record rather than granted by rule.

**Decided by / date.** Zana Yocum, 2026-09-26.

**Implementation note (2026-10-25, DEF-10).** As built, the closed-deal rule shared with the same Collections Team group, and read access to a deal gives read access to its account. So once the group had members, every rep could read every customer account, current or not. Reps now get deal access from the account rule itself, which grants read on the account's opportunities, so it follows Account Status. The closed-deal rule shares with dispute specialists only. The old rule was deleted on 2026-10-26. The decision stands, and the implementation now matches it.

---

## D-09 — Legacy ID fields stay in the org after the data load

**Context.** Loading child records requires pointing at parents that don't have Salesforce IDs yet. The standard approach is an External ID field on each parent carrying a stable identifier from the source system, so Data Loader can resolve relationships at insert time.

**Options considered.**

1. **Add `Legacy_Id__c` External ID fields, then delete them** once the load finishes, leaving a clean data model.
2. **Add them and keep them**, documented as migration artifacts.
3. **Skip External IDs** and load in stages, exporting Salesforce IDs after each parent load and mapping them into the child files by hand.

**Decision.** Option 2. `Legacy_Id__c` is added to Account, Opportunity, Service Contract, and Billing Statement, and stays after the load.

**Rationale.** Option 3 is how people do this when they haven't done it before, and it falls apart the moment a load has to be re-run — every ID changes and the mapping is worthless. Option 1 is tempting but shortsighted: this dataset will be reloaded several times during the build as objects change, and each reload needs the same anchor. Keeping the field also means the repo's seed data can be re-imported into a fresh org by anyone reviewing the project, which is the one-command deploy the README promises.

**Consequences.** Four objects carry a field with no business meaning, which needs explaining to anyone browsing the data model — hence the description on each one naming it a migration artifact. The fields are hidden from all page layouts and visible only to the admin. In a production migration these would typically be retained for exactly this reason and then cleaned up once the source system is decommissioned.

**Revisit if.** The org ever becomes the system of record with no upstream source, at which point the fields are dead weight.

**Decided by / date.** Zana Yocum, 2026-09-27.

---

## D-10 — Seed data loaded with the Salesforce CLI rather than Data Loader

**Context.** The plan called for Data Loader, the tool nearly every admin job description names. Partway through the load, relationships by External ID stopped resolving reliably through Data Loader's mapping dialog — one relationship wasn't exposed in the picker at all, and auto-match repeatedly mapped relationship columns to the plain lookup.

**Options considered.**

1. **Keep using Data Loader**, working around the mapping dialog one file at a time.
2. **Salesforce CLI bulk import** (`sf data import bulk`), which reads relationship references directly from the CSV header with no mapping step.
3. **Export Salesforce IDs and VLOOKUP them** into each child file, loading with plain IDs.

**Decision.** Option 2 for files 04 through 12. Files 01 and 02 had already loaded through Data Loader and stayed as they were.

**Rationale.** The CLI removes the step that kept failing. Headers name the relationship and the External ID, and the Bulk API resolves the parent at insert time — nothing to map, nothing to mis-map. It's also scriptable, so the whole load is reproducible from the repo, which Data Loader's GUI isn't. Option 3 works but needs a spreadsheet round trip per file and breaks every time the parent data reloads.

**Consequences.** CSV headers must be exact API names and use dot notation for relationships (`Account__r.Legacy_Id__c`), which differs from Data Loader's colon syntax — the same file can't serve both tools. PowerShell's `>` redirect produces files the Bulk API rejects, so `--output-file` is required. Two upsert passes that needed an External ID relationship Data Loader wouldn't expose were deferred to flows, which is the better design regardless.

**Revisit if.** A load needs field mapping the source headers can't express, or someone without CLI access has to rerun it.

**Decided by / date.** Zana Yocum, 2026-09-29.
