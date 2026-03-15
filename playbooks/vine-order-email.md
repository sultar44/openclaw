# Vine Order Email Processing

## Trigger
When you receive an email forwarded from `thehouse@goven.com` that is an Amazon order confirmation (subject contains "Ordered:" and from `auto-confirm@amazon.com`).

## What To Do

**Run the script. Do NOT try to parse or write to the sheet yourself.**

```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/vine_order_processor.py --message-id {MESSAGE_ID}
```

The script handles everything:
- Reads full HTML email body via Gmail API
- Parses order ID, ASIN, and price (handles Amazon's no-decimal format)
- Looks up brand name
- Finds next empty row and writes each column individually (no concatenation bugs)
- Checks for duplicates
- Sends notification to #chloelogs
- Archives the email

To scan all unprocessed vine emails in inbox:
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/vine_order_processor.py --scan
```

### Skip If
- Email is NOT an Amazon order confirmation (no "Ordered:" in subject)
- Email is NOT forwarded from `thehouse@goven.com`
