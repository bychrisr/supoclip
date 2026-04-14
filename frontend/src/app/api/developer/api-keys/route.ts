import { headers } from "next/headers";
import { NextResponse } from "next/server";
import crypto from "crypto";

import { auth } from "@/lib/auth";
import prisma from "@/lib/prisma";

function randomKey(prefix: string): string {
  const bytes = crypto.randomBytes(32).toString("base64url");
  return `${prefix}_${bytes}`;
}

function sha256Hex(value: string): string {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function hashApiKey(apiKey: string): string {
  const pepper = process.env.API_KEY_PEPPER;
  if (!pepper) {
    throw new Error("API_KEY_PEPPER is not configured");
  }
  return sha256Hex(`${pepper}${apiKey}`);
}

function normalizeScopes(scopes: unknown): string[] {
  if (!Array.isArray(scopes)) return [];
  return scopes
    .map((s) => String(s).trim())
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
      name: string;
      prefix: string;
      scopes: string[];
      last_used_at: Date | null;
      revoked_at: Date | null;
      created_at: Date;
    }>
  >`
    SELECT id, name, prefix, scopes, last_used_at, revoked_at, created_at
    FROM api_keys
    WHERE user_id = ${session.user.id}
    ORDER BY created_at DESC
    LIMIT 100
  `;

  return NextResponse.json({
    api_keys: rows.map((r) => ({
      id: r.id,
      name: r.name,
      prefix: r.prefix,
      scopes: r.scopes ?? [],
      last_used_at: r.last_used_at ? r.last_used_at.toISOString() : null,
      revoked_at: r.revoked_at ? r.revoked_at.toISOString() : null,
      created_at: r.created_at.toISOString(),
    })),
  });
}

export async function POST(request: Request) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = (await request.json().catch(() => ({}))) as {
    name?: unknown;
    scopes?: unknown;
  };
  const name = String(body.name ?? "").trim();
  if (!name) {
    return NextResponse.json({ error: "Name is required" }, { status: 400 });
  }

  const scopes = normalizeScopes(body.scopes);

  const prefix = `sk_${crypto.randomBytes(8).toString("hex")}`;
  const apiKey = randomKey(prefix);
  const keyHash = hashApiKey(apiKey);

  try {
    const inserted = await prisma.$queryRaw<Array<{ id: string }>>`
      INSERT INTO api_keys (user_id, key_hash, prefix, name, scopes)
      VALUES (${session.user.id}, ${keyHash}, ${prefix}, ${name}, ${scopes}::text[])
      RETURNING id
    `;

    return NextResponse.json({
      id: inserted?.[0]?.id ?? null,
      api_key: apiKey, // show once
      prefix,
    });
  } catch (error) {
    // Unique (user_id, prefix) can collide; retry once.
    const prefix2 = `sk_${crypto.randomBytes(8).toString("hex")}`;
    const apiKey2 = randomKey(prefix2);
    const keyHash2 = hashApiKey(apiKey2);

    const inserted2 = await prisma.$queryRaw<Array<{ id: string }>>`
      INSERT INTO api_keys (user_id, key_hash, prefix, name, scopes)
      VALUES (${session.user.id}, ${keyHash2}, ${prefix2}, ${name}, ${scopes}::text[])
      RETURNING id
    `;

    return NextResponse.json({
      id: inserted2?.[0]?.id ?? null,
      api_key: apiKey2,
      prefix: prefix2,
      warning: error instanceof Error ? error.message : "Key regenerated",
    });
  }
}

