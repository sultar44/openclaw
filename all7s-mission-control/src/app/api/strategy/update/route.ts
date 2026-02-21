import { NextRequest, NextResponse } from "next/server";
import { updateEntry } from "@/lib/strategy";

export async function POST(req: NextRequest) {
  try {
    const body = (await req.json()) as {
      id?: string;
      status?: "approved" | "rejected";
      question?: string;
      answer?: string;
    };

    if (!body.id || !body.status) {
      return NextResponse.json({ error: "id and status are required" }, { status: 400 });
    }

    await updateEntry(body.id, body.status, body.question, body.answer);

    return NextResponse.json({ ok: true });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to update strategy entry", details: String(error) },
      { status: 500 },
    );
  }
}
