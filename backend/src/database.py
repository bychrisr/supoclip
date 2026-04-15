import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://localhost:5432/supoclip")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base class for all models
class Base(DeclarativeBase):
    pass


async def set_rls_context(
    db: AsyncSession, *, user_id: str | None, internal: bool
) -> None:
    """
    Set Postgres session-local settings used by RLS policies.

    - app.user_id: authenticated user id (or empty)
    - app.internal: '1' enables internal bypass in policies
    """
    await db.execute(
        text("SELECT set_config('app.user_id', :user_id, true)"),
        {"user_id": user_id or ""},
    )
    await db.execute(
        text("SELECT set_config('app.internal', :internal, true)"),
        {"internal": "1" if internal else "0"},
    )


def _split_sql_statements(sql: str) -> list[str]:
    """
    Split a SQL file into statements safe for asyncpg.

    Handles:
    - semicolons inside single/double quotes
    - dollar-quoted blocks (DO $$ ... $$;)
    - line comments (-- ...)
    - block comments (/* ... */)
    """
    out: list[str] = []
    buf: list[str] = []
    i = 0
    n = len(sql)

    in_single = False
    in_double = False
    in_line_comment = False
    in_block_comment = False
    dollar_tag: str | None = None

    def flush():
        stmt = "".join(buf).strip()
        buf.clear()
        if stmt:
            out.append(stmt)

    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""

        if in_line_comment:
            buf.append(ch)
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue

        if in_block_comment:
            buf.append(ch)
            if ch == "*" and nxt == "/":
                buf.append(nxt)
                i += 2
                in_block_comment = False
            else:
                i += 1
            continue

        # Start comments (only when not inside quotes/dollar)
        if not in_single and not in_double and dollar_tag is None:
            if ch == "-" and nxt == "-":
                buf.append(ch)
                buf.append(nxt)
                i += 2
                in_line_comment = True
                continue
            if ch == "/" and nxt == "*":
                buf.append(ch)
                buf.append(nxt)
                i += 2
                in_block_comment = True
                continue

        # Dollar-quote open/close (only when not in single/double quotes)
        if not in_single and not in_double:
            if dollar_tag is None and ch == "$":
                # parse tag: $tag$
                j = i + 1
                while j < n and sql[j] != "$":
                    j += 1
                if j < n and sql[j] == "$":
                    tag = sql[i : j + 1]  # includes both $
                    dollar_tag = tag
                    buf.append(tag)
                    i = j + 1
                    continue
            elif dollar_tag is not None and ch == "$":
                if sql.startswith(dollar_tag, i):
                    buf.append(dollar_tag)
                    i += len(dollar_tag)
                    dollar_tag = None
                    continue

        if dollar_tag is None:
            if ch == "'" and not in_double:
                # handle escaped '' within strings
                if in_single and nxt == "'":
                    buf.append(ch)
                    buf.append(nxt)
                    i += 2
                    continue
                in_single = not in_single
                buf.append(ch)
                i += 1
                continue
            if ch == '"' and not in_single:
                in_double = not in_double
                buf.append(ch)
                i += 1
                continue

        # Statement terminator
        if ch == ";" and not in_single and not in_double and dollar_tag is None:
            flush()
            i += 1
            continue

        buf.append(ch)
        i += 1

    flush()
    return out


# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )

        migrations_dir = Path(__file__).parent / "migrations" / "sql"
        if migrations_dir.exists():
            files = sorted([p for p in migrations_dir.glob("*.sql") if p.is_file()])
            for migration_file in files:
                version = migration_file.name
                already_applied = await conn.execute(
                    text(
                        "SELECT 1 FROM schema_migrations WHERE version = :version LIMIT 1"
                    ),
                    {"version": version},
                )
                if already_applied.scalar() is not None:
                    continue

                sql = migration_file.read_text()
                for statement in _split_sql_statements(sql):
                    await conn.execute(text(statement))
                await conn.execute(
                    text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                    {"version": version},
                )


# Close database connections
async def close_db():
    await engine.dispose()
