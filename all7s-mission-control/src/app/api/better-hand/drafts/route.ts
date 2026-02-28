import { NextResponse } from "next/server";
import { loadDrafts, loadApprovedHistory } from "@/lib/better-hand";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const allDrafts = await loadDrafts();
    const approved = await loadApprovedHistory();
    const pending = allDrafts.filter((d) => d.status === "pending");
    const rejected = allDrafts.filter((d) => d.status === "rejected").length;

    return NextResponse.json({
      drafts: pending,
      approvedCount: approved.length,
      rejectedCount: rejected,
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to load drafts", details: String(error) },
      { status: 500 },
    );
  }
}
