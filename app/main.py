import logging

from app.database import init_db
from app.functional.crud import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task,
    update_task,
)

logger = logging.getLogger(__name__)


def _ask_done(prompt, default=None):
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


def main():
    init_db()
    print("Task Manager CLI")
    while True:
        print(
            "\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task"
            "\n5. Mark task done\n6. Stats\n7. Exit"
        )
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            if not title.strip():
                logger.warning("Task title cannot be empty.")
                continue
            description = input("Description (optional): ")
            done = _ask_done("Done (0/1) [0]: ", default=0)
            priority = _ask_priority(
                "Priority (low/normal/high) [normal]: ",
                "normal",
            )
            create_task(title, description or None, priority, done=done)
            logger.info("Task added.")
        elif choice == "2":
            tasks = get_all_tasks()
            if not tasks:
                logger.info("No tasks found.")
            else:
                for task in tasks:
                    print(task)
        elif choice == "3":
            try:
                task_id = int(input("Task ID: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if delete_task(task_id):
                logger.info("Task deleted.")
            else:
                logger.warning("Task not found.")
        elif choice == "4":
            try:
                task_id = int(input("Task ID: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if get_task(task_id) is None:
                logger.warning("Task not found.")
                continue
            title = input("New Title (leave blank to keep current): ")
            description = input("New Description (leave blank to keep current): ")
            done = _ask_done("Mark as done? 0/1 (leave blank to keep current): ")
            priority = _ask_priority(
                "New Priority (low/normal/high, leave blank to keep current): "
            )
            if update_task(
                task_id,
                title or None,
                description or None,
                done,
                priority,
            ):
                logger.info("Task updated.")
            else:
                logger.warning("Task not found.")
        elif choice == "5":
            try:
                task_id = int(input("Task ID: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if update_task(task_id, done=1):
                logger.info("Task marked as done.")
            else:
                logger.warning("Task not found.")
        elif choice == "6":
            from app.functional.crud import get_stats

            stats = get_stats()
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
