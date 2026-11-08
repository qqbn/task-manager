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
            done = ask_done("Done (0/1) [0]: ", default=0)
            new_task = {
                "id": new_id,
                "title": title,
                "description": description or None,
                "done": done
            }
            tasks.append(new_task)
            save_all_tasks(tasks)
            print("Adding a new task.")
        elif choice == "2":
            tasks = get_all_tasks()
            for task in tasks:
                print(task)
        elif choice == "3":
            id = input("Id of task: ")
            if delete_task(int(id)):
                print("Task deleted.")
            else:
                print("Task not found.")
        elif choice == "4":
            try:
                task_id = int(input("ID to update: "))
            except ValueError:
                print("ID must be a number.")
                continue

            task = get_task(task_id)
            if task is None:
                print("Task not found.")
                continue

            new_title = input(f"Title [{task['title']}]: ")
            new_description = input(f"Description [{task.get('description')}]: ")

            new_done = ask_done(f"Done (0/1) [{task.get('done')}]: ", default=None)

            update_task(task_id, new_title, new_description, new_done)
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

def delete_task(task_id):
    tasks = get_all_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        return False

    save_all_tasks(new_tasks)
    return True

def get_task(task_id):
    tasks = get_all_tasks()
    return next((t for t in tasks if t["id"] == task_id), None)

def ask_done(prompt, default):
    while True:
        value = input(prompt)
        if value == "":
            return default
        if value in ("0", "1"):
            return int(value)
        print("Enter 0 or 1.")

def update_task(task_id, title="", description="", done=None):
    tasks = get_all_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return False

    if title:
        task["title"] = title
    if description:
        task["description"] = description
    if done is not None:
        task["done"] = done

    save_all_tasks(tasks)
    return True

if __name__ == "__main__":
    main()