-- Add sources.user_id with FK to users.
--
-- Safe approach for existing databases:
-- - Add column as NULLable
-- - Backfill from tasks (pick earliest task owner per source)
-- - Add FK constraint as NOT VALID, then VALIDATE (avoids long locks)
-- - Update RLS policies to use sources.user_id directly (instead of via tasks)

ALTER TABLE sources ADD COLUMN IF NOT EXISTS user_id VARCHAR(36);

CREATE INDEX IF NOT EXISTS idx_sources_user_id ON sources(user_id);

-- Backfill: assign ownership based on earliest task that references the source.
UPDATE sources s
SET user_id = x.user_id
FROM (
    SELECT
        t.source_id,
        (array_agg(t.user_id ORDER BY t.created_at ASC))[1] AS user_id
    FROM tasks t
    WHERE t.source_id IS NOT NULL
    GROUP BY t.source_id
) x
WHERE s.id = x.source_id
  AND s.user_id IS NULL;

-- FK (nullable for now)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'sources_user_id_fkey'
  ) THEN
    ALTER TABLE sources
      ADD CONSTRAINT sources_user_id_fkey
      FOREIGN KEY (user_id) REFERENCES users(id)
      ON DELETE SET NULL
      NOT VALID;
  END IF;
END$$;

ALTER TABLE sources VALIDATE CONSTRAINT sources_user_id_fkey;

-- RLS: swap from "via tasks" to direct ownership.
DROP POLICY IF EXISTS sources_via_task_owner_select ON sources;
DROP POLICY IF EXISTS sources_via_task_owner_insert ON sources;
DROP POLICY IF EXISTS sources_via_task_owner_update ON sources;
DROP POLICY IF EXISTS sources_via_task_owner_delete ON sources;

DROP POLICY IF EXISTS sources_owner_select ON sources;
DROP POLICY IF EXISTS sources_owner_insert ON sources;
DROP POLICY IF EXISTS sources_owner_update ON sources;
DROP POLICY IF EXISTS sources_owner_delete ON sources;

CREATE POLICY sources_owner_select
ON sources
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY sources_owner_insert
ON sources
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY sources_owner_update
ON sources
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

CREATE POLICY sources_owner_delete
ON sources
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR user_id = NULLIF(current_setting('app.user_id', true), '')
);

