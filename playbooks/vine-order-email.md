# Vine Order Email Processing

## Trigger
When you receive an email forwarded from `thehouse@goven.com` that is an Amazon order confirmation (subject contains "Ordered:" and from `auto-confirm@amazon.com`).

## What To Do

Parse the email body and add a new row to the **bottom** of the "Por Vender" tab in Google Sheet `1Q8XCCCmkll6olnxx-aBrtpAZDttu50phWFJO6hrAalk`.

### Column Mapping
| Column | Field | How to find it |
|--------|-------|----------------|
| A | Order ID | e.g. `111-8714949-7882616` from "Order #" in the email |
| B | Today's date | Format: `M/D/YYYY` (e.g. `2/24/2026`) |
| C | Unit price | Found after "Quantity: X" — it's the dollar amount (format as `$XX.XX`). Note: Amazon emails show price without decimal (e.g. `$29999` means `$299.99`) |
| D | (leave blank) | |
| E | (leave blank) | |
| F | ASIN | Found in product links like `/dp/B0GCFL2BTZ` |
| G | (leave blank) | |
| H | Brand | Look up the product on Amazon (`amazon.com/dp/{ASIN}`) and find the brand from the "Visit the X Store" byline |
| I | Product description | Very short (2-4 words). Examples: "wine chiller", "EV charger", "Cold Press Juicer". Look at existing values in column I for style guidance |

### Tools
- **Sheet access:** Use `gog sheets` with `--account openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
- **Find last row:** Get column A to find how many rows exist, then write to the next row
- **Write columns A-C:** Update range `Por Vender!A{row}:C{row}`
- **Write columns F, H-I:** Update range `Por Vender!F{row}:I{row}` (with blank G)
- **Brand lookup:** Use `curl` to fetch `amazon.com/dp/{ASIN}` and grep for `bylineInfo` to find brand name

### Delivery
After processing, announce to #chloe-logs (C0AELHCGW4F):
"📦 Vine order added: {Brand} - {short description} (Order #{order_id})"

### Skip If
- Email is NOT an Amazon order confirmation (no "Ordered:" in subject)
- Email is NOT forwarded from `thehouse@goven.com`
