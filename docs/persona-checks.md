# Persona checks

These test what a role *can't* see or do, which an admin login can't prove. Most were checked on 2026-10-26 through the API as Test Persona, the one persona user (results doc, *Persona checks through the API*). What's left is optional: running the contact-attempt outcomes in the console as a rep, which the flow's definition already confirms. About 5 minutes.

## Left for the console (optional, about 5 minutes)

Test Persona is already set up as a Collections Rep (role Collections Rep, group Collections Rep).

1. As yourself: gear icon → **Setup** → Quick Find `Users` → **Users** → click **Login** next to **Test Persona**.
2. App Launcher → **Collections Console** → open a Delinquent account such as **Patrick Boone Household**.
3. **UAT-06 step 5:** click **Log Contact Attempt** and click **Next** with no outcome: blocked, and asked to pick one. ☐
4. **UAT-06 step 3:** log **Requested No Further Contact**: the account shows Do Not Contact. ☐
5. **UAT-06 step 4:** on another Delinquent account, log **Hardship or Bankruptcy Mentioned**: Account Status becomes Hardship Review. ☐
6. **UAT-06 step 2:** on a third Delinquent account with no active promise, log **Promise Made**: the promise screen follows, and the promise saves. ☐
7. Top right → **Log out as Test Persona**. Then, as yourself, put back what the test changed: untick Do Not Contact on the first account, set the second account's status back to Delinquent, and cancel the test promise (Status → Cancelled). Tell Claude which accounts you used.

Write Pass or Fail next to each line, with anything that looked wrong.

## Done through the API (2026-10-26)

| Step in the original checks | Result | How |
|---|---|---|
| **UAT-01** Collections section, related lists, payment fields hidden | Pass | Field access and layout assignment for Test Persona; a current account shows $0, 0 days and Current |
| **DEF-09** Account Status, High Value and Collection Hold Until read-only; Do Not Contact and Primary Contact editable | Pass | `UserFieldAccess` |
| **UAT-05 step 4 and DEF-10** a Delinquent account found, a Current account with no dispute not found | Pass | `UserRecordAccess`: 40 of 100 accounts readable, the 34 in collections editable |
| **UAT-06 step 1** Log Contact Attempt runs for a rep | Pass | Steward's hand check logged a Left Voicemail attempt as Test Persona |
| **UAT-12** reps see no default reviews | Pass | None of the 7 readable; report folder and Run Reports in place |
| Reports open for reps | Pass | Run Reports in the rep group; the Collections folder is shared with VP Customer Operations and subordinates |
| **UAT-13 criterion 3** a specialist can't approve their own credit | Pass (configuration) | Every request goes to one named approver, the supervisor |
| **UAT-08 / 18** a Sales Input team member adds a case comment | **Fail: DEF-11** | Refused in user mode as Test Persona: a comment needs edit access to the case. A feed post saved |
| Sales rep sees no payment detail | Pass | No access to Lease Payment, Billing Statement or Adjustment in the Sales Rep group |
| Sales rep loses access at close, and never sees a dispute they're not on | Pass | Phase 7 test (team removed at close) and Phase 6 negative test |

To check these by hand later (for outside UAT, say), the scripts are in `docs/uat-scripts.md`. Switching Test Persona between personas: on the user record, **Edit** the role, then **Permission Set Group Assignments** → **Edit Assignments** to swap the group. Switch back to Collections Rep afterwards.
