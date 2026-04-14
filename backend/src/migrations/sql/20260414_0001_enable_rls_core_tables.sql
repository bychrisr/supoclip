-- Enable Row Level Security for security-critical tables.
--
-- This repo uses a single DB role (no per-user DB roles). RLS is enforced via a
-- session-local GUC set by the backend/worker:
--   SELECT set_config('app.user_id', '<uuid>', true);
--   SELECT set_config('app.internal', '0|1', true);
--
-- Policies use current_setting('app.user_id', true) and allow an internal
-- maintenance bypass when app.internal='1' (used by worker startup sweep).

-- === tasks ===
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

-- === sources ===
-- sources has no user_id (scoped via owning tasks).
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

-- Allow inserts for authenticated app contexts (source rows are still not readable
-- unless linked to an owned task).
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

-- === generated_clips ===
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

