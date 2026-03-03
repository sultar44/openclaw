# FBM Sale Email Processing

## Trigger
When you receive an email forwarded to chloemercer32@gmail.com where the subject contains "Sold, ship now" (Amazon FBM sale notification).

## What To Do

1. **Parse the SKU** from the subject line: `Sold, ship now: {SKU}` 
   - Strip any `-MF` or `-FM` suffix from the SKU
2. **Parse the quantity** from the email body: look for `Quantity:` followed by a number (default to 1 if not found)
3. **Look up the SKU** in Google Sheet `1HFeDZ0vG3Jb8oi-LY2AsB5JdkogOoq5Qifk-a_03JCM`, tab "MC"
   - Column B = Caja number
   - Column C = Modelo (SKU)
   - Match the parsed SKU against column C to find the Caja
4. **Post to #ops_fbm** (C08TU971Z2P):
   ```
   Nueva venta: {SKU} - Cantidad: {quantity} - Caja #{caja}
   ```

### Tools
- **Sheet access:** Use service account credentials at `~/amazon-data/google_sheets_credentials.json`
- **Sheet ID:** `1HFeDZ0vG3Jb8oi-LY2AsB5JdkogOoq5Qifk-a_03JCM`
- **Tab:** `MC` — read columns B:C to build SKU→Caja map

### Delivery
Post the sale notification to **#ops_fbm** (C08TU971Z2P) via Slack.

### Skip If
- Email subject does NOT contain "Sold, ship now"
- SKU not found in the MC sheet (log a warning instead)

### Logging
- **Success:** Post ONLY to #ops_fbm. Do NOT post success summaries to #chloelogs or #chloebot.
- **Failure:** Post to #chloebot (C0AD9AZ7R6F) only.

### Post-Processing: Archive Email
After successfully processing the FBM sale email, **archive it** from Chloe's inbox:
```
gog gmail modify <messageId> --remove-labels INBOX
```
This keeps the inbox clean so Ramon can spot unprocessed emails (failure detection).

### Error Handling
- If SKU not found in sheet → post to #chloebot: "⚠️ FBM sale for unknown SKU: {SKU}"
- If parsing fails → post to #chloebot: "⚠️ Could not parse FBM sale email: {subject}"
