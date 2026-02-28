import { NextRequest, NextResponse } from "next/server";
import {
  updateDraft,
  createKlaviyoCampaign,
  addToApprovedHistory,
  getNextPS,
  advancePSRotation,
} from "@/lib/better-hand";

export async function POST(req: NextRequest) {
  try {
    const body = (await req.json()) as {
      id?: string;
      status?: "approved" | "rejected";
      subject?: string;
      previewText?: string;
      body?: string;
    };

    if (!body.id || !body.status) {
      return NextResponse.json({ error: "id and status are required" }, { status: 400 });
    }

    const draft = await updateDraft(body.id, body.status, body.subject, body.previewText, body.body);
    if (!draft) {
      return NextResponse.json({ error: "Draft not found" }, { status: 404 });
    }

    let klaviyoCampaignId: string | null = null;
    let psType: string | null = null;

    if (body.status === "approved") {
      try {
        // Get the next P.S. in rotation
        const ps = await getNextPS();
        psType = ps.type;

        // Create Klaviyo campaign
        klaviyoCampaignId = await createKlaviyoCampaign(draft.subject);

        // Log to approved history
        await addToApprovedHistory({
          id: draft.id,
          subject: draft.subject,
          approvedAt: new Date().toISOString(),
          klaviyoCampaignId: klaviyoCampaignId ?? undefined,
        });

        // Advance P.S. rotation for next time
        await advancePSRotation();
      } catch (err) {
        return NextResponse.json(
          { error: "Draft approved but Klaviyo campaign creation failed", details: String(err) },
          { status: 502 },
        );
      }
    }

    return NextResponse.json({ ok: true, klaviyoCampaignId, psType });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to update draft", details: String(error) },
      { status: 500 },
    );
  }
}
