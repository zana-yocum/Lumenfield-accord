# Persona checks — 15 minutes

These are the only scripts the admin can't prove, because they test what a role *can't* see. Log in as **Test Persona** (Setup → Users → Test Persona → Login, or a private window). Switch the role and permission set group between blocks. Write Pass/Fail next to each line, then hand it back and I'll fold it into the results.

## As Collections Rep (role Collections Rep, PSG Collections Rep)
1. **UAT-01** Open any Delinquent account in Collections Console. Collections section shows balance, DPD, bucket, priority, broken promises, primary contact. Open one of its Lease Payments: Method and External Reference are **not** shown. ☐
2. **UAT-05 step 4** Global search for **Patrick Boone Household** (Delinquent) — found. Then search for an account on the dashboard's *Current* bucket, e.g. **Regina Mundy Household** — **not found**. Reps reach accounts only through the Delinquent / Default Review sharing rule (D-08). ☐
3. **UAT-06** (possible since 2026-10-24: before DEF-08 was fixed, collections personas couldn't see this action) On a Delinquent account, Log Contact Attempt with no outcome → blocked. Log "Requested No Further Contact" → account shows Do Not Contact. (Untick it afterward as admin.) ☐
4. **UAT-12 negative** Reports → Collections → Default Review Timeliness: shows **0** cases. ☐
5. Reports open at all (Run Reports was just granted). ☐

## As Dispute Specialist (role Dispute Specialist, PSG Dispute Specialist)
6. **UAT-13 criterion 3** Create a $150 adjustment on an open dispute, Submit for Approval. In the approval request, there's **no Approve button** for you. (Approve or recall it as admin afterward.) ☐

## As Sales Rep (role Sales Rep, PSG Sales Rep)
7. **UAT-08 / 18** As admin, add Test Persona to an open dispute's Case Team as Sales Input. As Test Persona: case opens; **add a case comment** — does it save? ☐ (this is the open question)
8. Payment Method / External Reference not visible from the case's account. ☐
9. As admin, close the case. As Test Persona, reopen the link → no access. ☐
10. A dispute you're not on → no access. ☐

When done: set Test Persona back to Collections Rep.
