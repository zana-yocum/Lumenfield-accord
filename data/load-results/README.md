# Load results — Phase 5

Two Bulk API result files, kept as evidence for the load-failure table in `docs/data-plan.md`, where every failure was diagnosed from its job's error file.

| Job | Object | Failed | Error in the file | Cause and fix (from `data-plan.md`) |
|---|---|---|---|---|
| `750aj00001ExUr8AAF` | Opportunity | 69 of 100 | `INVALID_OR_NULL_FOR_RESTRICTED_PICKLIST` on Concession Offered | The org's picklist value was stored as `No,` with a trailing comma, so the CSV's `No` didn't match. Corrected in Setup |
| `750aj00001Ezc7rAAB` | Lead | 30 of 30 | `DUPLICATES_DETECTED` | Standard duplicate rules ship active, and API inserts fail rather than prompt. The leads had loaded on an earlier attempt |

The `-success-records.csv` files are the rows that loaded in the same jobs. All names, addresses and emails are invented (`example.com`).
