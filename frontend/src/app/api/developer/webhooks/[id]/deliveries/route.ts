import { headers } from "next/headers";
import { NextResponse } from "next/server";

import { auth } from "@/lib/auth";
import prisma from "@/lib/prisma";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  if (!id) {
    return NextResponse.json({ error: "Missing id" }, { status: 400 });
  }

  const rows = await prisma.$queryRaw<
    Array<{
      id: string;
      event: string;
      status: string;
      attempt: number;
      response_status: number | null;
      last_error: string | null;
      created_at: Date;
    }>
  >`
    SELECT id, event, status, attempt, response_status, last_error, created_at
    FROM webhook_deliveries
    WHERE user_id = ${session.user.id}
      AND webhook_id = ${id}
    ORDER BY created_at DESC
    LIMIT 100
  `;

  return NextResponse.json({
    deliveries: rows.map((r) => ({
      id: r.id,
      event: r.event,
      status: r.status,
      attempt: Number(r.attempt),
      response_status: r.response_status,
      last_error: r.last_error,
      created_at: r.created_at.toISOString(),
    })),
  });
}

