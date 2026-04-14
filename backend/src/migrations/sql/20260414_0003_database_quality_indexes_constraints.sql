-- Story 1.3 (Sprint 4): Database Quality — Indexes + Constraints
-- Focus tasks: 1.3.1–1.3.12 and covering indexes 1.3.25–1.3.27

-- === 1.3.1 session.expiresAt ===
CREATE INDEX IF NOT EXISTS idx_session_expiresAt ON session ("expiresAt");

-- === 1.3.2 tasks(user_id, status) ===
CREATE INDEX IF NOT EXISTS idx_tasks_user_id_status ON tasks (user_id, status);

-- === 1.3.3 tasks(user_id, created_at DESC) ===
CREATE INDEX IF NOT EXISTS idx_tasks_user_id_created_at_desc ON tasks (user_id, created_at DESC);

-- === 1.3.4 generated_clips(task_id, clip_order) ===
CREATE INDEX IF NOT EXISTS idx_generated_clips_task_id_clip_order ON generated_clips (task_id, clip_order);

-- === 1.3.5 generated_clips(virality_score DESC) ===
CREATE INDEX IF NOT EXISTS idx_generated_clips_virality_score_desc ON generated_clips (virality_score DESC);

-- === 1.3.6 sources.type ===
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources (type);

-- === 1.3.7 processing_cache(source_type, created_at) ===
CREATE INDEX IF NOT EXISTS idx_processing_cache_source_type_created_at
ON processing_cache (source_type, created_at DESC);

-- === 1.3.8 stripe_webhook_events.created_at ===
CREATE INDEX IF NOT EXISTS idx_stripe_webhook_events_created_at
ON stripe_webhook_events (created_at DESC);

-- === 1.3.9 stripe_webhook_events.type ===
CREATE INDEX IF NOT EXISTS idx_stripe_webhook_events_type
ON stripe_webhook_events (type);

-- === 1.3.10 account.providerId + account.accountId ===
CREATE INDEX IF NOT EXISTS idx_account_providerId ON account ("providerId");
CREATE INDEX IF NOT EXISTS idx_account_accountId ON account ("accountId");

-- === 1.3.11 UNIQUE account(providerId, accountId) ===
-- Create a unique index first (idempotent), then attach it as a named constraint.
CREATE UNIQUE INDEX IF NOT EXISTS ux_account_providerId_accountId
ON account ("providerId", "accountId");

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'account_providerId_accountId_unique'
  ) THEN
    ALTER TABLE account
      ADD CONSTRAINT account_providerId_accountId_unique
      UNIQUE USING INDEX ux_account_providerId_accountId;
  END IF;
END $$;

-- === 1.3.12 UNIQUE verification(identifier, value) ===
CREATE UNIQUE INDEX IF NOT EXISTS ux_verification_identifier_value
ON verification (identifier, value);

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'verification_identifier_value_unique'
  ) THEN
    ALTER TABLE verification
      ADD CONSTRAINT verification_identifier_value_unique
      UNIQUE USING INDEX ux_verification_identifier_value;
  END IF;
END $$;

-- === 1.3.26 Covering index: task list (user_id, status, created_at) ===
-- Supports common pattern: WHERE user_id=? [AND status=?] ORDER BY created_at DESC
-- INCLUDE allows index-only scans for lightweight projections (e.g. list views).
CREATE INDEX IF NOT EXISTS idx_tasks_cover_user_status_created_at_desc
ON tasks (user_id, status, created_at DESC)
INCLUDE (id, source_id);

-- === 1.3.27 Covering index: clip list (task_id, clip_order, id) ===
-- Supports: WHERE task_id=? ORDER BY clip_order ASC (stable tie-break via id)
CREATE INDEX IF NOT EXISTS idx_generated_clips_cover_task_clip_order_id
ON generated_clips (task_id, clip_order, id);

