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

function fmt(ms?: number) {
  if (!ms) return "—";
  return new Date(ms).toLocaleString("en-US", {
    timeZone: "America/New_York",
    weekday: "short",
    month: "short",
    day: "2-digit",
    hour: "numeric",
    minute: "2-digit",
  });
}

function monthLabel(d: Date) {
  return d.toLocaleString("en-US", { month: "long", year: "numeric", timeZone: "America/New_York" });
}

export default function CronPage() {
  const [jobs, setJobs] = useState<JobView[]>([]);
  const [monthOffset, setMonthOffset] = useState(0);

  useEffect(() => {
    fetch("/api/cron")
      .then((r) => r.json())
      .then((d) => setJobs(d.jobs ?? []));
  }, []);

  const month = useMemo(() => {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth() + monthOffset, 1);
  }, [monthOffset]);

  const days = useMemo(() => {
    const first = new Date(month.getFullYear(), month.getMonth(), 1);
    const last = new Date(month.getFullYear(), month.getMonth() + 1, 0);
    const startPad = first.getDay();
    const total = last.getDate();
    const slots: (Date | null)[] = [];
    for (let i = 0; i < startPad; i++) slots.push(null);
    for (let d = 1; d <= total; d++) slots.push(new Date(month.getFullYear(), month.getMonth(), d));
    return slots;
  }, [month]);

  const jobsByDay = useMemo(() => {
    const map = new Map<string, JobView[]>();
    for (const job of jobs) {
      if (!job.state?.nextRunAtMs) continue;
      const d = new Date(job.state.nextRunAtMs);
      if (d.getMonth() !== month.getMonth() || d.getFullYear() !== month.getFullYear()) continue;
      const key = `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
      const list = map.get(key) ?? [];
      list.push(job);
      map.set(key, list);
    }
    return map;
  }, [jobs, month]);

  return (
    <div>
      <h1>Cron Calendar</h1>
      <p className="muted">Timezone: America/New_York</p>
      <div className="calendar-header">
        <button onClick={() => setMonthOffset((v) => v - 1)}>←</button>
        <strong>{monthLabel(month)}</strong>
        <button onClick={() => setMonthOffset((v) => v + 1)}>→</button>
      </div>

      <div className="legend">
        {Object.entries(BUCKETS).map(([bucket, color]) => (
          <span key={bucket} className="legend-item">
            <i style={{ background: color }} /> {bucket}
          </span>
        ))}
      </div>

      <div className="calendar-grid">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
          <div key={d} className="dow">{d}</div>
        ))}
        {days.map((day, idx) => {
          if (!day) return <div key={`empty-${idx}`} className="day empty" />;
          const key = `${day.getFullYear()}-${day.getMonth()}-${day.getDate()}`;
          const dayJobs = jobsByDay.get(key) ?? [];

          return (
            <div key={key} className="day">
              <div className="day-num">{day.getDate()}</div>
              <div className="day-jobs">
                {dayJobs.map((job) => (
                  <article
                    key={job.id}
                    className="job-card"
                    style={{ borderLeft: `4px solid ${BUCKETS[job.bucket]}` }}
                  >
                    <div className="job-top">
                      <strong>{job.name}</strong>
                      <span className={`badge ${job.status.tone}`}>{job.status.label}</span>
                    </div>
                    <div className="mini">🕐 {job.scheduleText}</div>
                    <div className="mini"><b>Next:</b> {fmt(job.state?.nextRunAtMs)}</div>
                    <div className="mini"><b>Last:</b> {fmt(job.state?.lastRunAtMs)}</div>
                    <div className="mini id">ID: {job.id.slice(0, 8)}...</div>
                  </article>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
