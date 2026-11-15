import pytest

from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository


@pytest.fixture
def repository(tmp_path):
    db_path = str(tmp_path / "tasks.db")
    init_db(db_path)
    return TaskRepository(db_path)


def test_cli_adds_and_lists_task(repository, caplog, capsys):
    from app.cli import main

    caplog.set_level("INFO", logger="app.cli")
    main(["add", "CLI task", "--description", "Opis"], repository)
    assert "Task added. ID: 1" in caplog.text

    main(["list"], repository)

    assert repository.get_all_tasks() == [Task("CLI task", "Opis", id=1)]
    # The list is the program's output, so it goes to stdout, not the log.
    assert "CLI task" in capsys.readouterr().out


def test_cli_updates_and_deletes_task(repository, caplog):
    from app.cli import main

    caplog.set_level("INFO", logger="app.cli")
    task = repository.create_task(Task("Old title"))

    main(["update", str(task.id), "--title", "New title", "--done", "1"], repository)

    assert repository.get_task(task.id) == Task("New title", done=True, id=task.id)
    assert "Task updated." in caplog.text

    main(["delete", str(task.id)], repository)

    assert repository.get_task(task.id) is None
    assert "Task deleted." in caplog.text


def test_cli_logs_empty_list_and_missing_task_as_warning(repository, caplog):
    from app.cli import main

    caplog.set_level("INFO", logger="app.cli")

    main(["list"], repository)
    main(["delete", "404"], repository)

    records = [(record.levelname, record.getMessage()) for record in caplog.records]
    assert ("INFO", "No tasks found.") in records
    assert ("WARNING", "Task not found.") in records


def test_cli_rejects_invalid_done_value(repository):
    from app.cli import main

    with pytest.raises(SystemExit):
        main(["update", "1", "--done", "2"], repository)


def test_cli_rejects_empty_task_title(repository):
    from app.cli import main

    with pytest.raises(SystemExit):
        main(["add", "   "], repository)
