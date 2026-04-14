-- Database initialization script for SupoClip
-- Create database schema with required tables

-- Enable UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (compatible with Prisma schema)
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    "emailVerified" BOOLEAN NOT NULL DEFAULT false,
    image VARCHAR(500),
    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    password_hash VARCHAR(255),
    -- Default font preferences
    default_font_family VARCHAR(100) DEFAULT 'TikTokSans-Regular',
    default_font_size INTEGER DEFAULT 24,
    default_font_color VARCHAR(7) DEFAULT '#FFFFFF',
    -- Monetization and billing fields
    is_admin BOOLEAN NOT NULL DEFAULT false,
    plan VARCHAR(20) NOT NULL DEFAULT 'free',
    subscription_status VARCHAR(20) NOT NULL DEFAULT 'inactive',
    stripe_customer_id VARCHAR(255) UNIQUE,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    billing_period_start TIMESTAMP WITH TIME ZONE,
    billing_period_end TIMESTAMP WITH TIME ZONE,
    trial_ends_at TIMESTAMP WITH TIME ZONE
);

-- Source table (created before tasks since tasks reference sources)
CREATE TABLE sources (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    type VARCHAR(20) CHECK (type IN ('youtube', 'video_url')) NOT NULL,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000),
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source_id VARCHAR(36) REFERENCES sources(id) ON DELETE SET NULL,
    generated_clips_ids VARCHAR(36)[], -- Array of clip IDs
    status VARCHAR(20) NOT NULL DEFAULT 'pending',

    -- Progress tracking fields
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    progress_message TEXT,

    -- Font customization fields
    font_family VARCHAR(100) DEFAULT 'TikTokSans-Regular',
    font_size INTEGER DEFAULT 24,
    font_color VARCHAR(7) DEFAULT '#FFFFFF', -- Hex color code

    -- Caption template and B-roll options
    caption_template VARCHAR(50) DEFAULT 'default',
    include_broll BOOLEAN DEFAULT false,
    processing_mode VARCHAR(20) NOT NULL DEFAULT 'fast',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    cache_hit BOOLEAN NOT NULL DEFAULT false,
    error_code VARCHAR(80),
    stage_timings_json TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Generated clips table
CREATE TABLE generated_clips (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    task_id VARCHAR(36) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    start_time VARCHAR(20) NOT NULL, -- MM:SS format
    end_time VARCHAR(20) NOT NULL,   -- MM:SS format
    duration FLOAT NOT NULL,         -- Duration in seconds
    text TEXT,                       -- Transcript text for this clip
    relevance_score FLOAT NOT NULL,
    reasoning TEXT,                  -- AI reasoning for selection
    clip_order INTEGER NOT NULL,     -- Order within the task

    -- Virality score breakdown
    virality_score INTEGER DEFAULT 0,
    hook_score INTEGER DEFAULT 0,
    engagement_score INTEGER DEFAULT 0,
    value_score INTEGER DEFAULT 0,
    shareability_score INTEGER DEFAULT 0,
    hook_type VARCHAR(50),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE processing_cache (
    cache_key VARCHAR(255) PRIMARY KEY,
    source_url TEXT NOT NULL,
    source_type VARCHAR(20) NOT NULL,
    video_path TEXT,
    transcript_text TEXT,
    analysis_json TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Billing records (per-task usage tracking)
CREATE TABLE IF NOT EXISTS billing_records (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id VARCHAR(36) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    minutes_processed INTEGER NOT NULL DEFAULT 0 CHECK (minutes_processed >= 0),
    source_url VARCHAR(1000),
    source_title VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Idempotency: one billing record per task.
CREATE UNIQUE INDEX IF NOT EXISTS ux_billing_records_task_id ON billing_records(task_id);

-- API keys (API-first programmatic access)
CREATE TABLE IF NOT EXISTS api_keys (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(64) NOT NULL,
    prefix VARCHAR(16) NOT NULL,
    name VARCHAR(120) NOT NULL,
    scopes TEXT[] NOT NULL DEFAULT '{}'::text[],
    last_used_at TIMESTAMP WITH TIME ZONE,
    revoked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_api_keys_user_prefix_unique
ON api_keys(user_id, prefix);

CREATE INDEX IF NOT EXISTS idx_api_keys_prefix
ON api_keys(prefix);

CREATE INDEX IF NOT EXISTS idx_api_keys_user_created
ON api_keys(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_api_keys_active_prefix
ON api_keys(prefix)
WHERE revoked_at IS NULL;

-- Webhooks + delivery logs
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
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    attempt INTEGER NOT NULL DEFAULT 1,
    response_status INTEGER,
    response_body TEXT,
    last_error TEXT,
    delivered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_webhook_deliveries_webhook_id ON webhook_deliveries(webhook_id);
CREATE INDEX IF NOT EXISTS idx_webhook_deliveries_user_created ON webhook_deliveries(user_id, created_at DESC);

-- Per-user rate/usage limits (used by backend)
CREATE TABLE IF NOT EXISTS user_limits (
    user_id VARCHAR(36) NOT NULL,
    scope VARCHAR(40) NOT NULL,
    limit_per_minute INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, scope)
);

-- Better Auth tables
CREATE TABLE session (
    id VARCHAR(36) PRIMARY KEY,
    "expiresAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    "ipAddress" VARCHAR(255),
    "userAgent" TEXT,
    "userId" VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE account (
    id VARCHAR(36) PRIMARY KEY,
    "accountId" VARCHAR(255) NOT NULL,
    "providerId" VARCHAR(255) NOT NULL,
    "userId" VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    "accessToken" TEXT,
    "refreshToken" TEXT,
    "idToken" TEXT,
    "accessTokenExpiresAt" TIMESTAMP WITH TIME ZONE,
    "refreshTokenExpiresAt" TIMESTAMP WITH TIME ZONE,
    scope TEXT,
    password TEXT,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE verification (
    id VARCHAR(36) PRIMARY KEY,
    identifier VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    "expiresAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    "createdAt" TIMESTAMP WITH TIME ZONE,
    "updatedAt" TIMESTAMP WITH TIME ZONE
);

-- Stripe webhook idempotency table
CREATE TABLE stripe_webhook_events (
    id VARCHAR(255) PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_source_id ON tasks(source_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_processing_mode ON tasks(processing_mode);
CREATE INDEX idx_tasks_completed_at ON tasks(completed_at);
CREATE INDEX idx_sources_created_at ON sources(created_at);
CREATE INDEX idx_processing_cache_source_url ON processing_cache(source_url);
CREATE INDEX IF NOT EXISTS idx_billing_records_user_id ON billing_records(user_id);
CREATE INDEX IF NOT EXISTS idx_billing_records_created_at ON billing_records(created_at);
CREATE INDEX IF NOT EXISTS idx_billing_records_user_created_at ON billing_records(user_id, created_at DESC);
CREATE INDEX idx_generated_clips_task_id ON generated_clips(task_id);
CREATE INDEX idx_generated_clips_clip_order ON generated_clips(clip_order);
CREATE INDEX idx_generated_clips_created_at ON generated_clips(created_at);
CREATE INDEX idx_session_token ON session(token);
CREATE INDEX idx_session_userId ON session("userId");
CREATE INDEX idx_account_userId ON account("userId");
CREATE INDEX idx_verification_identifier ON verification(identifier);
CREATE INDEX IF NOT EXISTS idx_user_limits_scope ON user_limits(scope);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create function for updatedAt column (Prisma format)
CREATE OR REPLACE FUNCTION update_updatedAt_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW."updatedAt" = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at and updatedAt
-- Users table only has "updatedAt" (Better Auth convention)
CREATE TRIGGER update_users_updatedAt BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updatedAt_column();

-- Tasks, sources, and generated_clips use snake_case updated_at
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sources_updated_at BEFORE UPDATE ON sources FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_generated_clips_updated_at BEFORE UPDATE ON generated_clips FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Better Auth tables use camelCase "updatedAt"
CREATE TRIGGER update_session_updatedAt BEFORE UPDATE ON session FOR EACH ROW EXECUTE FUNCTION update_updatedAt_column();
CREATE TRIGGER update_account_updatedAt BEFORE UPDATE ON account FOR EACH ROW EXECUTE FUNCTION update_updatedAt_column();
CREATE TRIGGER update_verification_updatedAt BEFORE UPDATE ON verification FOR EACH ROW EXECUTE FUNCTION update_updatedAt_column();

-- === Row Level Security (RLS) policies ===
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS tasks_owner_select ON tasks;
DROP POLICY IF EXISTS tasks_owner_insert ON tasks;
DROP POLICY IF EXISTS tasks_owner_update ON tasks;
DROP POLICY IF EXISTS tasks_owner_delete ON tasks;

CREATE POLICY tasks_owner_select
ON tasks
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY tasks_owner_insert
ON tasks
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY tasks_owner_update
ON tasks
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY tasks_owner_delete
ON tasks
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

ALTER TABLE billing_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE billing_records FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS billing_records_owner_select ON billing_records;
DROP POLICY IF EXISTS billing_records_owner_insert ON billing_records;
DROP POLICY IF EXISTS billing_records_owner_delete ON billing_records;

CREATE POLICY billing_records_owner_select
ON billing_records
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY billing_records_owner_insert
ON billing_records
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY billing_records_owner_delete
ON billing_records
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

-- === API keys RLS ===
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS api_keys_owner_select ON api_keys;
DROP POLICY IF EXISTS api_keys_owner_insert ON api_keys;
DROP POLICY IF EXISTS api_keys_owner_update ON api_keys;
DROP POLICY IF EXISTS api_keys_owner_delete ON api_keys;

CREATE POLICY api_keys_owner_select
ON api_keys
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY api_keys_owner_insert
ON api_keys
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY api_keys_owner_update
ON api_keys
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY api_keys_owner_delete
ON api_keys
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

-- === Webhooks RLS ===
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

ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE sources FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS sources_via_task_owner_select ON sources;
DROP POLICY IF EXISTS sources_via_task_owner_insert ON sources;
DROP POLICY IF EXISTS sources_via_task_owner_update ON sources;
DROP POLICY IF EXISTS sources_via_task_owner_delete ON sources;

CREATE POLICY sources_via_task_owner_select
ON sources
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.source_id = sources.id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY sources_via_task_owner_insert
ON sources
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR NULLIF(current_setting('app.user_id', true), '') IS NOT NULL
);

CREATE POLICY sources_via_task_owner_update
ON sources
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.source_id = sources.id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.source_id = sources.id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY sources_via_task_owner_delete
ON sources
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.source_id = sources.id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

ALTER TABLE generated_clips ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_clips FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS clips_via_task_owner_select ON generated_clips;
DROP POLICY IF EXISTS clips_via_task_owner_insert ON generated_clips;
DROP POLICY IF EXISTS clips_via_task_owner_update ON generated_clips;
DROP POLICY IF EXISTS clips_via_task_owner_delete ON generated_clips;

CREATE POLICY clips_via_task_owner_select
ON generated_clips
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = generated_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY clips_via_task_owner_insert
ON generated_clips
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = generated_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY clips_via_task_owner_update
ON generated_clips
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = generated_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = generated_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY clips_via_task_owner_delete
ON generated_clips
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = generated_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);
