# Billing data regeneration / re-age runbook

Rebuilds Billing Statements, Payments, Promises to Pay and Adjustments for the 88
Residential Agreement accounts, anchored to a given date, so the delinquency mix
matches `docs/data-plan.md` on the day it's loaded. Accounts, contacts,
opportunities, commitments and service contracts are kept; service contract
activation dates and account statuses are updated to match.

Generated 2026-10-08: 632 statements, 545 payments, 60 promises, 12 adjustments.
Buckets: Current 52 · 1–30 14 · 31–60 10 · 61–90 7 · 90+ 5.

## Why this exists

The original seed's statement series ended months or a year before the load,
so unpaid statements aged past 90 days and 29 of 30 delinquent accounts landed
in 90+. Days Past Due counts from TODAY(), so any fixed dataset keeps aging;
rerun this before UAT or a demo.

## Run (PowerShell, from the repo root)

Delete in child-to-parent order. Payments are master-detail to statements, so
deleting statements removes them.

    sf data query -o lumenfield -q "SELECT Id FROM Adjustment__c" -r csv --output-file data\regen\del_adjustments.csv
    sf data delete bulk -o lumenfield -s Adjustment__c -f data\regen\del_adjustments.csv -w 10
    sf data query -o lumenfield -q "SELECT Id FROM Promise_to_Pay__c" -r csv --output-file data\regen\del_promises.csv
    sf data delete bulk -o lumenfield -s Promise_to_Pay__c -f data\regen\del_promises.csv -w 10
    sf data query -o lumenfield -q "SELECT Id FROM Billing_Statement__c" -r csv --output-file data\regen\del_statements.csv
    sf data delete bulk -o lumenfield -s Billing_Statement__c -f data\regen\del_statements.csv -w 10

Load, parents before children:

    sf data import bulk -o lumenfield -s Billing_Statement__c -f data\regen\01_statements.csv --line-ending LF -w 10
    sf data import bulk -o lumenfield -s Payment__c -f data\regen\02_payments.csv --line-ending LF -w 10
    sf data import bulk -o lumenfield -s Promise_to_Pay__c -f data\regen\03_promises.csv --line-ending LF -w 10
    sf data import bulk -o lumenfield -s Adjustment__c -f data\regen\04_adjustments.csv --line-ending LF -w 10
    sf data upsert bulk -o lumenfield -s ServiceContract -f data\regen\05_service_contracts.csv -i Legacy_Id__c --line-ending LF -w 10
    sf data upsert bulk -o lumenfield -s Account -f data\regen\06_accounts.csv -i Legacy_Id__c --line-ending LF -w 10

`--line-ending LF` is required on Windows: the CSVs use LF line endings and the CLI defaults to CRLF there.

Then empty the Org Recycle Bin so the old records stop counting against anything.

## To re-age later

    python data\regen\generate_billing.py 2027-01-15 data\regen

then run the same commands. The `del_*.csv` files are scratch; don't commit them.
