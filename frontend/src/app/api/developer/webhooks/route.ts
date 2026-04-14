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

export async function GET() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const rows = await prisma.$queryRaw<
    Array<{
      id: string;
      url: string;
      events: string[];
      enabled: boolean;
      created_at: Date;
    }>
  >`
    SELECT id, url, events, enabled, created_at
    FROM webhooks
    WHERE user_id = ${session.user.id}
    ORDER BY created_at DESC
    LIMIT 100
  `;

  return NextResponse.json({
    webhooks: rows.map((w) => ({
      id: w.id,
      url: w.url,
      events: w.events ?? [],
      enabled: Boolean(w.enabled),
      created_at: w.created_at.toISOString(),
    })),
  });
}

export async function POST(request: Request) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = (await request.json().catch(() => ({}))) as {
    url?: unknown;
    events?: unknown;
    enabled?: unknown;
  };

  const url = String(body.url ?? "").trim();
  if (!url) {
    return NextResponse.json({ error: "URL is required" }, { status: 400 });
  }

  const events = normalizeEvents(body.events);
  const enabled = body.enabled === undefined ? true : Boolean(body.enabled);
  const secret = `whsec_${crypto.randomBytes(24).toString("hex")}`;

  const inserted = await prisma.$queryRaw<Array<{ id: string }>>`
    INSERT INTO webhooks (user_id, url, events, enabled, secret)
    VALUES (${session.user.id}, ${url}, ${events}::text[], ${enabled}, ${secret})
    RETURNING id
  `;

  return NextResponse.json({
    id: inserted?.[0]?.id ?? null,
    secret, // show once
  });
}

