# Persona checks — about 20 minutes

These are the checks the admin can't make, because they test what a role *can't* see or do. Each block runs as **Test Persona**, the one persona user, switched to a different role and permission set group between blocks. Write Pass or Fail next to each line, with anything that looked wrong, then hand it back to be folded into the results.

## Switching Test Persona between personas

Do this as yourself, before each block.

1. Gear icon → **Setup** → Quick Find `Users` → **Users** → click **Test Persona** (the name, not Login).
2. **Role:** click **Edit**, set **Role** to the block's role, **Save**.
3. **Group:** scroll to **Permission Set Group Assignments** → **Edit Assignments**. Move the old group to *Available* and the block's group to *Enabled*, then **Save**.
4. Back on the Users list, click **Login** next to Test Persona. When the block is done, top right → **Log out as Test Persona**.

## As Collections Rep (role Collections Rep, group Collections Rep)

Test Persona is set up this way already.

1. **UAT-01** In Collections Console, open a Delinquent account such as **Patrick Boone Household**. The Collections section shows the balances, days past due, bucket, priority score and broken promises, and Primary Contact is filled in above it. In **Billing Statements**, open a statement with a payment, then open the payment under **Lease Payments**: Method and External Reference are **not** shown. ☐
2. **DEF-09** Back on the account, click **Edit**. Account Status, High Value and Collection Hold Until are read-only. The layout allows editing them, so this is field-level security at work. Do Not Contact and Primary Contact can be changed. Click **Cancel**. ☐
3. **UAT-05 step 4 and DEF-10** Global search for **Patrick Boone Household** (Delinquent): found. Then search for **Regina Mundy Household** (Current, no disputes): **not found**. A rep reaches an account through its status (Delinquent, Hardship Review or Default Review, D-08), or read-only through a billing dispute on it. ☐
4. **UAT-06** On a Delinquent account, click **Log Contact Attempt** and finish with no outcome: blocked. Then log **Requested No Further Contact**: the account shows Do Not Contact. Afterwards, as yourself, untick Do Not Contact on that account. ☐
5. **UAT-12 negative** App Launcher → **Reports** → Collections → **Default Review Timeliness**: shows **0** cases, since reps can't see default reviews. ☐
6. Reports open at all (Run Reports, granted 2026-10-14). ☐

## As Dispute Specialist (role Dispute Specialist, group Dispute Specialist)

7. **UAT-13 criterion 3** On an open billing dispute, create a $150 adjustment and click **Submit for Approval**. In the approval request there's **no Approve button** for you. Afterwards, as yourself, approve it or recall it. ☐

## As Sales Rep (role Sales Rep, group Sales Rep)

8. **UAT-08 / 18** As yourself, add Test Persona to an open dispute's **Case Team** as **Sales Input**. As Test Persona: the case opens; **add a case comment**. Does it save? ☐ (this is the open question)
9. On that case, Payment Method and External Reference aren't visible anywhere. ☐
10. As yourself, close the case. As Test Persona, open the case link again: no access. ☐
11. A dispute Test Persona isn't on: no access. ☐

**When done:** switch Test Persona back to role **Collections Rep** and group **Collections Rep**.
