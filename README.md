# Task Manager CRUD

This project is a simple CRUD application built in Python as a practice project for learning database operations, modular application structure, and Python development basics.

It is intended as a hands-on exercise for GH-300 and AI-300 certification preparation.

## Features

The application allows users to:

- add a new task,
- view all existing tasks,
- delete a task by ID,
- update a task,
- assign a priority (`low`, `normal`, or `high`),
- choose whether a task is already done when adding it,
- limit task titles to 200 characters and descriptions to 300 characters,
- mark a task as done,
- show task statistics,
- filter tasks by completion status,
- store data in a local SQLite database,
- run the app in a virtual environment.

## Project Structure

```text
task-manager/
├── app/
│   ├── __init__.py
│   ├── database.py          # shared SQLite connection + init
│   ├── main.py              # CLI entry point (function-based)
│   ├── class_main.py        # CLI entry point (class-based)
│   ├── functional/
│   │   ├── crud.py
│   │   └── json_io.py
│   └── oop/
│       ├── task.py
│       └── task_repository.py
├── tests/
│   ├── functional/
│   │   ├── test_crud.py
│   │   └── test_json_io.py
│   └── oop/
│       └── test_task_repository.py
├── requirements.txt
├── README.md
├── tasks.db
└── .venv/
```

## Output: `print` vs `logging`

- `print` is used for what the user asked to see: menus, prompts and the task list.
- `logging` (stderr) is used for status and problems: `Task added.`, `Task not found.`,
  `Invalid option`. Handlers are configured only in the `__main__` block of each entry point.
- The interactive menus warn about invalid IDs, empty titles, invalid completion
  values, and missing tasks; an empty task list is reported as an informational message.

## Technologies

- Python 3
- SQLite
- pytest

## Requirements

- Python 3.9 or newer
- pip
- virtual environment (venv)

## Installation

1. Open a terminal in the project directory.
2. Create a virtual environment:

```bash
python3 -m venv .venv
```

3. Activate the environment:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Application

From the project root, run:

```bash
python -m app.main
```

This command ensures the package is recognized correctly and the application starts as a module.

To run the class-based version, use:

```bash
python -m app.class_main
```

In this version, `Task` represents a task as a Python object, `TaskRepository`
handles SQLite operations, and `class_main.py` provides the CLI. The original
function-based version remains available in `crud.py` and `main.py` for
comparison.

To manage tasks with command-line arguments instead of the interactive menu,
use the argparse interface:

```bash
python -m app.cli add "Buy groceries" --description "Milk and bread"
python -m app.cli list
python -m app.cli list --done 1
python -m app.cli add "Call dentist" --priority high --done 1
python -m app.cli done 1
python -m app.cli stats
python -m app.cli update 1 --title "Buy groceries" --done 1 --priority normal
python -m app.cli delete 1
```

The argparse interface uses the same `TaskRepository` and `tasks.db` as the
class-based version. For `add`, `--done` accepts `0` (not done) or `1` (done)
and defaults to `0`. For update commands, omit any field that should remain
unchanged; there, `--done` also accepts `0` or `1`.

## Example Menu

When the app starts, the user sees the following menu:

```text
1. Add task
2. List tasks
3. Delete task
4. Update task
5. Exit
```

The user can then:

- add a task,
- list all tasks,
- delete a task by ID,
- update a task,
- exit the application.

## Database

The project uses SQLite and stores data in a file named `tasks.db`.

The `tasks` table contains:

- `id` — record identifier,
- `title` — task title, maximum 200 characters,
- `description` — optional task description, maximum 300 characters,
- `done` — task completion status (`0` or `1`).
- `priority` — `low`, `normal`, or `high`; defaults to `normal`.

## Testing

Run the test suite with:

```bash
pytest
```

## Possible Extensions

This project can be expanded with:

- updating existing tasks,
- marking tasks as complete,
- filtering tasks by title or status,
- adding creation/update timestamps,
- building a web interface,
- connecting to an external API.

## Summary

This is a small but practical Python project that demonstrates core CRUD operations, database interaction, project organization, and testing fundamentals. It is well suited for hands-on learning and certificate preparation.
