CREATE TABLE IF NOT EXISTS user_limits (
    user_id VARCHAR(36) NOT NULL,
    scope VARCHAR(40) NOT NULL,
    limit_per_minute INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, scope)
);

CREATE INDEX IF NOT EXISTS idx_user_limits_scope ON user_limits(scope);

