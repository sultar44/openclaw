# PR Opportunity Workflow (HARO + Source of Sources)

## Goal
Migrate PR lead triage from Google Apps Script into OpenClaw.

## Intake Sources
- `haro@helpareporter.com`
- `peter@sourceofsources.com`
- `peter@shankman.com`

## Trigger
Use Gmail Pub/Sub webhook (`openclaw webhooks gmail`) for new inbound emails from approved senders.

## Classification Lanes
Each parsed query is classified into one of three lanes:

1. **Product Placement Fit**
   - Roundups, gift guides, products for seniors, games, family activities, brain games.
2. **Thought Leadership / Story Fit**
   - Isolation after 50, friendship, routines/rituals, social connection, aging + community, cognitive activity.
3. **Ignore**
   - Irrelevant categories (crypto, politics, kids/babies focus, unrelated tech, non-fit geos if required).

## Scoring Rubric (0-100)
Score dimensions:
- Audience fit (women 50+, seniors, empty nesters): 0-30
- Topic fit (games/community/friendship/isolation/ritual): 0-30
- Outlet relevance/quality: 0-20
- Actionability (clear ask + deadline + contact): 0-20

Decision threshold:
- `>= 70`: Draft package
- `50-69`: Hold for review
- `< 50`: Ignore

## Output Model (No direct reporter outreach)
OpenClaw **does not email reporters directly**.

For each selected opportunity, send an email to `ramon@goven.com` containing:
- Reporter name + email
- Outlet
- Query summary + deadline
- Chosen lane (Product Placement or Thought Leadership)
- Suggested subject line
- **Email 1 draft** (forward-ready)
- **Follow-up draft (7 days later)**
- Why selected (short rationale)

## Follow-up State Logic
Track in sheet:
- `Draft Sent to Ramon`
- `Forwarded by Ramon`
- `Follow-up Draft Sent to Ramon`
- `Closed - No Response`
- `Closed - Responded`

Follow-up timing:
- If status is `Forwarded by Ramon` and no response marker after 7 days -> send follow-up draft package to Ramon.

## Sheet
Tracking sheet ID:
`1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc`

Preferred Sheets identity:
`openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`

## Email Tone Rules
- Avoid generic “product sample” language unless lane is Product Placement.
- For Thought Leadership lane, lead with expertise/story angle first; mention product only if additive.
- Keep concise, specific to the journalist request.

## Safety + Ops
- No hardcoded API keys in scripts.
- Use OpenClaw model for classification/drafting.
- Rotate compromised keys from legacy script (OpenAI + Slack webhook) if still active.
