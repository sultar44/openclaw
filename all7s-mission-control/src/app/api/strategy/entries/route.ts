import { NextResponse } from "next/server";
import { loadEntries } from "@/lib/strategy";

export async function GET() {
  try {
    const entries = await loadEntries();

    // Normalize: some entries use entry_id instead of id
    const normalize = (e: Record<string, unknown>) => ({
      ...e,
      id: e.id ?? e.entry_id ?? e.post_id ?? "unknown",
    });

    const pending = entries
      .filter((e) => e.status === "pending")
      .map(normalize);
    const approved = entries.filter((e) => e.status === "approved").length;
    const rejected = entries.filter((e) => e.status === "rejected").length;

    return NextResponse.json({ pending, approved, rejected, total: entries.length });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to load strategy entries", details: String(error) },
      { status: 500 },
    );
  }
}
