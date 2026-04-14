"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Alert, AlertDescription } from "@/components/ui/alert";

type ApiKey = {
  id: string;
  name: string;
  prefix: string;
  scopes: string[];
  last_used_at: string | null;
  revoked_at: string | null;
  created_at: string;
};

type Webhook = {
  id: string;
  url: string;
  events: string[];
  enabled: boolean;
  created_at: string;
};

export default function DeveloperSettingsPage() {
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [creatingKey, setCreatingKey] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [newKeyScopes, setNewKeyScopes] = useState("clips:read,clips:write");
  const [createdKeyOnce, setCreatedKeyOnce] = useState<string | null>(null);

  const [webhooks, setWebhooks] = useState<Webhook[]>([]);
  const [creatingWebhook, setCreatingWebhook] = useState(false);
  const [newWebhookUrl, setNewWebhookUrl] = useState("");
  const [newWebhookEvents, setNewWebhookEvents] = useState(
    "task.processing_started,task.processing_completed,task.processing_failed"
  );
  const [createdWebhookSecretOnce, setCreatedWebhookSecretOnce] = useState<string | null>(null);

  const scopes = useMemo(
    () =>
      newKeyScopes
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    [newKeyScopes]
  );

  const events = useMemo(
    () =>
      newWebhookEvents
        .split(",")
        .map((e) => e.trim())
        .filter(Boolean),
    [newWebhookEvents]
  );

  async function refresh() {
    setError(null);
    const [keysResp, hooksResp] = await Promise.all([
      fetch("/api/developer/api-keys", { cache: "no-store" }),
      fetch("/api/developer/webhooks", { cache: "no-store" }),
    ]);

    if (keysResp.ok) {
      const json = (await keysResp.json()) as { api_keys: ApiKey[] };
      setApiKeys(json.api_keys ?? []);
    }
    if (hooksResp.ok) {
      const json = (await hooksResp.json()) as { webhooks: Webhook[] };
      setWebhooks(json.webhooks ?? []);
    }
  }

  useEffect(() => {
    refresh().catch(() => {});
  }, []);

  async function createKey() {
    setError(null);
    setSuccess(null);
    setCreatedKeyOnce(null);
    if (!newKeyName.trim()) {
      setError("Key name is required.");
      return;
    }

    setCreatingKey(true);
    try {
      const resp = await fetch("/api/developer/api-keys", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name: newKeyName.trim(), scopes }),
      });
      const json = (await resp.json().catch(() => ({}))) as {
        api_key?: string;
        error?: string;
      };
      if (!resp.ok) {
        setError(json.error || "Failed to create API key.");
        return;
      }
      setCreatedKeyOnce(json.api_key ?? null);
      setSuccess("API key created. Copy it now — it will only be shown once.");
      await refresh();
      setNewKeyName("");
    } finally {
      setCreatingKey(false);
    }
  }

  async function revokeKey(id: string) {
    setError(null);
    setSuccess(null);
    const resp = await fetch(`/api/developer/api-keys/${id}`, { method: "POST" });
    if (!resp.ok) {
      const json = (await resp.json().catch(() => ({}))) as { error?: string };
      setError(json.error || "Failed to revoke key.");
      return;
    }
    setSuccess("API key revoked.");
    await refresh();
  }

  async function createWebhook() {
    setError(null);
    setSuccess(null);
    setCreatedWebhookSecretOnce(null);
    if (!newWebhookUrl.trim()) {
      setError("Webhook URL is required.");
      return;
    }
    if (events.length === 0) {
      setError("At least one event is required.");
      return;
    }

    setCreatingWebhook(true);
    try {
      const resp = await fetch("/api/developer/webhooks", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ url: newWebhookUrl.trim(), events, enabled: true }),
      });
      const json = (await resp.json().catch(() => ({}))) as {
        secret?: string;
        error?: string;
      };
      if (!resp.ok) {
        setError(json.error || "Failed to create webhook.");
        return;
      }
      setCreatedWebhookSecretOnce(json.secret ?? null);
      setSuccess("Webhook created. Copy the secret now — it will only be shown once.");
      await refresh();
      setNewWebhookUrl("");
    } finally {
      setCreatingWebhook(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-3xl space-y-8 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Developer</h1>
          <p className="text-sm text-muted-foreground">
            API keys, webhooks, and automation settings.
          </p>
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
      {success ? (
        <Alert>
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      ) : null}

      <section className="space-y-4">
        <h2 className="text-lg font-semibold">API Keys</h2>

        <div className="rounded-lg border p-4 space-y-3">
          <div className="space-y-2">
            <Label htmlFor="key-name">Name</Label>
            <Input
              id="key-name"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              placeholder="e.g. Zapier, Make, internal tool"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="key-scopes">Scopes (comma-separated)</Label>
            <Input
              id="key-scopes"
              value={newKeyScopes}
              onChange={(e) => setNewKeyScopes(e.target.value)}
            />
          </div>
          <Button onClick={createKey} disabled={creatingKey}>
            {creatingKey ? "Creating..." : "Create API key"}
          </Button>

          {createdKeyOnce ? (
            <div className="rounded-md bg-muted p-3 font-mono text-xs break-all">
              {createdKeyOnce}
            </div>
          ) : null}
        </div>

        <div className="rounded-lg border divide-y">
          {apiKeys.length === 0 ? (
            <div className="p-4 text-sm text-muted-foreground">No API keys yet.</div>
          ) : (
            apiKeys.map((k) => (
              <div key={k.id} className="p-4 flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <div className="font-medium truncate">{k.name}</div>
                  <div className="text-xs text-muted-foreground">
                    Prefix: <span className="font-mono">{k.prefix}</span>
                    {k.revoked_at ? " • Revoked" : ""}
                  </div>
                </div>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => revokeKey(k.id)}
                  disabled={Boolean(k.revoked_at)}
                >
                  Revoke
                </Button>
              </div>
            ))
          )}
        </div>
      </section>

      <Separator />

      <section className="space-y-4">
        <h2 className="text-lg font-semibold">Webhooks</h2>

        <div className="rounded-lg border p-4 space-y-3">
          <div className="space-y-2">
            <Label htmlFor="wh-url">URL</Label>
            <Input
              id="wh-url"
              value={newWebhookUrl}
              onChange={(e) => setNewWebhookUrl(e.target.value)}
              placeholder="https://example.com/webhooks/supoclip"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="wh-events">Events (comma-separated)</Label>
            <Input
              id="wh-events"
              value={newWebhookEvents}
              onChange={(e) => setNewWebhookEvents(e.target.value)}
            />
          </div>
          <Button onClick={createWebhook} disabled={creatingWebhook}>
            {creatingWebhook ? "Creating..." : "Create webhook"}
          </Button>

          {createdWebhookSecretOnce ? (
            <div className="rounded-md bg-muted p-3 font-mono text-xs break-all">
              {createdWebhookSecretOnce}
            </div>
          ) : null}
        </div>

        <div className="rounded-lg border divide-y">
          {webhooks.length === 0 ? (
            <div className="p-4 text-sm text-muted-foreground">No webhooks yet.</div>
          ) : (
            webhooks.map((w) => (
              <div key={w.id} className="p-4 flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <div className="font-medium truncate">{w.url}</div>
                  <div className="text-xs text-muted-foreground truncate">
                    Events: {w.events.join(", ")}
                  </div>
                </div>
                <Button asChild variant="secondary" size="sm">
                  <Link href={`/settings/developer/webhooks/${w.id}`}>Logs</Link>
                </Button>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}

