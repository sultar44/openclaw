import fs from "node:fs/promises";
import path from "node:path";

export type StrategyEntry = {
  id: string;
  source?: string;
  status?: string;
  post_date?: string;
  question?: string;
  title?: string;
  recommendation?: string;
  strategy?: string;
  tags?: string[];
  reviewed_at?: string | null;
};

export const STRATEGY_FILE = "/Users/ramongonzalez/.openclaw/workspace/canasta-rules/strategy.jsonl";
export const BACKUP_DIR = "/Users/ramongonzalez/.openclaw/workspace/canasta-rules/backups";

export async function loadEntries(): Promise<StrategyEntry[]> {
  const raw = await fs.readFile(STRATEGY_FILE, "utf-8");
  return raw
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line) as StrategyEntry);
}

export async function backupAndSave(entries: StrategyEntry[]): Promise<void> {
  await fs.mkdir(BACKUP_DIR, { recursive: true });

  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\..+/, "").replace("T", "_");
  const backup = path.join(BACKUP_DIR, `strategy_${stamp}.jsonl`);

  try {
    await fs.copyFile(STRATEGY_FILE, backup);
  } catch {
    // file might not exist on first run
  }

  const content = entries.map((e) => JSON.stringify(e)).join("\n") + "\n";
  await fs.writeFile(STRATEGY_FILE, content, "utf-8");
}

export async function updateEntry(
  entryId: string,
  newStatus: "approved" | "rejected",
  question?: string,
  answer?: string,
): Promise<void> {
  const entries = await loadEntries();

  for (const e of entries) {
    if (e.id !== entryId) continue;
    e.status = newStatus;
    e.reviewed_at = new Date().toISOString();

    if (question !== undefined) {
      if ("question" in e) e.question = question;
      else e.title = question;
    }

    if (answer !== undefined) {
      e.recommendation = answer;
      e.strategy = answer;
    }
    break;
  }

  await backupAndSave(entries);
}
