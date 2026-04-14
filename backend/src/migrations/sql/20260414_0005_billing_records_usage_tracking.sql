-- Add billing_records table for per-task usage tracking.
-- Records one row per completed task (idempotent via UNIQUE(task_id)).

CREATE TABLE IF NOT EXISTS billing_records (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id VARCHAR(36) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    minutes_processed INTEGER NOT NULL DEFAULT 0 CHECK (minutes_processed >= 0),
    source_url VARCHAR(1000),
    source_title VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Idempotency: do not allow multiple records per task.
CREATE UNIQUE INDEX IF NOT EXISTS ux_billing_records_task_id ON billing_records(task_id);

CREATE INDEX IF NOT EXISTS idx_billing_records_user_id ON billing_records(user_id);
CREATE INDEX IF NOT EXISTS idx_billing_records_created_at ON billing_records(created_at);
CREATE INDEX IF NOT EXISTS idx_billing_records_user_created_at ON billing_records(user_id, created_at DESC);

-- === Row Level Security (RLS) policies ===
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

