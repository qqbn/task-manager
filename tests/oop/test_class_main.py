import pytest

from app.database import init_db
from app.oop.task import Task
from app.oop.task_repository import TaskRepository


@pytest.fixture
def repository(tmp_path):
    db_path = str(tmp_path / "tasks.db")
    init_db(db_path)
    return TaskRepository(db_path)


def test_class_menu_reports_empty_list_and_rejects_empty_title(
    repository, monkeypatch, caplog
):
    answers = iter(["2", "1", "   ", "", "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.class_main import main

    caplog.set_level("INFO", logger="app.class_main")
    main(repository)

    assert repository.get_all_tasks() == []
    assert "No tasks found." in caplog.text
    assert "Task title cannot be empty." in caplog.text


def test_class_menu_reports_invalid_ids_and_retries_invalid_done(
    repository, monkeypatch, caplog
):
    task = repository.create_task(Task("Existing task"))
    answers = iter(
        [
            "3",
            "bad",
            "3",
            "404",
            "4",
            "bad",
            "4",
            "404",
            "4",
            str(task.id),
            "",
            "",
            "",
            "bad",
            "0",
            "7",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.class_main import main

    caplog.set_level("INFO", logger="app.class_main")
    main(repository)

    assert caplog.text.count("ID must be a number.") == 2
    assert caplog.text.count("Task not found.") == 2
    assert "Enter 0 or 1." in caplog.text
    assert repository.get_task(task.id) == Task("Existing task", done=False, id=task.id)


def test_class_menu_can_add_completed_task(repository, monkeypatch):
    answers = iter(["1", "Completed task", "", "1", "normal", "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.class_main import main

    main(repository)

    assert repository.get_all_tasks() == [Task("Completed task", done=True, id=1)]


def test_class_menu_rejects_overlong_description(repository, monkeypatch, caplog):
    answers = iter(["1", "Valid", "B" * 301, "0", "normal", "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.class_main import main

    caplog.set_level("INFO", logger="app.class_main")
    main(repository)

    assert repository.get_all_tasks() == []
    assert "Task description cannot be longer than 300 characters" in caplog.text
