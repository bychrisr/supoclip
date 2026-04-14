import { headers } from "next/headers";
import { NextResponse } from "next/server";

import { auth } from "@/lib/auth";
import prisma from "@/lib/prisma";

function asIso(value: unknown): string | null {
  if (!value) return null;
  if (value instanceof Date) return value.toISOString();
  const parsed = new Date(String(value));
  return Number.isNaN(parsed.getTime()) ? null : parsed.toISOString();
}

type BillingHistoryItem = {
  task_id: string;
  created_at: string;
  source_title: string | null;
  minutes: number;
  status: string;
};

export async function GET() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    select: {
      billing_period_start: true,
      billing_period_end: true,
      plan: true,
      subscription_status: true,
    },
  });

  const periodStart = user?.billing_period_start ?? null;
  const periodEnd = user?.billing_period_end ?? null;

  const minutesRow = (await prisma.$queryRaw<Array<{ minutes: number | null }>>`
    SELECT COALESCE(SUM(br.minutes_processed), 0) AS minutes
    FROM billing_records br
    WHERE br.user_id = ${session.user.id}
      AND (${periodStart}::timestamptz IS NULL OR br.created_at >= ${periodStart})
      AND (${periodEnd}::timestamptz IS NULL OR br.created_at <= ${periodEnd})
  `)?.[0];

  const minutesUsed = Number(minutesRow?.minutes ?? 0);

  const historyRows = await prisma.$queryRaw<
    Array<{
      task_id: string;
      created_at: Date;
      source_title: string | null;
      minutes_processed: number | null;
      status: string;
    }>
  >`
    SELECT
      br.task_id AS task_id,
      br.created_at AS created_at,
      br.source_title AS source_title,
      br.minutes_processed AS minutes_processed,
      t.status AS status
    FROM billing_records br
    LEFT JOIN tasks t ON t.id = br.task_id
    WHERE br.user_id = ${session.user.id}
      AND (${periodStart}::timestamptz IS NULL OR br.created_at >= ${periodStart})
      AND (${periodEnd}::timestamptz IS NULL OR br.created_at <= ${periodEnd})
    ORDER BY br.created_at DESC
    LIMIT 25
  `;

  const history: BillingHistoryItem[] = historyRows.map((row) => ({
    task_id: row.task_id,
    created_at: row.created_at.toISOString(),
    source_title: row.source_title,
    minutes: Number(row.minutes_processed ?? 0),
    status: row.status,
  }));

  // Remaining minutes: we don't have a minutes-based cap in config yet.
  // Return null so UI can display "Unlimited/—" until a backend limit exists.
  const minutesRemaining: number | null = null;

  return NextResponse.json({
    period_start: asIso(periodStart),
    period_end: asIso(periodEnd),
    plan: user?.plan ?? "free",
    subscription_status: user?.subscription_status ?? "inactive",
    minutes_used: minutesUsed,
    minutes_remaining: minutesRemaining,
    history,
  });
}

