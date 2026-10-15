## v1.0 — 2026-10-14 — Phase 10: Release

Accord is feature-complete: 20 of 21 stories delivered, one cut on purpose. This release adds the documentation that turns the build into something another admin could test, run and support. Outside UAT and the walkthrough video are the two items that need people and time, and are tracked in `open-items.md`.

### Added — docs
- `docs/case-study.md` — the project in ten minutes: problem, decisions, what went wrong, results
- `docs/uat-scripts.md` — 21 scripts, one per story, each with its negative case and a sign-off table
- `docs/rca-balance-formula.md` — root cause analysis of the $0-balance formula, including why four existing checks missed it
- `docs/quick-reference.md` — one page per role
- `README.md` — rewritten as the front door: results, what's in the org, how to explore, known limits
- `docs/requirements.md` — traceability complete; US-17 marked cut with the reason
- `docs/data-plan.md` — after numbers (every target met), billing regeneration, household rename, control-total check added to load verification
- Security model additions: case sharing, role cleanup, case teams, activity access, folder sharing, D-07 exceptions, admin self-approval

### Added — manifests
- `manifest/phase9-retrieve.xml` — everything built through the API in Phases 7–9 that isn't in source yet
- `manifest/cleanup-fields/` — destructive deploy: 24 Developer Edition sample fields and the sample Delivery Status link
- `manifest/cleanup-layouts/` — destructive deploy: 6 sample Account and Case layouts

### Release checks
| Check | Result |
|---|---|
| All 11 flows active | ✓ |
| 12 validation rules active, each with a description | ✓ |
| Data Quality dashboard | 0 on every metric |
| Collections Supervisor dashboard refreshes, all 10 components return data | ✓ |
| Standard Lead and Contact duplicate rules inactive; custom alert rules active | ✓ |
| Collections Console opens on Collections Home | ✓ |
| No real-looking personal data in the org | ✓ (one web-form test lead corrected) |

### Still open, by design
- **Outside UAT** with 3–5 testers who didn't build it
- **Walkthrough video**
- **Automatic Default Review.** Two accounts reach 90 days past due around October 18–19. The nightly flow should open their reviews on its own — the first "on time" review on the dashboard.
