# Task Manager CRUD

This project is a simple CRUD application built in Python as a practice project for learning database operations, modular application structure, and Python development basics.

It is intended as a hands-on exercise for GH-300 and AI-300 certification preparation.

## Features

The application allows users to:

- add a new task,
- view all existing tasks,
- delete a task by ID,
- store data in a local SQLite database,
- run the app in a virtual environment.

## Project Structure

```text
task-manager/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   └── main.py
├── tests/
│   └── test_crud.py
├── requirements.txt
├── README.md
├── tasks.db
└── .venv/
```

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

## Example Menu

When the app starts, the user sees the following menu:

```text
1. Add task
2. List tasks
3. Delete task
4. Exit
```

The user can then:

- add a task,
- list all tasks,
- delete a task by ID,
- exit the application.

## Database

The project uses SQLite and stores data in a file named `tasks.db`.

The `tasks` table contains:

- `id` — record identifier,
- `title` — task title,
- `description` — optional task description,
- `done` — task completion status (`0` or `1`).

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
