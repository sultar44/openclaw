export type CronJob = {
  id: string;
  name: string;
  enabled: boolean;
  schedule?: {
    kind?: string;
    expr?: string;
    tz?: string;
  };
  state?: {
    nextRunAtMs?: number;
    lastRunAtMs?: number;
    lastStatus?: string;
  };
};

export const BUCKETS = {
  "Data Collection": "#3b82f6",
  "Monitoring & Alerts": "#f59e0b",
  "Content & Reports": "#8b5cf6",
  "Retry Jobs": "#ef4444",
} as const;

export type Bucket = keyof typeof BUCKETS;

export function categorizeJob(name: string): Bucket {
  const n = name.toLowerCase();

  if (n.includes("retry")) return "Retry Jobs";
  if (["collection", "sync", "pricing", "ppc", "rank", "amazon", "sqp"].some((x) => n.includes(x))) {
    return "Data Collection";
  }
  if (["monitor", "bsr", "listing", "gsc"].some((x) => n.includes(x))) {
    return "Monitoring & Alerts";
  }
  if (["report", "strategy", "scraper", "facebook"].some((x) => n.includes(x))) {
    return "Content & Reports";
  }

  return "Data Collection";
}

export function formatSchedule(job: CronJob): string {
  const schedule = job.schedule ?? {};
  if (schedule.kind !== "cron") return schedule.expr ?? "Unknown";

  const expr = schedule.expr ?? "";
  const parts = expr.split(" ");
  if (parts.length !== 5) return expr || "Unknown";

  const [minute, hour, dom, _month, dow] = parts;

  const formatHour = (h: string) => {
    const num = Number(h);
    if (Number.isNaN(num)) return `${h}:${minute}`;
    const ampm = num < 12 ? "AM" : "PM";
    const h12 = num % 12 === 0 ? 12 : num % 12;
    return `${h12}:${minute.padStart(2, "0")} ${ampm}`;
  };

  const timeStr = hour.includes(",")
    ? hour
        .split(",")
        .map((h) => formatHour(h).replace(":00 ", ""))
        .join(", ")
    : formatHour(hour);

  let dayStr = "Daily";
  if (dow === "*" && dom === "*") dayStr = "Daily";
  else if (dow === "1") dayStr = "Monday";
  else if (dow === "0,3") dayStr = "Sun & Wed";
  else if (dow === "2,3,4,5") dayStr = "Tue-Fri";
  else if (dow === "1,2,3") dayStr = "Mon-Wed";
  else if (dow !== "*") {
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    dayStr = dow
      .split(",")
      .map((d) => days[Number(d)] ?? d)
      .join(", ");
  }

  return `${dayStr} @ ${timeStr}`;
}

export function statusInfo(job: CronJob): { label: string; tone: string } {
  const enabled = job.enabled ?? true;
  const status = job.state?.lastStatus ?? "unknown";

  if (!enabled) return { label: "Disabled", tone: "disabled" };
  if (status === "ok") return { label: "✓ OK", tone: "success" };
  if (status === "error") return { label: "✗ Error", tone: "error" };
  return { label: "Pending", tone: "pending" };
}
