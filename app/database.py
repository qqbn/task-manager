import sqlite3

DB_PATH = "tasks.db"


# db_path=None means "use the default DB_PATH".
# Why: the function-based version (crud.py) calls get_connection() without
# arguments and keeps working unchanged, while the class-based version can
# pass its own path (e.g. a temporary one in tests). One function serves both.
def get_connection(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_connection(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
