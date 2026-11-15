# Project instructions

Task manager CRUD in Python 3.9+ (SQLite, pytest). It is a learning project:
the same functionality is implemented several times, in different styles, on
purpose. Keep those implementations equal in behavior.

## Rule 1: Linting

- Linter and formatter: **ruff**. Configuration lives in `pyproject.toml`; do not
  override it with inline settings, and do not add other linters or formatters.
- Before finishing any change, run all three and fix what they report:

  ```bash
  ruff check .
  ruff format --check .
  pytest
  ```

- Use `ruff format .` to fix formatting. Do not hand-format.
- Do not silence a warning with `# noqa` unless there is a short reason in the
  same comment.
- Target Python 3.9: use `Optional[X]` / `List[X]` from `typing`, not `X | None`
  or `list[X]` in annotations.

## Rule 2: Feature parity between modules

Every user-facing feature (a new command, field, validation, message) must be
added to **all** modules below in the **same change**. Modules differ only in
*how* they do it, never in *what* they do.

| Module | Files | Storage |
|---|---|---|
| Functional, SQLite | `app/main.py`, `app/functional/crud.py` | SQLite |
| Functional, JSON | `app/functional/json_io.py` | `tasks.json` |
| OOP | `app/class_main.py`, `app/cli.py`, `app/oop/` | SQLite |

- Each module keeps its own storage and style. The JSON module stays on JSON,
  the functional one stays functions, the OOP one stays classes.
- Same names where the style allows it (`create_task`, `update_task`, ...), same
  validation rules, same user-visible messages.
- Every module gets its own tests in the mirrored path under `tests/`.
- When adding something to one module, check the others first and list in your
  answer which ones you changed. If a module cannot get the feature, say so
  explicitly; never skip it silently.
- A database schema change (`app/database.py`) must be reflected in the JSON
  module's data shape too.

## Conventions

- All SQL lives in `app/oop/task_repository.py` (OOP) or `app/functional/crud.py`
  (functional). Use `?` placeholders; never build SQL with f-strings.
- Open connections with `closing(get_connection(db_path))`.
- Pass the database path through the constructor / argument. Tests use `tmp_path`
  and must never touch the real `tasks.db` or `tasks.json`.
- Validation of a task lives in `Task.__post_init__` (OOP); other layers reuse it.
- Run the app as a module from the project root: `python -m app.main`,
  `python -m app.class_main`, `python -m app.cli`.
- Type-annotate new functions. Comments explain *why*, not *what*. Write code,
  comments and docstrings in English.
- Update `README.md` (structure, usage) when behavior or files change.
