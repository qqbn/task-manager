import argparse
import logging

from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository

logger = logging.getLogger(__name__)


def _non_empty(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("value cannot be empty")
    return value


def create_parser():
    parser = argparse.ArgumentParser(description="Manage tasks.")
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="Add a task")
    add_command.add_argument("title", type=_non_empty)
    add_command.add_argument("--description")

    commands.add_parser("list", help="List all tasks")

    update_command = commands.add_parser("update", help="Update a task")
    update_command.add_argument("task_id", type=int)
    update_command.add_argument("--title", type=_non_empty)
    update_command.add_argument("--description")
    update_command.add_argument("--done", choices=("0", "1"))

    delete_command = commands.add_parser("delete", help="Delete a task")
    delete_command.add_argument("task_id", type=int)

    return parser


def main(argv=None, tasks=None):
    parser = create_parser()
    args = parser.parse_args(argv)
    tasks = tasks if tasks is not None else TaskRepository()
    init_db(tasks.db_path)

    if args.command == "add":
        task = tasks.create_task(Task(args.title, args.description))
        logger.info("Task added. ID: %s", task.id)
    elif args.command == "list":
        all_tasks = tasks.get_all_tasks()
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
        ):
            logger.info("Task updated.")
        else:
            logger.warning("Task not found.")
    elif args.command == "delete":
        if tasks.delete_task(args.task_id):
            logger.info("Task deleted.")
        else:
            logger.warning("Task not found.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
