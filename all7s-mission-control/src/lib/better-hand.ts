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

export async function createKlaviyoCampaign(subject: string): Promise<string | null> {
  const apiKey = loadEnvVar("KLAVIYO_API_KEY");
  if (!apiKey) throw new Error("KLAVIYO_API_KEY not found in .env");

  const listId = loadEnvVar("KLAVIYO_LIST_ID");

  const payload = {
    data: {
      type: "campaign",
      attributes: {
        name: `The Better Hand: ${subject}`,
        audiences: {
          included: listId ? [listId] : [],
          excluded: [],
        },
        send_strategy: {
          method: "static" as const,
          options_static: { datetime: null },
        },
        campaign_messages: [{ channel: "email", label: "default" }],
      },
    },
  };

  const res = await fetch("https://a.klaviyo.com/api/campaigns/", {
    method: "POST",
    headers: {
      Authorization: `Klaviyo-API-Key ${apiKey}`,
      revision: "2024-10-15",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Klaviyo API error ${res.status}: ${text}`);
  }

  const data = await res.json();
  return data?.data?.id ?? null;
}
