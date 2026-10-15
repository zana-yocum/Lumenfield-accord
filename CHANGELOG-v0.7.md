## v0.7 — 2026-10-14 — Phase 8: Sales

Website inquiries become routed leads, a lead that matches an existing customer is flagged, and collections reps log every contact attempt with a structured outcome. One Could story was cut on purpose.

### Added
| Component | Type | Does | Stories |
|---|---|---|---|
| `web/lumenfield-solar-inquiry.html` | Web-to-lead form | Name, email, phone, service address, service area, inquiry detail. Posts to the org; custom fields mapped by field ID | US-16 |
| `VR_Lead_EmailOrPhoneRequired` | Validation rule | A lead with neither email nor phone is rejected, because there's no way to follow up | US-16 |
| `Accord Lead Routing` | Lead assignment rule | Every new lead, web or manual, goes to the Inbound Leads queue | US-16 |
| `Contact_Match_Email_Only` | Matching rule | Exact email match, lead to contact | US-16 |
| `Lead.Lead_Matches_Existing_Customer` | Duplicate rule | **Alert, not block.** Flags a lead whose email belongs to an existing customer, so web submissions still arrive | US-16 |
| `Contact_Outcome__c` | Activity field | Picklist on the global value set Contact Outcome | US-06 |
| `Account_Screen_LogContactAttempt` | Screen flow | Logs a completed task with an outcome. Promise Made goes straight into the promise screen; Requested No Further Contact sets Do Not Contact; Hardship or Bankruptcy sets Hardship Review | US-06, US-21 |
| `Account.Log_Contact_Attempt` | Quick action | Launches the flow from the Residential Agreement layout | US-06 |

### Changed
- Standard Lead Duplicate Rule deactivated. It blocked API and web-to-lead inserts outright; the custom rule alerts instead.
- Minimum Access profile given **Residential Agreement** as its default Account record type. This is the single exception to D-07: permission sets can grant record types but can't set a default, and lead conversion needs one.
- `Contact_Outcome__c` field-level security granted: System Administrator, Collections Core (edit), Dispute Management (read). New fields deployed from source get no access by default.

### Verified
- Web form submission → lead created with all custom fields populated → owned by Inbound Leads
- Submission with no email or phone → rejected, no lead
- Submission using an existing customer's email → lead created and flagged as a 100% match to that contact
- Log Contact Attempt is covered by UAT-06 (outcome required, Promise Made chains into the promise, Do Not Contact and Hardship flags)

### Cut on purpose
- **US-17, pipeline and forecast against quota (Could).** Collaborative Forecasts and quota loading add setup and screenshots without touching the lead-to-cash problem Accord exists to solve. Cutting the only Could story is a scope decision, recorded so it isn't mistaken for an oversight.
- **Quotes.** Not needed by any story. `PS_Sales_Core` has no Quote, Product or Price Book access.

### Lessons recorded
- The promise step has its own fault screen. `Promise_AfterSave_ApplyPolicy` can refuse a promise (a second active promise, for example), and without a fault path the rep would see a raw flow error instead of the reason.
- Activity custom fields live under `objects/Activity` in source, but field permissions reference them as `Task.Contact_Outcome__c`.
- Flows can't run assignment rules, so anything a flow creates must set its owner directly. The lead rule covers people and the web form; the default review flow sets its queue itself.

### Data
- One test lead entered through the web form with a real-looking personal email and phone was changed to fictional values (`example.com`, `555`). All data in this org stays invented.
