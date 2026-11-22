import argparse
import logging

from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository
from app.validation import validate_description, validate_title

logger = logging.getLogger(__name__)


def _non_empty(value):
    try:
        validate_title(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return value


def _description(value):
    try:
        validate_description(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return value


def _priority(value):
    if value not in ("low", "normal", "high"):
        raise argparse.ArgumentTypeError("priority must be low, normal or high")
    return value


def create_parser():
    parser = argparse.ArgumentParser(description="Manage tasks.")
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="Add a task")
    add_command.add_argument("title", type=_non_empty)
    add_command.add_argument("--description", type=_description)
    add_command.add_argument("--priority", type=_priority, default="normal")
    add_command.add_argument("--done", choices=("0", "1"), default="0")

    list_command = commands.add_parser("list", help="List all tasks")
    list_command.add_argument("--done", choices=("0", "1"))

    update_command = commands.add_parser("update", help="Update a task")
    update_command.add_argument("task_id", type=int)
    update_command.add_argument("--title", type=_non_empty)
    update_command.add_argument("--description", type=_description)
    update_command.add_argument("--done", choices=("0", "1"))
    update_command.add_argument("--priority", type=_priority)

    delete_command = commands.add_parser("delete", help="Delete a task")
    delete_command.add_argument("task_id", type=int)

    done_command = commands.add_parser("done", help="Mark a task as done")
    done_command.add_argument("task_id", type=int)

    commands.add_parser("stats", help="Show task statistics")

    return parser


def main(argv=None, tasks=None):
    parser = create_parser()
    args = parser.parse_args(argv)
    tasks = tasks if tasks is not None else TaskRepository()
    init_db(tasks.db_path)

    if args.command == "add":
        task = tasks.create_task(
            Task(
                args.title,
                args.description,
                done=args.done == "1",
                priority=args.priority,
            )
        )
        logger.info("Task added. ID: %s", task.id)
    elif args.command == "list":
        if args.done is None:
            all_tasks = tasks.get_all_tasks()
        else:
            all_tasks = tasks.get_tasks_by_done(args.done == "1")
        if not all_tasks:
            logger.info("No tasks found.")
        for task in all_tasks:
            print(task)
    elif args.command == "update":
        done = None if args.done is None else args.done == "1"
        if tasks.update_task(
            args.task_id,
            title=args.title,
            description=args.description,
            done=done,
            priority=args.priority,
        ):
            logger.info("Task updated.")
        else:
            logger.warning("Task not found.")
    elif args.command == "delete":
        if tasks.delete_task(args.task_id):
            logger.info("Task deleted.")
        else:
            logger.warning("Task not found.")
    elif args.command == "done":
        if tasks.update_task(args.task_id, done=True):
            logger.info("Task marked as done.")
        else:
            logger.warning("Task not found.")
    elif args.command == "stats":
        stats = tasks.get_stats()
        print(f"Total: {stats['total']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
