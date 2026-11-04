import json

def main():
    print("JSON Func")

    while True:
        print("\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            tasks = get_all_tasks()
            new_id = max((t["id"] for t in tasks), default=0) + 1
            title = input("Title: ")
            description = input("Description (optional): ")
            new_task = {
                "id": new_id,
                "title": title,
                "description": description or None
            }
            tasks.append(new_task)
            save_all_tasks(tasks)
            print("Adding a new task.")
        elif choice == "2":
            tasks = get_all_tasks()
            for task in tasks:
                print(task)
        elif choice == "3":
            print("Task deleted.")
        elif choice == "4":
            print("Task updated.")
        elif choice == "5":
            break
        else:
            print("Invalid option")

def get_all_tasks():
    with open("tasks.json", "r") as file:
        return json.load(file)

def save_all_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()