from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository


def main():
    init_db()
    tasks = TaskRepository()
    print("Task Manager CLI (class-based)")

    while True:
        print("\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            description = input("Description (optional): ")
            task = tasks.create_task(Task(title, description or None))
            print("Task added. ID:", task.id)
        elif choice == "2":
            for task in tasks.get_all_tasks():
                print(task)
        elif choice == "3":
            task_id = int(input("Task ID: "))
            tasks.delete_task(task_id)
            print("Task deleted.")
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
            print("Task updated.")
        elif choice == "5":
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
