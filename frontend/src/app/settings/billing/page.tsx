"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";

type BillingHistoryItem = {
  task_id: string;
  created_at: string;
  source_title: string | null;
  minutes: number;
  status: string;
};

type BillingDashboard = {
  period_start: string | null;
  period_end: string | null;
  plan: string;
  subscription_status: string;
  minutes_used: number;
  minutes_remaining: number | null;
  history: BillingHistoryItem[];
};

export default function BillingSettingsPage() {
  const [data, setData] = useState<BillingDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/billing/dashboard", { cache: "no-store" })
      .then(async (r) => {
        const json = (await r.json().catch(() => ({}))) as BillingDashboard & { error?: string };
        if (!r.ok) throw new Error(json.error || "Failed to load billing dashboard");
        setData(json);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load billing dashboard"));
  }, []);

  return (
    <div className="mx-auto w-full max-w-3xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Billing</h1>
          <p className="text-sm text-muted-foreground">Usage and processing minutes.</p>
        </div>
        <Button asChild variant="ghost">
          <Link href="/settings">Back</Link>
        </Button>
      </div>

      {error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <div className="rounded-lg border p-4 space-y-2">
        <div className="text-sm text-muted-foreground">Current period</div>
        <div className="text-sm">
          {data?.period_start ?? "—"} → {data?.period_end ?? "—"}
        </div>
        <Separator />
        <div className="flex items-center justify-between">
          <div className="text-sm">Minutes processed</div>
          <div className="text-lg font-semibold">{data?.minutes_used ?? 0}</div>
        </div>
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">Minutes remaining</div>
          <div className="text-sm">{data?.minutes_remaining ?? "—"}</div>
        </div>
      </div>

      <div className="space-y-2">
        <h2 className="text-lg font-semibold">History</h2>
        <div className="rounded-lg border divide-y">
          {data?.history?.length ? (
            data.history.map((h) => (
              <div key={h.task_id} className="p-4 flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <div className="font-medium truncate">{h.source_title || h.task_id}</div>
                  <div className="text-xs text-muted-foreground truncate">
                    {h.created_at} • {h.status}
                  </div>
                </div>
                <div className="text-sm font-semibold">{h.minutes} min</div>
              </div>
            ))
          ) : (
            <div className="p-4 text-sm text-muted-foreground">No history yet.</div>
          )}
        </div>
      </div>
    </div>
  );
}

