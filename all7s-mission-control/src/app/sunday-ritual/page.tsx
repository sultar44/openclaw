"use client";

import { useEffect, useState } from "react";

type Topic = {
  topic: string;
  status: string;
  added: string;
  brief: string;
  email_subject?: string;
  email_preview?: string;
  email_body?: string;
};

export default function SundayRitualPage() {
  const [pending, setPending] = useState<Topic[]>([]);
  const [selected, setSelected] = useState<Topic | null>(null);
  const [drafted, setDrafted] = useState<Topic | null>(null);
  const [usedCount, setUsedCount] = useState(0);
  const [publishedCount, setPublishedCount] = useState(0);
  const [loading, setLoading] = useState(false);

  async function load() {
    const data = await fetch("/api/sunday-ritual/topics").then((r) => r.json());
    setPending(data.pending ?? []);
    setSelected(data.selected ?? null);
    setDrafted(data.drafted ?? null);
    setUsedCount(data.usedCount ?? 0);
    setPublishedCount(data.publishedCount ?? 0);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleSelect(topicName: string) {
    const ok = window.confirm(
      `Select "${topicName}" for this week's Sunday Ritual? Chloe will start drafting the email.`
    );
    if (!ok) return;

    setLoading(true);
    try {
      const res = await fetch("/api/sunday-ritual/select", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topicName }),
      });

      if (!res.ok) {
        const data = await res.json();
        alert(`Error: ${data.error}`);
        return;
      }

      alert(
        `"${topicName}" selected! Tell Chloe in Slack to start Phase 2 (draft the email).`
      );
      await load();
    } finally {
      setLoading(false);
    }
  }

  const activeItem = selected || drafted;

  return (
    <div>
      <h1>Sunday Ritual</h1>
      <div className="stats-row">
        <div className="stat">
          <b>{pending.length}</b>
          <span>Topics Ready</span>
        </div>
        <div className="stat">
          <b>{usedCount}</b>
          <span>Used</span>
        </div>
        <div className="stat">
          <b>{publishedCount}</b>
          <span>Published</span>
        </div>
      </div>

      {activeItem && (
        <div className="panel" style={{ marginBottom: 24 }}>
          <div className="meta">
            Status: <strong>{activeItem.status}</strong>
          </div>
          <h3 style={{ margin: "8px 0 4px" }}>{activeItem.topic}</h3>
          <p style={{ margin: 0, color: "#aaa" }}>{activeItem.brief}</p>
          {activeItem.email_subject && (
            <div style={{ marginTop: 12 }}>
              <label>Subject</label>
              <div className="meta">{activeItem.email_subject}</div>
              <label>Preview</label>
              <div className="meta">{activeItem.email_preview}</div>
              <label>Body</label>
              <div
                className="meta"
                style={{ whiteSpace: "pre-wrap", maxHeight: 300, overflow: "auto" }}
              >
                {activeItem.email_body}
              </div>
            </div>
          )}
          <div className="meta" style={{ marginTop: 8, fontStyle: "italic" }}>
            {activeItem.status === "selected"
              ? "Waiting for Chloe to draft the email. Tell her in Slack!"
              : "Email drafted — review in Slack to approve."}
          </div>
        </div>
      )}

      <h2 style={{ fontSize: 16, marginBottom: 12 }}>Topic Queue</h2>
      {pending.length === 0 ? (
        <div className="panel">
          No pending topics. New topics are proposed every Thursday at 9 PM.
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {pending.map((t) => (
            <div key={t.topic} className="panel" style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ flex: 1 }}>
                <strong>{t.topic}</strong>
                <div className="meta">{t.brief}</div>
              </div>
              <button
                className="approve"
                onClick={() => handleSelect(t.topic)}
                disabled={loading || !!activeItem}
                style={{ flexShrink: 0 }}
              >
                Select
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
