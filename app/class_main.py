import logging

from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository

logger = logging.getLogger(__name__)


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
        print("\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            description = input("Description (optional): ")
            task = tasks.create_task(Task(title, description or None))
            logger.info("Task added. ID: %s", task.id)
        elif choice == "2":
            for task in tasks.get_all_tasks():
                print(task)
        elif choice == "3":
            task_id = int(input("Task ID: "))
            tasks.delete_task(task_id)
            logger.info("Task deleted.")
        elif choice == "4":
            task_id = int(input("Task ID: "))
            title = input("New Title (leave blank to keep current): ")
            description = input("New Description (leave blank to keep current): ")
            done_raw = input("Mark as done? 0/1 (leave blank to keep current): ")
            done = done_raw == "1" if done_raw in ("0", "1") else None
            tasks.update_task(
                task_id,
                title or None,
                description or None,
                done,
            )
            logger.info("Task updated.")
        elif choice == "5":
            break
        else:
            logger.warning("Invalid option")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
