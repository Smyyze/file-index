"""DuckDB schema definition for the file index."""

import duckdb


def init_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Create tables and indexes if they don't exist."""
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS file_index_id_seq START 1;
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_index (
            id          INTEGER PRIMARY KEY DEFAULT nextval('file_index_id_seq'),
            name        TEXT NOT NULL,
            path        TEXT NOT NULL UNIQUE,
            type        TEXT,           -- 'script', 'doc', 'config', 'data'
            category    TEXT,           -- 'projects', 'research', 'life-ops'
            tags        TEXT[],         -- Array of tags
            description TEXT,
            quick_command TEXT,
            related_files TEXT[],
            created     TIMESTAMP,
            modified    TIMESTAMP,
            size_kb     DOUBLE
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_path     ON file_index(path)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_modified ON file_index(modified)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_type     ON file_index(type)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_category ON file_index(category)
    """)
