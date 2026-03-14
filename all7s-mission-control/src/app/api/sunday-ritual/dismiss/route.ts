import { NextResponse } from "next/server";
import { dismissActive } from "@/lib/sunday-ritual";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    const dismissed = await dismissActive();
    return NextResponse.json({ ok: true, dismissed });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to dismiss", details: String(error) },
      { status: 500 },
    );
  }
}
