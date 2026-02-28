import { NextResponse } from "next/server";
import { getNextPS } from "@/lib/better-hand";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const ps = await getNextPS();
    return NextResponse.json(ps);
  } catch (error) {
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}
