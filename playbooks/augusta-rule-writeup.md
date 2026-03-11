# Augusta Rule Monthly Write-Up

## Purpose
Generate a monthly "Augusta Rule" meeting write-up summarizing all business activities from the previous month, then email it to Ramon.

## Schedule
1st of every month at 10:00 AM EST

## Format
The write-up MUST follow this exact format:

```
[Last day of previous month, e.g. "February 28, 2026"]

Monthly Meeting for The Goven House

Minutes:
[Narrative paragraphs - no bullet points, no headers, no markdown. Just flowing prose paragraphs covering everything that happened in the business that month.]
```

## Style Rules
- Plain narrative paragraphs only. No bullet points, no section headers, no bold text.
- Write in past tense, third person where appropriate ("Ramon", "we", "the team").
- Each major topic gets its own paragraph.
- Include specific numbers when available (revenue changes, metrics, counts).
- Conversational but professional tone - these are meeting minutes, not a report.
- No em dashes (Ramon's rule).
- Cover ALL business activities, not just All7s (wholesale, compliance, infrastructure, etc.)

## Data Sources
Read ALL memory files from the previous month:
1. `memory/YYYY-MM-DD.md` files for every day of the previous month
2. `MEMORY.md` for context on ongoing projects
3. Any relevant data from BigQuery/SQLite if revenue numbers are needed

## Topics to Cover (check memory for each)
- Revenue and financial performance (compare YoY if data available)
- Amazon operations (inventory, PPC, listings, compliance)
- All7s brand and Canasta initiatives
- Marketing (email campaigns, social media, content)
- SEO progress
- PR and media outreach
- Infrastructure and automation changes
- Product development or sourcing
- Any new tools, integrations, or systems built
- Wholesale operations
- eBay channel
- Any strategic decisions made

## Revenue Data
Query BigQuery or SQLite for previous month's revenue:
```bash
cd ~/amazon-data && python3 -c "
import sqlite3, datetime
conn = sqlite3.connect('amazon.db')
# Get previous month date range
today = datetime.date.today()
first_of_this_month = today.replace(day=1)
last_month_end = first_of_this_month - datetime.timedelta(days=1)
last_month_start = last_month_end.replace(day=1)
# Also get same month previous year for YoY
prev_year_start = last_month_start.replace(year=last_month_start.year - 1)
prev_year_end = last_month_end.replace(year=last_month_end.year - 1)
print(f'Period: {last_month_start} to {last_month_end}')
cur = conn.cursor()
cur.execute('SELECT SUM(ordered_product_sales) FROM sales_daily WHERE date BETWEEN ? AND ?', (str(last_month_start), str(last_month_end)))
current = cur.fetchone()[0]
cur.execute('SELECT SUM(ordered_product_sales) FROM sales_daily WHERE date BETWEEN ? AND ?', (str(prev_year_start), str(prev_year_end)))
previous = cur.fetchone()[0]
if current and previous:
    change = ((current - previous) / previous) * 100
    print(f'Revenue: \${current:,.2f} (vs \${previous:,.2f} last year, {change:+.1f}%)')
elif current:
    print(f'Revenue: \${current:,.2f}')
conn.close()
"
```

## Delivery
Email the completed write-up to ramon@goven.com using the email utility:
```bash
cd ~/amazon-data/collectors && python3 email_util.py \
  --to "ramon@goven.com" \
  --subject "Augusta Rule - [Month Year] Meeting Notes" \
  --body "<the write-up text>"
```

## Important
- This is a FOUNDATION draft. Ramon will add personal notes about supplier conversations, agency experiences, and personal reflections.
- Include everything from memory. Better to over-include than miss something.
- The write-up should read like the January example: natural, flowing meeting minutes.
