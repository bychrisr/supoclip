"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

type Delivery = {
  id: string;
  event: string;
  status: string;
  attempt: number;
  response_status: number | null;
  last_error: string | null;
  created_at: string;
};

export default function WebhookLogsPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    fetch(`/api/developer/webhooks/${id}/deliveries`, { cache: "no-store" })
      .then(async (r) => {
        const json = (await r.json().catch(() => ({}))) as { deliveries?: Delivery[]; error?: string };
        if (!r.ok) throw new Error(json.error || "Failed to load deliveries");
        setDeliveries(json.deliveries ?? []);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load deliveries"));
  }, [id]);

  return (
    <div className="mx-auto w-full max-w-3xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Webhook logs</h1>
          <p className="text-sm text-muted-foreground">Recent delivery attempts.</p>
        </div>
        <Button asChild variant="ghost">
          <Link href="/settings/developer">Back</Link>
        </Button>
      </div>

      {error ? (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <div className="rounded-lg border divide-y">
        {deliveries.length === 0 ? (
          <div className="p-4 text-sm text-muted-foreground">No deliveries yet.</div>
        ) : (
          deliveries.map((d) => (
            <div key={d.id} className="p-4 space-y-1">
              <div className="flex items-center justify-between gap-4">
                <div className="font-mono text-xs truncate">{d.id}</div>
                <div className="text-xs text-muted-foreground">
                  {d.status} • attempt {d.attempt} • {d.response_status ?? "—"}
                </div>
              </div>
              <div className="text-sm">{d.event}</div>
              {d.last_error ? (
                <div className="text-xs text-destructive break-words">{d.last_error}</div>
              ) : null}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

