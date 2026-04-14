-- API keys for programmatic access (hashed-only storage).
--
-- Notes:
-- - Store ONLY a hash of the secret (key_hash) + a short prefix for lookup/logging.
-- - Lookup during authentication is done in an internal RLS context (app.internal=1)
--   because we don't know the user_id until the key is validated.
--
-- Columns:
-- - user_id: owner (matches users.id type: VARCHAR(36))
-- - key_hash: SHA-256 hex digest of (pepper + raw_secret)
-- - prefix: short public identifier (first 8 chars of secret); used for lookup
-- - name: user-provided label
-- - scopes: optional string list for future authorization layers (not enforced yet)
-- - last_used_at: best-effort updated on successful auth
-- - revoked_at: soft revoke timestamp
-- - created_at: creation timestamp

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

-- Uniqueness and lookup indexes
CREATE UNIQUE INDEX IF NOT EXISTS idx_api_keys_user_prefix_unique
ON api_keys(user_id, prefix);

CREATE INDEX IF NOT EXISTS idx_api_keys_prefix
ON api_keys(prefix);

CREATE INDEX IF NOT EXISTS idx_api_keys_user_created
ON api_keys(user_id, created_at DESC);

-- Fast "active key" filtering
CREATE INDEX IF NOT EXISTS idx_api_keys_active_prefix
ON api_keys(prefix)
WHERE revoked_at IS NULL;

-- RLS: only the owner can manage their keys (with internal bypass).
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

