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
   - Full description with hashtags (column G) — **MAX 5 HASHTAGS**
   - Pinned comment text (column H) — same for all platforms
   - Drive folder link: https://drive.google.com/drive/folders/1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf
6. **Send to #chloebot** (channel C0AD9AZ7R6F) as SEPARATE messages for easy copy-paste

## Message Format (SEPARATE MESSAGES — one per copyable block)

### Message 1: Overview
```
📹 Today's Video — [DATE]

🎬 [TOPIC] ([PILLAR])
📁 File: [FILENAME]
🔗 Drive: https://drive.google.com/drive/folders/1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf
```

### Message 2: Description (copy-ready)
Just the raw description text with hashtags. Nothing else. No label, no emoji prefix.
```
[full description text with hashtags — max 5 hashtags]
```

### Message 3: Pinned Comment (copy-ready, all platforms)
Just the raw pinned comment text. Nothing else. No label, no emoji prefix.
```
[pinned comment text]
```

**Why separate messages:** Ramon copies each block directly to the platform. Each message should contain ONLY the text to paste — no headers, labels, or formatting around it.

## After Ramon Says "Done" / "Posted"
1. Mark all 4 platform rows for today's video as "posted" in the Post URL column (J)
2. **Move the video file** from "To Post" folder (`1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf`) to "Posted" folder (`16X4cz-UYwEKg4uB_pcE26ZUVgpu3_tva`) in Google Drive
3. When Ramon shares specific post URLs, update the matching platform row

## Rules
- **Max 5 hashtags** per description (never more)
- **Single pinned comment** for ALL platforms: "Comment START" version (no more "DM me START" variant)
- **Description CTA:** Include "comment START for..." line in all descriptions (no "follow @playall7s")
- **Comment automation:** ManyChat (IG/FB), TikTok native automation (TikTok), manual reply (YouTube)
- Each copyable text block must be its own standalone Slack message

## Sheet Columns
A: Date | B: Video # | C: Topic | D: Platform | E: Pillar | F: File Name | G: Description | H: Pinned Comment | I: (unused) | J: Post URL | K: Views 24h | L: Views 48h | M: Views 7d | N: Likes | O: Comments | P: Shares

## Sheet ID
`1l9VL3DCkz3MNe2kAGy6obqmEulvffmX1UdIGgVIx_YU`

## Drive Folders
- **To Post:** `1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf`
- **Posted:** `16X4cz-UYwEKg4uB_pcE26ZUVgpu3_tva`

## Service Account
`openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
