ALTER TABLE processing_cache
ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP WITH TIME ZONE;

-- Backfill existing rows (best-effort) so cleanup can start immediately
UPDATE processing_cache
SET expires_at = created_at + (INTERVAL '1 second' * 604800)
WHERE expires_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_processing_cache_expires_at
ON processing_cache(expires_at);

-- Common lookup patterns
CREATE INDEX IF NOT EXISTS idx_processing_cache_source_type_created_at
ON processing_cache(source_type, created_at);

