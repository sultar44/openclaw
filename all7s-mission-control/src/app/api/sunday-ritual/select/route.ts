import { NextResponse } from "next/server";
import { selectTopic } from "@/lib/sunday-ritual";
import { exec } from "node:child_process";
import { promisify } from "node:util";

const execAsync = promisify(exec);

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

    // Send message to #chloebot to trigger the workflow directly
    const message = `[AUTO] Sunday Ritual topic selected from dashboard: "${selected.topic}". Brief: ${selected.brief}. Please research this person, write the email body and blog HTML, then run sunday_ritual_publisher.py to publish and create the Klaviyo campaign. Post results here.`;

    // Fire and forget — don't block the UI response
    execAsync(
      `openclaw message send --channel slack --target C0AD9AZ7R6F --message ${JSON.stringify(message)}`,
    ).catch((err) => {
      console.error("Failed to send Slack trigger:", err);
    });

    return NextResponse.json({ ok: true, selected });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to select topic", details: String(error) },
      { status: 500 },
    );
  }
}
