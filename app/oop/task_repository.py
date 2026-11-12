import sqlite3
from contextlib import closing
from typing import List, Optional

from app.database import DB_PATH, get_connection
from app.oop.task import Task


class TaskRepository:
    """Reads and writes Task objects in a SQLite database.

    All SQL knowledge lives here. The rest of the program just asks for
    tasks and never needs to know that SQLite is underneath.
    """

    # Constructor: the repository receives the database path and REMEMBERS it
    # as an attribute (self.db_path). This is the object's "state".
    # Why this instead of a global variable:
    #  - it is explicit which database we are working with,
    #  - tests pass a temporary file, so the real data can never be deleted
    #    (no monkeypatch needed),
    #  - two repositories can work on two databases at the same time.
    # DB_PATH is the default, so TaskRepository() works as before.
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def create_task(self, task: Task) -> Task:
        with closing(get_connection(self.db_path)) as connection:
            cursor = connection.execute(
                "INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)",
                (task.title, task.description, task.done),
            )
            connection.commit()
            task_id = cursor.lastrowid

        if task_id is None:
            raise RuntimeError("SQLite did not return an ID for the new task.")

        return Task(
            id=task_id,
            title=task.title,
            description=task.description,
            done=task.done,
        )

    def get_all_tasks(self) -> List[Task]:
        with closing(get_connection(self.db_path)) as connection:
            rows = connection.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [self._task_from_row(row) for row in rows]

    def get_task(self, task_id: int) -> Optional[Task]:
        with closing(get_connection(self.db_path)) as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
        return self._task_from_row(row) if row else None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        done: Optional[bool] = None,
    ) -> bool:
        with closing(get_connection(self.db_path)) as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET title = COALESCE(?, title),
                    description = COALESCE(?, description),
                    done = COALESCE(?, done)
                WHERE id = ?
                """,
                (title, description, done, task_id),
            )
            connection.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        with closing(get_connection(self.db_path)) as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?", (task_id,)
            )
            connection.commit()
            return cursor.rowcount > 0

    # @staticmethod: this method does not need `self` (it reads no object
    # attributes), so it is a plain helper function kept inside the class.
    # The `_` prefix is a convention: "internal, do not call from outside".
    # It is the only place that knows the DB stores `done` as 0/1 while we
    # want a bool.
    @staticmethod
    def _task_from_row(row: sqlite3.Row) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            done=bool(row["done"]),
        )
