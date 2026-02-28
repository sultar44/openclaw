import { NextResponse } from "next/server";
import { loadTopics, loadLog } from "@/lib/sunday-ritual";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const topics = await loadTopics();
    const log = await loadLog();

    const pending = topics.filter((t) => t.status === "pending");
    const selected = topics.find((t) => t.status === "selected") ?? null;
    const drafted = topics.find((t) => t.status === "drafted") ?? null;
    const usedCount = topics.filter((t) => t.status === "used").length;

    return NextResponse.json({
      pending,
      selected,
      drafted,
      usedCount,
      publishedCount: log.length,
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to load topics", details: String(error) },
      { status: 500 },
    );
  }
}
