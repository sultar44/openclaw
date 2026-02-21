import { NextResponse } from "next/server";
import { loadEntries } from "@/lib/strategy";

export async function GET() {
  try {
    const entries = await loadEntries();
    const pending = entries.filter((e) => e.status === "pending");
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
