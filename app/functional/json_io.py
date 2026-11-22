import json
import logging

logger = logging.getLogger(__name__)
VALID_PRIORITIES = ("low", "normal", "high")


def main():
    print("JSON Func")

    while True:
        print(
            "\n1. Add task\n2. List tasks\n3. Delete task\n4. Update task"
            "\n5. Mark task done\n6. Stats\n7. Exit"
        )
        choice = input("Choose: ")

        if choice == "1":
            tasks = get_all_tasks()
            new_id = max((t["id"] for t in tasks), default=0) + 1
            title = input("Title: ")
            if not title.strip():
                logger.warning("Task title cannot be empty.")
                continue
            description = input("Description (optional): ")
            done = ask_done("Done (0/1) [0]: ", default=0)
            priority = ask_priority("Priority (low/normal/high) [normal]: ")
            new_task = {
                "id": new_id,
                "title": title,
                "description": description or None,
                "done": done,
                "priority": priority,
            }
            tasks.append(new_task)
            save_all_tasks(tasks)
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
                task_id = int(input("Id of task: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue
            if delete_task(task_id):
                logger.info("Task deleted.")
            else:
                logger.warning("Task not found.")
        elif choice == "4":
            try:
                task_id = int(input("ID to update: "))
            except ValueError:
                logger.warning("ID must be a number.")
                continue

            task = get_task(task_id)
            if task is None:
                logger.warning("Task not found.")
                continue

            new_title = input(f"Title [{task['title']}]: ")
            new_description = input(f"Description [{task.get('description')}]: ")

            new_done = ask_done(f"Done (0/1) [{task.get('done')}]: ", default=None)
            new_priority = ask_priority(
                "Priority (low/normal/high) [current]: ",
                default=None,
            )

            if update_task(
                task_id,
                new_title,
                new_description,
                new_done,
                new_priority,
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
            stats = get_stats()
            print(f"Total: {stats['total']}")
            print(f"Completed: {stats['completed']}")
            print(f"Pending: {stats['pending']}")
        elif choice == "7":
            break
        else:
            logger.warning("Invalid option")


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
        logger.warning("Enter 0 or 1.")


def ask_priority(prompt, default="normal"):
    while True:
        value = input(prompt).strip().lower()
        if value == "":
            return default
        if value in VALID_PRIORITIES:
            return value
        logger.warning("Priority must be low, normal or high.")


def update_task(task_id, title="", description="", done=None, priority=None):
    tasks = get_all_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return False
    if title and not title.strip():
        raise ValueError("Task title cannot be empty")
    if priority is not None and priority not in VALID_PRIORITIES:
        raise ValueError("Priority must be low, normal or high")

    if title:
        task["title"] = title
    if description:
        task["description"] = description
    if done is not None:
        task["done"] = done
    if priority is not None:
        task["priority"] = priority

    save_all_tasks(tasks)
    return True


def get_tasks_by_done(done):
    tasks = get_all_tasks()
    return [task for task in tasks if bool(task["done"]) == bool(done)]


def get_stats():
    tasks = get_all_tasks()
    completed = sum(1 for task in tasks if task["done"])
    return {
        "total": len(tasks),
        "completed": completed,
        "pending": len(tasks) - completed,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
