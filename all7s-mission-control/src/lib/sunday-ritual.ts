import fs from "node:fs/promises";
import path from "node:path";

export type TopicEntry = {
  topic: string;
  status: "pending" | "drafted" | "used" | "selected";
  added: string;
  brief: string;
  used_date?: string;
  email_subject?: string;
  email_preview?: string;
  email_body?: string;
  blog_status?: "pending" | "draft" | "published";
  blog_url?: string;
};

export type RitualLogEntry = {
  topic: string;
  sentAt: string;
  blogUrl?: string;
  klaviyoCampaignId?: string;
};

const QUEUE_FILE = "/Users/ramongonzalez/.openclaw/workspace/playbooks/sunday-ritual-topic-queue.jsonl";
const LOG_FILE = "/Users/ramongonzalez/.openclaw/workspace/playbooks/sunday-ritual-log.jsonl";

function parseJsonl<T>(raw: string): T[] {
  return raw
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"))
    .map((l) => JSON.parse(l) as T);
}

async function ensureFile(filePath: string) {
  try {
    await fs.access(filePath);
  } catch {
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.writeFile(filePath, "", "utf-8");
  }
}

export async function loadTopics(): Promise<TopicEntry[]> {
  await ensureFile(QUEUE_FILE);
  const raw = await fs.readFile(QUEUE_FILE, "utf-8");
  return parseJsonl<TopicEntry>(raw);
}

export async function saveTopics(topics: TopicEntry[]): Promise<void> {
  const content = topics.map((t) => JSON.stringify(t)).join("\n") + "\n";
  await fs.writeFile(QUEUE_FILE, content, "utf-8");
}

export async function loadLog(): Promise<RitualLogEntry[]> {
  await ensureFile(LOG_FILE);
  const raw = await fs.readFile(LOG_FILE, "utf-8");
  return parseJsonl<RitualLogEntry>(raw);
}

export async function selectTopic(topicName: string): Promise<TopicEntry | null> {
  const topics = await loadTopics();
  const topic = topics.find((t) => t.topic === topicName && t.status === "pending");
  if (!topic) return null;
  topic.status = "selected";
  await saveTopics(topics);
  return topic;
}
