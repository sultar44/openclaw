"use client";

import { useEffect, useMemo, useState } from "react";

type Entry = {
  id: string;
  source?: string;
  question?: string;
  title?: string;
  recommendation?: string;
  strategy?: string;
  tags?: string[];
  post_date?: string;
};

export default function StrategyReviewPage() {
  const [pending, setPending] = useState<Entry[]>([]);
  const [approved, setApproved] = useState(0);
  const [rejected, setRejected] = useState(0);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const active = pending[0];

  async function load() {
    const data = await fetch("/api/strategy/entries").then((r) => r.json());
    setPending(data.pending ?? []);
    setApproved(data.approved ?? 0);
    setRejected(data.rejected ?? 0);
  }

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    if (!active) return;
    setQuestion(active.question ?? active.title ?? "");
    setAnswer(active.recommendation ?? active.strategy ?? "");
  }, [active?.id]);

  const pendingCount = useMemo(() => pending.length, [pending]);

  async function submit(status: "approved" | "rejected") {
    if (!active) return;

    await fetch("/api/strategy/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: active.id, status, question, answer }),
    });

    await load();
  }

  function skip() {
    if (pending.length <= 1) return;
    const [first, ...rest] = pending;
    setPending([...rest, first]);
  }

  return (
    <div>
      <h1>Canasta Strategy Review</h1>
      <div className="stats-row">
        <div className="stat"><b>{pendingCount}</b><span>Pending</span></div>
        <div className="stat"><b>{approved}</b><span>Approved</span></div>
        <div className="stat"><b>{rejected}</b><span>Rejected</span></div>
      </div>

      {!active ? (
        <div className="panel">All done. No pending entries.</div>
      ) : (
        <div className="panel">
          <div className="meta">Entry 1 of {pendingCount} · {active.id} · {active.source ?? "unknown"}</div>
          {active.post_date ? <div className="meta">{active.post_date}</div> : null}

          <label>Question</label>
          <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={4} />

          <label>Answer</label>
          <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} rows={7} />

          <div className="tags">
            {(active.tags ?? []).map((tag) => (
              <span key={tag} className="tag">{tag}</span>
            ))}
          </div>

          <div className="actions">
            <button className="reject" onClick={() => submit("rejected")}>Reject</button>
            <button className="skip" onClick={skip}>Skip</button>
            <button className="approve" onClick={() => submit("approved")}>Approve</button>
          </div>
        </div>
      )}
    </div>
  );
}
