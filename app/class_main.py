import logging
from typing import Optional

from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository
from app.validation import validate_description, validate_title

logger = logging.getLogger(__name__)


def _ask_done(prompt: str, default: Optional[int] = None) -> Optional[int]:
    while True:
        value = input(prompt)
        if value == "":
            return default
        if value in ("0", "1"):
            return int(value)
        logger.warning("Enter 0 or 1.")


def _ask_priority(prompt, default=None):
    while True:
        value = input(prompt).strip().lower()
        if value == "":
            return default
        if value in ("low", "normal", "high"):
            return value
        logger.warning("Priority must be low, normal or high.")


# main() accepts a repository as an argument (it creates a default one).
# Why: the program is not hard-wired to a single database - a test can pass
# a repository that points to a temporary file. This is called dependency
# injection: an object receives what it needs from the outside.
def main(tasks=None):
    tasks = tasks or TaskRepository()
    # Create the table in the same DB the repository uses.
    init_db(tasks.db_path)
    print("Task Manager CLI (class-based)")

    while True:
        print(
            "\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task"
            "\n5. Mark task done\n6. Stats\n7. Exit"
        )
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            try:
                validate_title(title)
            except ValueError as error:
                logger.warning("%s", error)
                continue
            description = input("Description (optional): ")
            try:
                validate_description(description or None)
            except ValueError as error:
                logger.warning("%s", error)
                continue
            done = _ask_done("Done (0/1) [0]: ", default=0) == 1
            priority = _ask_priority(
                "Priority (low/normal/high) [normal]: ",
                "normal",
            )
            task = tasks.create_task(
                Task(title, description or None, done=done, priority=priority)
            )
            logger.info("Task added. ID: %s", task.id)
        elif choice == "2":
            all_tasks = tasks.get_all_tasks()
            if not all_tasks:
                logger.info("No tasks found.")
            else:
                for task in all_tasks:
                    print(task)
        elif choice == "3":
            try:
                task_id = int(input("Task ID: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if tasks.delete_task(task_id):
                logger.info("Task deleted.")
            else:
                logger.warning("Task not found.")
        elif choice == "4":
            try:
                task_id = int(input("Task ID: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if tasks.get_task(task_id) is None:
                logger.warning("Task not found.")
                continue
            title = input("New Title (leave blank to keep current): ")
            description = input("New Description (leave blank to keep current): ")
            priority = _ask_priority(
                "New Priority (low/normal/high, blank to keep current): "
            )
            done_value = _ask_done("Mark as done? 0/1 (leave blank to keep current): ")
            done = None if done_value is None else done_value == 1
            try:
                updated = tasks.update_task(
                    task_id,
                    title or None,
                    description or None,
                    done,
                    priority,
                )
            except ValueError as error:
                logger.warning("%s", error)
                continue
            if updated:
                logger.info("Task updated.")
            else:
                logger.warning("Task not found.")
        elif choice == "5":
            try:
                task_id = int(input("Task ID: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if tasks.update_task(task_id, done=True):
                logger.info("Task marked as done.")
            else:
                logger.warning("Task not found.")
        elif choice == "6":
            stats = tasks.get_stats()
            print(f"Total: {stats['total']}")
            print(f"Completed: {stats['completed']}")
            print(f"Pending: {stats['pending']}")
        elif choice == "7":
            break
        else:
            logger.warning("Invalid option")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
