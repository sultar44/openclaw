"use client";

import { useEffect, useMemo, useState } from "react";
import { BUCKETS } from "@/lib/cron";

type JobView = {
  id: string;
  name: string;
  bucket: keyof typeof BUCKETS;
  scheduleText: string;
  status: { label: string; tone: string };
  state?: { nextRunAtMs?: number; lastRunAtMs?: number };
};

const TZ = "America/New_York";
const ROLLING_DAYS = 8; // today + next 7 days

function fmt(ms?: number) {
  if (!ms) return "—";
  return new Date(ms).toLocaleString("en-US", {
    timeZone: TZ,
    weekday: "short",
    month: "short",
    day: "2-digit",
    hour: "numeric",
    minute: "2-digit",
  });
}

function dayKeyET(d: Date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(d);

  const year = parts.find((p) => p.type === "year")?.value;
  const month = parts.find((p) => p.type === "month")?.value;
  const day = parts.find((p) => p.type === "day")?.value;

  return `${year}-${month}-${day}`;
}

function dayLabelET(d: Date) {
  return d.toLocaleDateString("en-US", {
    timeZone: TZ,
    weekday: "short",
    month: "numeric",
    day: "numeric",
  });
}

export default function CronPage() {
  const [jobs, setJobs] = useState<JobView[]>([]);

  useEffect(() => {
    fetch("/api/cron")
      .then((r) => r.json())
      .then((d) => setJobs(d.jobs ?? []));
  }, []);

  const rollingDays = useMemo(() => {
    const today = new Date();
    return Array.from({ length: ROLLING_DAYS }, (_, i) => {
      const d = new Date(today);
      d.setDate(today.getDate() + i);
      return {
        date: d,
        key: dayKeyET(d),
        label: dayLabelET(d),
      };
    });
  }, []);

  const jobsByDay = useMemo(() => {
    const map = new Map<string, JobView[]>();
    for (const job of jobs) {
      if (!job.state?.nextRunAtMs) continue;
      const key = dayKeyET(new Date(job.state.nextRunAtMs));
      const list = map.get(key) ?? [];
      list.push(job);
      map.set(key, list);
    }
    return map;
  }, [jobs]);

  return (
    <div>
      <h1>Cron Calendar</h1>
      <p className="muted">Rolling view: today + next 7 days ({TZ})</p>

      <div className="legend">
        {Object.entries(BUCKETS).map(([bucket, color]) => (
          <span key={bucket} className="legend-item">
            <i style={{ background: color }} /> {bucket}
          </span>
        ))}
      </div>

      <div className="rolling-grid">
        {rollingDays.map((day, idx) => {
          const dayJobs = jobsByDay.get(day.key) ?? [];

          return (
            <div key={day.key} className="day">
              <div className="day-num">{idx === 0 ? `Today · ${day.label}` : day.label}</div>
              <div className="day-jobs">
                {dayJobs.length === 0 ? (
                  <div className="mini">No jobs scheduled.</div>
                ) : (
                  dayJobs.map((job) => (
                    <article key={job.id} className="job-card" style={{ border: `1px solid ${BUCKETS[job.bucket]}` }}>
                      <div className="job-top">
                        <strong>{job.name}</strong>
                        <span className={`badge ${job.status.tone}`}>{job.status.label}</span>
                      </div>
                      <div className="mini">🕐 {job.scheduleText}</div>
                      <div className="mini">
                        <b>Next:</b> {fmt(job.state?.nextRunAtMs)}
                      </div>
                      <div className="mini">
                        <b>Last:</b> {fmt(job.state?.lastRunAtMs)}
                      </div>
                      <div className="mini id">ID: {job.id.slice(0, 8)}...</div>
                    </article>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
