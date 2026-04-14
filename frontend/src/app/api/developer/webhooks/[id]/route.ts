import { headers } from "next/headers";
import { NextResponse } from "next/server";
import crypto from "crypto";

import { auth } from "@/lib/auth";
import prisma from "@/lib/prisma";

function normalizeEvents(events: unknown): string[] {
  if (!Array.isArray(events)) return [];
  return events
    .map((e) => String(e).trim())
    .filter(Boolean)
    .slice(0, 50);
}

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const body = (await request.json().catch(() => ({}))) as {
    url?: unknown;
    events?: unknown;
    enabled?: unknown;
    rotate_secret?: unknown;
  };

  const url = body.url === undefined ? undefined : String(body.url ?? "").trim();
  const events = body.events === undefined ? undefined : normalizeEvents(body.events);
  const enabled = body.enabled === undefined ? undefined : Boolean(body.enabled);
  const rotateSecret = Boolean(body.rotate_secret);

  const newSecret = rotateSecret ? `whsec_${crypto.randomBytes(24).toString("hex")}` : null;

  const updated = await prisma.$queryRaw<Array<{ id: string }>>`
    UPDATE webhooks
    SET
      url = COALESCE(${url}, url),
      events = COALESCE(${events}::text[], events),
      enabled = COALESCE(${enabled}, enabled),
      secret = CASE WHEN ${rotateSecret} THEN ${newSecret} ELSE secret END
    WHERE id = ${id}
      AND user_id = ${session.user.id}
    RETURNING id
  `;

  if (!updated?.[0]?.id) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json({ ok: true, secret: newSecret });
}

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const deleted = await prisma.$queryRaw<Array<{ id: string }>>`
    DELETE FROM webhooks
    WHERE id = ${id}
      AND user_id = ${session.user.id}
    RETURNING id
  `;

  if (!deleted?.[0]?.id) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json({ ok: true });
}

