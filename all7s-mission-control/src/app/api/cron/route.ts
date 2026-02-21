import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import { NextResponse } from "next/server";
import { categorizeJob, formatSchedule, statusInfo, type CronJob } from "@/lib/cron";

export async function GET() {
  try {
    const jobsPath = path.join(homedir(), ".openclaw", "cron", "jobs.json");
    const raw = await readFile(jobsPath, "utf8");
    const parsed = JSON.parse(raw) as { jobs?: CronJob[] };

    const jobs = (parsed.jobs ?? []).map((job) => ({
      ...job,
      bucket: categorizeJob(job.name ?? ""),
      scheduleText: formatSchedule(job),
      status: statusInfo(job),
    }));

    return NextResponse.json({ jobs, fetchedAt: Date.now() });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to load cron jobs", details: String(error) },
      { status: 500 },
    );
  }
}
