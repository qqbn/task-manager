from app.database import get_connection

VALID_PRIORITIES = ("low", "normal", "high")


def create_task(title, description=None, priority="normal", db_path=None, done=0):
    if not title.strip():
        raise ValueError("Task title cannot be empty")
    if priority not in VALID_PRIORITIES:
        raise ValueError("Priority must be low, normal or high")
    conn = get_connection(db_path)
    cursor = conn.execute(
        """
        INSERT INTO tasks (title, description, done, priority)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, done, priority),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_all_tasks(db_path=None):
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task(task_id, db_path=None):
    conn = get_connection(db_path)
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_tasks_by_done(done, db_path=None):
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM tasks WHERE done = ? ORDER BY id",
        (int(done),),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats(db_path=None):
    tasks = get_all_tasks(db_path)
    completed = sum(1 for task in tasks if task["done"])
    return {
        "total": len(tasks),
        "completed": completed,
        "pending": len(tasks) - completed,
    }


def update_task(
    task_id,
    title=None,
    description=None,
    done=None,
    priority=None,
    db_path=None,
):
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError("Priority must be low, normal or high")
    conn = get_connection(db_path)
    cursor = conn.execute(
        "UPDATE tasks "
        "SET title = COALESCE(?, title), "
        "description = COALESCE(?, description), "
        "done = COALESCE(?, done), "
        "priority = COALESCE(?, priority) "
        "WHERE id = ?",
        (title, description, done, priority, task_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_task(task_id, db_path=None):
    conn = get_connection(db_path)
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
