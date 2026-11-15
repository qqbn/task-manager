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


def _ask_done(prompt):
    while True:
        value = input(prompt)
        if value == "":
            return None
        if value in ("0", "1"):
            return int(value)
        logger.warning("Enter 0 or 1.")


def main():
    init_db()
    print("Task Manager CLI")
    while True:
        print("\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            if not title.strip():
                logger.warning("Task title cannot be empty.")
                continue
            description = input("Description (optional): ")
            create_task(title, description or None)
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
            if update_task(task_id, title or None, description or None, done):
                logger.info("Task updated.")
            else:
                logger.warning("Task not found.")
        elif choice == "5":
            break
        else:
            logger.warning("Invalid option")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
