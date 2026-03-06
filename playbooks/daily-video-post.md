# Daily Video Post Package — 10 AM EST

## Purpose
Every day at 10 AM EST, deliver today's video posting package to #chloebot so Ramon can post it.

## Steps

1. **Read the tracking sheet** (`1l9VL3DCkz3MNe2kAGy6obqmEulvffmX1UdIGgVIx_YU`, tab "Content Tracker")
2. **Find today's rows** by matching the Date column (A) to today's date (YYYY-MM-DD, EST)
   - Each video has 4 rows (tiktok, IG reels, yt shorts, fb reels). The first row of each group has all the video info.
3. **If no row matches today** → send message to #chloebot: "No video scheduled for today."
4. **If today's file says "(pending from agency)"** → send message to #chloebot noting the video is still pending
5. **Build the posting package** from the first row of today's group:
   - Topic (column C)
   - Pillar (column E: Famous People or Isolation Protection)
   - File name (column F, naming: YYYYMMDD_S01_V##_FP_slug.mp4 or _PI_slug.mp4)
   - Full description with hashtags (column G)
   - Pinned comment text (column H)
   - Drive folder link: https://drive.google.com/drive/folders/1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf
6. **Send to #chloebot** (channel C0AD9AZ7R6F) formatted cleanly

## Format

```
📹 Today's Video — [DATE]

🎬 [TOPIC] ([PILLAR])
📁 File: [FILENAME]
🔗 Drive: https://drive.google.com/drive/folders/1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf

📝 Description:
[full description with hashtags]

📌 Pinned Comment:
[pinned comment text]
```

## After Posting
- When Ramon replies "posted" in the thread, mark all 4 platform rows for today's video as "posted" in the Post URL column (I)
- When Ramon shares specific post URLs, update the matching platform row
- Track any engagement numbers Ramon shares

## Sheet ID
`1l9VL3DCkz3MNe2kAGy6obqmEulvffmX1UdIGgVIx_YU`

## Drive Folder
`https://drive.google.com/drive/folders/1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf`

## Service Account
`openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
