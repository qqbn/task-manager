import pytest

from app import database
from app.oop.task import Task
from app.oop.task_repository import TaskRepository


@pytest.fixture
def repository(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "tasks.db"))
    database.init_db()
    return TaskRepository()


def test_create_and_list_task(repository):
    created = repository.create_task(Task("Test task", "Opis"))

    tasks = repository.get_all_tasks()

    assert created.id is not None
    assert tasks == [created]
    assert tasks[0].done is False


def test_get_task_returns_none_for_missing_id(repository):
    assert repository.get_task(999) is None


def test_update_task_changes_selected_fields(repository):
    task = repository.create_task(Task("Stary tytuł", "Stary opis"))
    task_id = task.id
    assert task_id is not None

    updated = repository.update_task(
        task_id,
        title="Nowy tytuł",
        description="Nowy opis",
        done=True,
    )

    assert updated is True
    assert repository.get_task(task_id) == Task(
        "Nowy tytuł", "Nowy opis", done=True, id=task_id
    )


def test_delete_task(repository):
    task = repository.create_task(Task("Do usunięcia"))
    task_id = task.id
    assert task_id is not None

    assert repository.delete_task(task_id) is True
    assert repository.get_task(task_id) is None
    assert repository.delete_task(task_id) is False


def test_class_cli_adds_a_task(repository, monkeypatch):
    answers = iter(["1", "CLI task", "Opis", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.class_main import main

    main()

    assert repository.get_all_tasks() == [Task("CLI task", "Opis", id=1)]
