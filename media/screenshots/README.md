# Screenshots

Taken in the org as each phase closed. Names start with the phase so the folder sorts in build order (`docs/conventions.md`). Each one records the org on the day it was taken; what changed later is in `CHANGELOG.md`.

| Screenshot | What it shows | Written up in |
|---|---|---|
| [phase01-business-hours-holidays.png](phase01-business-hours-holidays.png) | Thanksgiving as a recurring holiday on Lumenfield Support Hours, the calendar the dispute SLA runs on | `docs/brief.md`, CHANGELOG v0.5 |
| [phase03-schema-full-model.png](phase03-schema-full-model.png) | Schema Builder: the custom objects around Account, Opportunity, Service Contract, Contact and Case | `docs/data-model.md` |
| [phase03-schema-custom-objects.png](phase03-schema-custom-objects.png) | Schema Builder: the five custom objects and their relationships | `docs/data-model.md` |
| [phase03-commitment-master-detail-opportunity.png](phase03-commitment-master-detail-opportunity.png) | Commitment as a master-detail child of Opportunity (D-02) | `docs/decision-log.md` |
| [phase03-account-rollup-past-due-balance.png](phase03-account-rollup-past-due-balance.png) | The account's Past Due Balance roll-up | `docs/data-dictionary.md` |
| [phase03-billing-statement-rollup-amount-paid.png](phase03-billing-statement-rollup-amount-paid.png) | The statement's Amount Paid roll-up from Lease Payments | `docs/data-dictionary.md` |
| [phase03-promise-out-of-policy-formula.png](phase03-promise-out-of-policy-formula.png) | The Out of Policy formula on Promise to Pay | `docs/data-dictionary.md` |
| [phase03-policy-settings-custom-metadata.png](phase03-policy-settings-custom-metadata.png) | The nine policy settings as custom metadata records, each citing its user story | `docs/data-dictionary.md` |
| [phase04-org-wide-defaults.png](phase04-org-wide-defaults.png) | Org-wide defaults: Private for Lead, Account, Opportunity and Case; Contact controlled by parent | `docs/security-model.md` |
| [phase04-role-hierarchy.png](phase04-role-hierarchy.png) | The role hierarchy: the collections chain under VP Customer Operations, the sales chain under VP Sales | `docs/security-model.md` |
| [phase04-permission-set-group-supervisor.png](phase04-permission-set-group-supervisor.png) | The Collections Supervisor group as first built, with its five permission sets | `docs/security-model.md` |
| [phase04-muting-permission-set.png](phase04-muting-permission-set.png) | The Collections Rep group as first built: Collections Core, with Promise to Pay delete muted | `docs/security-model.md` |
| [phase04-health-check-baseline.png](phase04-health-check-baseline.png) | Security Health Check before remediation: 66%, Poor | `docs/security-model.md` |
| [phase04-health-check-after.png](phase04-health-check-after.png) | Security Health Check after remediation: 96%, Excellent. The one Critical left is trusted IP ranges, on purpose | `docs/security-model.md` |
| [phase05-data-quality-dashboard-before.png](phase05-data-quality-dashboard-before.png) | The data quality dashboard on Oct 1, before cleanup: duplicate contacts, 3 accounts invisible to collections, 88 with no one to contact, 2 statement date errors, 16 contacts with no role | `docs/data-plan.md` |
| [phase05-data-quality-dashboard-after.png](phase05-data-quality-dashboard-after.png) | The same dashboard on Oct 3, after cleanup: no duplicates, no date errors, no missing roles. The other two tiles were fixed by Phase 7's automation (status flow, primary contact) | `docs/data-plan.md`, CHANGELOG v0.6 |
| [phase05-duplicate-alert-in-action.png](phase05-duplicate-alert-in-action.png) | The contact duplicate rule flagging a potential duplicate on Melissa Sanders | `docs/data-plan.md` |
| [phase05-validation-rule-in-action.png](phase05-validation-rule-in-action.png) | `VR_Statement_DueAfterStatementDate` blocking a due date before the statement date | `docs/data-plan.md` |
| [phase06-collections-console.png](phase06-collections-console.png) | Test Persona in the Collections Console on the default home page, before Phase 9 replaced it with the Collections home page | CHANGELOG v0.5, v0.8 |

Since these were taken: the delete on Promise to Pay was removed from every persona (OBS-01, v1.0.1), and the supervisor group gained Steward's permission sets and `PS_Collections_Overrides` (v1.0.2).
