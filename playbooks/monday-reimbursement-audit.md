# Monday Reimbursement Audit

**Schedule:** Every Monday, 9:00 AM EST
**Cron job:** Runs `monday_reimbursement_audit.py` then browser-checks IDR

## Three Checks

### 1. Shipment Discrepancies (API)
- Script pulls all CLOSED shipments from last 90 days
- Compares shipped vs received quantities
- Cross-references against already-tracked items in the sheet
- Only flags NEW untracked discrepancies

**Important:** API data can be stale. If discrepancies found, verify via browser before alerting.

### 2. Sizing Changes (Smart Canary)
- Baseline is STATIC (captured once, not re-pulled weekly)
- New ASINs auto-detected from inventory and added to baseline automatically
- Uses sp_fba_fees report from BQ as zero-cost canary (Amazon's own fee data)
- Falls back to Fee Estimate API for ASINs not in the report
- Only re-pulls full dimensions when a fee mismatch is detected
- Only alerts if fee impact > $0.25/unit
- Baseline stored in sheet tab `Sizing_Baseline`
- Change history stored in `Sizing_History` tab
- Manual add: `python3 collectors/sizing_monitor.py add <ASIN>`

### 3. IDR Portal Check (Browser)
- Navigate to: https://sellercentral.amazon.com/inventory-reimbursement/overview
- Check "Eligible for Claim" count
- If > 0: click through, note the ASINs and amounts
- Also check Warehouse Operations filter specifically

## Alert Routing
- **No issues on any check** → Single message to #chloelogs: "✅ Monday reimbursement audit: all clear (X shipments, Y ASINs, IDR 0 eligible)"
- **Issues on any check** → Detailed alert to #chloebot with sheet link
- **Mixed** → Confirmations to #chloelogs, issues to #chloebot

## Sheet
- ID: `1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs`
- Tabs: FBA_Reimbursements, Cases, Sizing_Baseline, Sizing_History

## Process for Filing Cases (TBD)
- Shipment discrepancies: Ramon will walk through process next time one is found
- Warehouse/Customer: Use IDR "Reimburse" button if eligible
- FBA fee overcharge: Calculate affected orders × overcharge amount (Ramon to walk through)
