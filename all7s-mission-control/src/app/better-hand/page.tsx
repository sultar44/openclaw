"use client";

import { useEffect, useState } from "react";

type Draft = {
  id: string;
  subject: string;
  previewText: string;
  body: string;
  status: string;
  createdAt: string;
};

export default function BetterHandPage() {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [approvedCount, setApprovedCount] = useState(0);
  const [rejectedCount, setRejectedCount] = useState(0);
  const [subject, setSubject] = useState("");
  const [previewText, setPreviewText] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [nextPS, setNextPS] = useState<{ type: string; text: string } | null>(null);

  const active = drafts[0];

  async function load() {
    const data = await fetch("/api/better-hand/drafts").then((r) => r.json());
    setDrafts(data.drafts ?? []);
    setApprovedCount(data.approvedCount ?? 0);
    setRejectedCount(data.rejectedCount ?? 0);
  }

  async function loadPS() {
    const ps = await fetch("/api/better-hand/ps").then((r) => r.json());
    setNextPS(ps);
  }

  useEffect(() => {
    load();
    loadPS();
  }, []);

  useEffect(() => {
    if (!active) return;
    setSubject(active.subject ?? "");
    setPreviewText(active.previewText ?? "");
    setBody(active.body ?? "");
  }, [active?.id]);

  async function submit(status: "approved" | "rejected") {
    if (!active) return;

    if (status === "approved") {
      const ok = window.confirm(
        `This will create a Klaviyo draft campaign and add the "${nextPS?.type}" P.S. Continue?`
      );
      if (!ok) return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/better-hand/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: active.id, status, subject, previewText, body }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(`Error: ${data.error}\n${data.details ?? ""}`);
        return;
      }

      if (status === "approved" && data.klaviyoCampaignId) {
        alert(
          `Klaviyo draft campaign created!\n\nCampaign ID: ${data.klaviyoCampaignId}\nP.S. type: ${data.psType}\n\nCheck Klaviyo to finalize and schedule.`
        );
        await loadPS(); // refresh P.S. indicator
      }

      await load();
    } finally {
      setLoading(false);
    }
  }

  function skip() {
    if (drafts.length <= 1) return;
    const [first, ...rest] = drafts;
    setDrafts([...rest, first]);
  }

  return (
    <div>
      <h1>Better Hand Emails</h1>
      <div className="stats-row">
        <div className="stat">
          <b>{drafts.length}</b>
          <span>Pending</span>
        </div>
        <div className="stat">
          <b>{approvedCount}</b>
          <span>Approved</span>
        </div>
        <div className="stat">
          <b>{rejectedCount}</b>
          <span>Rejected</span>
        </div>
        {nextPS && (
          <div className="stat">
            <b>{nextPS.type}</b>
            <span>Next P.S.</span>
          </div>
        )}
      </div>

      {!active ? (
        <div className="panel">
          All done. No pending drafts.
          <div className="meta" style={{ marginTop: 8 }}>
            Drafts are generated every Wednesday at 9:15 AM.
          </div>
        </div>
      ) : (
        <div className="panel">
          <div className="meta">
            Draft {1} of {drafts.length} · {active.id} · Created{" "}
            {new Date(active.createdAt).toLocaleDateString()}
          </div>

          <label>Subject Line</label>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />

          <label>Preview Text</label>
          <input
            type="text"
            value={previewText}
            onChange={(e) => setPreviewText(e.target.value)}
          />

          <label>Email Body</label>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={12}
          />

          {nextPS && (
            <div className="meta" style={{ marginTop: 12, fontStyle: "italic" }}>
              On approve, this P.S. will be added: {nextPS.text}
            </div>
          )}

          <div className="actions">
            <button className="reject" onClick={() => submit("rejected")} disabled={loading}>
              Reject
            </button>
            <button className="skip" onClick={skip} disabled={loading}>
              Skip
            </button>
            <button className="approve" onClick={() => submit("approved")} disabled={loading}>
              {loading ? "Creating..." : "Approve"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
