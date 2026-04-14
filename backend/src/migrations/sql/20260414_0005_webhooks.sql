-- Webhooks + delivery logs
-- Events (suggested):
-- - task.processing_started
-- - task.processing_completed
-- - task.processing_failed
-- - clip.generated

CREATE TABLE IF NOT EXISTS webhooks (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    events TEXT[] NOT NULL DEFAULT '{}',
    enabled BOOLEAN NOT NULL DEFAULT true,
    secret TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_webhooks_user_id ON webhooks(user_id);
CREATE INDEX IF NOT EXISTS idx_webhooks_user_enabled ON webhooks(user_id, enabled);
CREATE INDEX IF NOT EXISTS idx_webhooks_events_gin ON webhooks USING GIN (events);

CREATE TABLE IF NOT EXISTS webhook_deliveries (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    webhook_id VARCHAR(36) NOT NULL REFERENCES webhooks(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event TEXT NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending|success|failed
    attempt INTEGER NOT NULL DEFAULT 1,
    response_status INTEGER,
    response_body TEXT,
    last_error TEXT,
    delivered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_webhook_deliveries_webhook_id ON webhook_deliveries(webhook_id);
CREATE INDEX IF NOT EXISTS idx_webhook_deliveries_user_created ON webhook_deliveries(user_id, created_at DESC);

-- === Row Level Security (RLS) policies ===
ALTER TABLE webhooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhooks FORCE ROW LEVEL SECURITY;
ALTER TABLE webhook_deliveries ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhook_deliveries FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS webhooks_owner_select ON webhooks;
DROP POLICY IF EXISTS webhooks_owner_insert ON webhooks;
DROP POLICY IF EXISTS webhooks_owner_update ON webhooks;
DROP POLICY IF EXISTS webhooks_owner_delete ON webhooks;

CREATE POLICY webhooks_owner_select
ON webhooks
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY webhooks_owner_insert
ON webhooks
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY webhooks_owner_update
ON webhooks
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY webhooks_owner_delete
ON webhooks
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

DROP POLICY IF EXISTS webhook_deliveries_owner_select ON webhook_deliveries;
DROP POLICY IF EXISTS webhook_deliveries_owner_insert ON webhook_deliveries;
DROP POLICY IF EXISTS webhook_deliveries_owner_update ON webhook_deliveries;
DROP POLICY IF EXISTS webhook_deliveries_owner_delete ON webhook_deliveries;

CREATE POLICY webhook_deliveries_owner_select
ON webhook_deliveries
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY webhook_deliveries_owner_insert
ON webhook_deliveries
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY webhook_deliveries_owner_update
ON webhook_deliveries
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY webhook_deliveries_owner_delete
ON webhook_deliveries
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);
