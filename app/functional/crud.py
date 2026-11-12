from app.database import get_connection

def create_task(title, description=None):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, done) VALUES (?, ?, 0)",
        (title, description)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_all_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_task(task_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_task(task_id, title=None, description=None, done=None):
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE tasks SET title = COALESCE(?, title), description = COALESCE(?, description), done = COALESCE(?, done) WHERE id = ?",
        (title, description, done, task_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0