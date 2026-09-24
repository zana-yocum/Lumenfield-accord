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
