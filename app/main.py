from app.database import init_db
from app.crud import create_task, get_all_tasks, delete_task, update_task

def main():
    init_db()
    print("Task Manager CLI")
    while True:
        print("\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            description = input("Description (optional): ")
            create_task(title, description or None)
            print("Task added.")
        elif choice == "2":
            tasks = get_all_tasks()
            for task in tasks:
                print(task)
        elif choice == "3":
            task_id = int(input("Task ID: "))
            delete_task(task_id)
            print("Task deleted.")
        elif choice == "4":
            task_id = int(input("Task ID: "))
            title = input("New Title (leave blank to keep current): ")
            description = input("New Description (leave blank to keep current): ")
            done_raw = input("Mark as done? 0/1 (leave blank to keep current): ")
            done = int(done_raw) if done_raw in ("0", "1") else None
            update_task(task_id, title or None, description or None, done)
            print("Task updated.")
        elif choice == "5":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()