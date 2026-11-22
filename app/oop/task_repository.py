import sqlite3
from contextlib import closing
from typing import List, Optional

from app.database import DB_PATH, get_connection
from app.oop.task import Task
from app.validation import validate_description, validate_title


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
                """
                INSERT INTO tasks (title, description, done, priority)
                VALUES (?, ?, ?, ?)
                """,
                (task.title, task.description, task.done, task.priority),
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
            priority=task.priority,
        )

    def get_all_tasks(self) -> List[Task]:
        with closing(get_connection(self.db_path)) as connection:
            rows = connection.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [self._task_from_row(row) for row in rows]

    def get_tasks_by_done(self, done: bool) -> List[Task]:
        with closing(get_connection(self.db_path)) as connection:
            rows = connection.execute(
                "SELECT * FROM tasks WHERE done = ? ORDER BY id",
                (int(done),),
            ).fetchall()
        return [self._task_from_row(row) for row in rows]

    def get_stats(self) -> dict:
        tasks = self.get_all_tasks()
        completed = sum(1 for task in tasks if task.done)
        return {
            "total": len(tasks),
            "completed": completed,
            "pending": len(tasks) - completed,
        }

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
        priority: Optional[str] = None,
    ) -> bool:
        if title is not None:
            validate_title(title)
        validate_description(description)
        if priority is not None and priority not in ("low", "normal", "high"):
            raise ValueError("Priority must be low, normal or high")
        with closing(get_connection(self.db_path)) as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET title = COALESCE(?, title),
                    description = COALESCE(?, description),
                    done = COALESCE(?, done),
                    priority = COALESCE(?, priority)
                WHERE id = ?
                """,
                (title, description, done, priority, task_id),
            )
            connection.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        with closing(get_connection(self.db_path)) as connection:
            cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
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
            priority=row["priority"] if row["priority"] else "normal",
        )
