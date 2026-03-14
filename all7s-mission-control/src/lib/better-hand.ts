import fs from "node:fs/promises";
import path from "node:path";

export type BetterHandDraft = {
  id: string;
  subject: string;
  previewText: string;
  body: string;
  status: "pending" | "approved" | "rejected";
  createdAt: string;
  reviewedAt?: string;
};

export type ApprovedEntry = {
  id: string;
  subject: string;
  approvedAt: string;
  klaviyoCampaignId?: string;
};

const DRAFTS_FILE = "/Users/ramongonzalez/.openclaw/workspace/playbooks/better-hand-drafts.jsonl";
const APPROVED_FILE = "/Users/ramongonzalez/.openclaw/workspace/playbooks/better-hand-approved.jsonl";
const BACKUP_DIR = "/Users/ramongonzalez/.openclaw/workspace/playbooks/backups";

async function ensureFile(filePath: string) {
  try {
    await fs.access(filePath);
  } catch {
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.writeFile(filePath, "", "utf-8");
  }
}

function parseJsonl<T>(raw: string): T[] {
  return raw
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"))
    .map((l) => JSON.parse(l) as T);
}

export async function loadDrafts(): Promise<BetterHandDraft[]> {
  await ensureFile(DRAFTS_FILE);
  const raw = await fs.readFile(DRAFTS_FILE, "utf-8");
  return parseJsonl<BetterHandDraft>(raw);
}

async function backupAndSaveDrafts(drafts: BetterHandDraft[]): Promise<void> {
  await fs.mkdir(BACKUP_DIR, { recursive: true });
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\..+/, "").replace("T", "_");
  const backup = path.join(BACKUP_DIR, `better-hand-drafts_${stamp}.jsonl`);
  try {
    await fs.copyFile(DRAFTS_FILE, backup);
  } catch { /* first run */ }
  const content = drafts.map((d) => JSON.stringify(d)).join("\n") + "\n";
  await fs.writeFile(DRAFTS_FILE, content, "utf-8");
}

export async function updateDraft(
  id: string,
  status: "approved" | "rejected",
  subject?: string,
  previewText?: string,
  body?: string,
): Promise<BetterHandDraft | null> {
  const drafts = await loadDrafts();
  const draft = drafts.find((d) => d.id === id);
  if (!draft) return null;

  draft.status = status;
  draft.reviewedAt = new Date().toISOString();
  if (subject !== undefined) draft.subject = subject;
  if (previewText !== undefined) draft.previewText = previewText;
  if (body !== undefined) draft.body = body;

  await backupAndSaveDrafts(drafts);
  return draft;
}

export async function loadApprovedHistory(): Promise<ApprovedEntry[]> {
  await ensureFile(APPROVED_FILE);
  const raw = await fs.readFile(APPROVED_FILE, "utf-8");
  return parseJsonl<ApprovedEntry>(raw);
}

export async function addToApprovedHistory(entry: ApprovedEntry): Promise<void> {
  await ensureFile(APPROVED_FILE);
  await fs.appendFile(APPROVED_FILE, JSON.stringify(entry) + "\n", "utf-8");
}

function loadEnvVar(key: string): string | undefined {
  try {
    const raw = require("node:fs").readFileSync("/Users/ramongonzalez/amazon-data/.env", "utf-8");
    for (const line of raw.split("\n")) {
      const trimmed = line.trim();
      if (trimmed.startsWith("#") || !trimmed.includes("=")) continue;
      const eqIdx = trimmed.indexOf("=");
      const k = trimmed.slice(0, eqIdx).trim();
      const v = trimmed.slice(eqIdx + 1).trim();
      if (k === key) return v;
    }
  } catch { /* */ }
  return undefined;
}

const PS_STATE_FILE = "/Users/ramongonzalez/.openclaw/workspace/playbooks/better-hand-ps-state.json";

export async function getNextPS(): Promise<{ type: string; text: string }> {
  const fsSync = require("node:fs");
  const raw = fsSync.readFileSync(PS_STATE_FILE, "utf-8");
  const state = JSON.parse(raw);
  const idx = state.nextIndex ?? 0;
  const type = state.rotation[idx % state.rotation.length];
  const text = state.templates[type];
  return { type, text };
}

export async function advancePSRotation(): Promise<void> {
  const fsSync = require("node:fs");
  const raw = fsSync.readFileSync(PS_STATE_FILE, "utf-8");
  const state = JSON.parse(raw);
  state.nextIndex = ((state.nextIndex ?? 0) + 1) % state.rotation.length;
  fsSync.writeFileSync(PS_STATE_FILE, JSON.stringify(state, null, 2), "utf-8");
}

async function createKlaviyoTemplate(name: string, bodyText: string, apiKey: string): Promise<string> {
  // Wrap plain text body in minimal HTML for email clients
  // Georgia 20px, 1.5 line height per deliverability rules
  const htmlBody = `<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; font-size: 20px; line-height: 1.5; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
${bodyText.split("\n").map((line) => {
    if (!line.trim()) return "<br>";
    return `<p style="margin: 0 0 16px 0;">${line}</p>`;
  }).join("\n")}
</body></html>`;

  const payload = {
    data: {
      type: "template",
      attributes: {
        name,
        editor_type: "CODE",
        html: htmlBody,
        text: bodyText,
      },
    },
  };

  const res = await fetch("https://a.klaviyo.com/api/templates/", {
    method: "POST",
    headers: {
      Authorization: `Klaviyo-API-Key ${apiKey}`,
      revision: "2025-01-15",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Klaviyo template creation failed ${res.status}: ${text}`);
  }

  const data = await res.json();
  return data?.data?.id;
}

async function assignTemplateToMessage(messageId: string, templateId: string, apiKey: string): Promise<void> {
  const payload = {
    data: {
      type: "campaign-message",
      id: messageId,
      relationships: {
        template: {
          data: { type: "template", id: templateId },
        },
      },
    },
  };

  const res = await fetch("https://a.klaviyo.com/api/campaign-message-assign-template/", {
    method: "POST",
    headers: {
      Authorization: `Klaviyo-API-Key ${apiKey}`,
      revision: "2025-01-15",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Klaviyo template assignment failed ${res.status}: ${text}`);
  }
}

export async function createKlaviyoCampaign(subject: string, emailSubject?: string, previewText?: string, bodyText?: string): Promise<string | null> {
  const apiKey = loadEnvVar("KLAVIYO_API_KEY");
  if (!apiKey) throw new Error("KLAVIYO_API_KEY not found in .env");

  const listId = loadEnvVar("KLAVIYO_LIST_ID") || "TMu4eG";

  // Get sequential number from approved history (2 already sent before this system existed)
  const approved = await loadApprovedHistory();
  const campaignNumber = approved.length + 1;

  // Schedule for next Friday at 10 AM EST (15:00 UTC)
  const now = new Date();
  const daysUntilFriday = (5 - now.getUTCDay() + 7) % 7 || 7; // next Friday
  const friday = new Date(now);
  friday.setDate(friday.getDate() + daysUntilFriday);
  const sendDate = `${friday.getFullYear()}-${String(friday.getMonth() + 1).padStart(2, "0")}-${String(friday.getDate()).padStart(2, "0")}T15:00:00+00:00`;

  // Extract topic from subject (strip "The Better Hand: " prefix if present)
  const topic = subject.replace(/^The Better Hand:\s*/i, "").replace(/\s*🃏\s*$/, "");

  // Step 1: Create template with email body (if body provided)
  let templateId: string | undefined;
  if (bodyText) {
    templateId = await createKlaviyoTemplate(
      `Better Hand #${campaignNumber}: ${topic}`,
      bodyText,
      apiKey,
    );
  }

  // Step 2: Create campaign
  const payload = {
    data: {
      type: "campaign",
      attributes: {
        name: `The Better Hand #${campaignNumber}: ${topic}`,
        audiences: {
          included: [listId],
          excluded: [],
        },
        send_strategy: {
          method: "static" as const,
          datetime: sendDate,
        },
        "campaign-messages": {
          data: [{
            type: "campaign-message",
            attributes: {
              definition: {
                channel: "email",
                label: "default",
                content: {
                  subject: emailSubject || subject,
                  preview_text: previewText || "",
                  from_email: "hello@all7s.co",
                  from_label: "Ramon from All7s",
                },
              },
            },
          }],
        },
      },
    },
  };

  const res = await fetch("https://a.klaviyo.com/api/campaigns/", {
    method: "POST",
    headers: {
      Authorization: `Klaviyo-API-Key ${apiKey}`,
      revision: "2025-01-15",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Klaviyo API error ${res.status}: ${text}`);
  }

  const data = await res.json();
  const campaignId = data?.data?.id;

  // Step 3: Assign template to campaign message (if we created one)
  if (templateId && campaignId) {
    // Get the message ID from the campaign response
    const messages = data?.data?.attributes?.["campaign-messages"]?.data
      ?? data?.data?.relationships?.["campaign-messages"]?.data;
    const messageId = messages?.[0]?.id;

    if (messageId) {
      await assignTemplateToMessage(messageId, templateId, apiKey);
    } else {
      // Fallback: fetch the campaign's messages
      const msgRes = await fetch(`https://a.klaviyo.com/api/campaigns/${campaignId}/campaign-messages/`, {
        headers: {
          Authorization: `Klaviyo-API-Key ${apiKey}`,
          revision: "2025-01-15",
        },
      });
      if (msgRes.ok) {
        const msgData = await msgRes.json();
        const fallbackMsgId = msgData?.data?.[0]?.id;
        if (fallbackMsgId) {
          await assignTemplateToMessage(fallbackMsgId, templateId, apiKey);
        }
      }
    }
  }

  return campaignId ?? null;
}
