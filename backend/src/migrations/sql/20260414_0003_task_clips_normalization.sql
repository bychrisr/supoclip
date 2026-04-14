-- Normalize tasks.generated_clips_ids into a relational table.
--
-- Goals:
-- - Create task_clips(task_id, clip_id, position)
-- - Backfill from tasks.generated_clips_ids (preserving order)
-- - Backfill from generated_clips as a safety net
-- - Enable RLS with the same ownership semantics as generated_clips (via owning task)
--
-- NOTE: We keep tasks.generated_clips_ids for now for backward compatibility.

CREATE TABLE IF NOT EXISTS task_clips (
    task_id VARCHAR(36) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    clip_id VARCHAR(36) NOT NULL REFERENCES generated_clips(id) ON DELETE CASCADE,
    position INTEGER NOT NULL CHECK (position >= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_id, clip_id),
    UNIQUE (task_id, position)
);

CREATE INDEX IF NOT EXISTS idx_task_clips_task_id ON task_clips(task_id);
CREATE INDEX IF NOT EXISTS idx_task_clips_clip_id ON task_clips(clip_id);

-- Backfill from legacy array (preserve order with ordinality).
INSERT INTO task_clips (task_id, clip_id, position, created_at)
SELECT
    t.id AS task_id,
    x.clip_id AS clip_id,
    x.position AS position,
    NOW()
FROM tasks t
JOIN LATERAL unnest(t.generated_clips_ids) WITH ORDINALITY AS x(clip_id, position)
    ON t.generated_clips_ids IS NOT NULL
ON CONFLICT (task_id, clip_id) DO NOTHING;

-- Safety net: backfill from generated_clips when task_clips is empty.
INSERT INTO task_clips (task_id, clip_id, position, created_at)
SELECT
    gc.task_id,
    gc.id AS clip_id,
    COALESCE(gc.clip_order, 1) AS position,
    NOW()
FROM generated_clips gc
WHERE NOT EXISTS (
    SELECT 1 FROM task_clips tc WHERE tc.task_id = gc.task_id
)
ON CONFLICT (task_id, clip_id) DO NOTHING;

-- RLS
ALTER TABLE task_clips ENABLE ROW LEVEL SECURITY;
ALTER TABLE task_clips FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS task_clips_via_task_owner_select ON task_clips;
DROP POLICY IF EXISTS task_clips_via_task_owner_insert ON task_clips;
DROP POLICY IF EXISTS task_clips_via_task_owner_update ON task_clips;
DROP POLICY IF EXISTS task_clips_via_task_owner_delete ON task_clips;

CREATE POLICY task_clips_via_task_owner_select
ON task_clips
FOR SELECT
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = task_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY task_clips_via_task_owner_insert
ON task_clips
FOR INSERT
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = task_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY task_clips_via_task_owner_update
ON task_clips
FOR UPDATE
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = task_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
)
WITH CHECK (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = task_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

CREATE POLICY task_clips_via_task_owner_delete
ON task_clips
FOR DELETE
USING (
  current_setting('app.internal', true) = '1'
  OR EXISTS (
    SELECT 1
    FROM tasks t
    WHERE t.id = task_clips.task_id
      AND t.user_id = NULLIF(current_setting('app.user_id', true), '')
  )
);

