import { NextResponse } from "next/server";
import { selectTopic } from "@/lib/sunday-ritual";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { topic } = await req.json();
    if (!topic) {
      return NextResponse.json({ error: "Missing topic" }, { status: 400 });
    }

    const selected = await selectTopic(topic);
    if (!selected) {
      return NextResponse.json(
        { error: "Topic not found or not pending" },
        { status: 404 },
      );
    }

    return NextResponse.json({ ok: true, selected });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to select topic", details: String(error) },
      { status: 500 },
    );
  }
}
