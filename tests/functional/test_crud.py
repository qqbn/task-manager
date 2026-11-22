import pytest

from app.database import init_db
from app.functional.crud import (
    create_task,
    delete_task,
    get_all_tasks,
    get_stats,
    get_task,
    get_tasks_by_done,
    update_task,
)


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "tasks.db")
    init_db(path)
    return path


def test_create_task_with_priority_and_stats(db_path):
    task_id = create_task("High task", "Opis", "high", db_path)

    task = get_task(task_id, db_path)
    assert task["priority"] == "high"
    assert get_stats(db_path) == {
        "total": 1,
        "completed": 0,
        "pending": 1,
    }


def test_create_task_with_done_status(db_path):
    task_id = create_task("Completed task", db_path=db_path, done=1)

    assert get_task(task_id, db_path)["done"] == 1


def test_invalid_priority_is_rejected(db_path):
    with pytest.raises(ValueError):
        create_task("Task", priority="urgent", db_path=db_path)


def test_filter_done_tasks(db_path):
    pending_id = create_task("Pending", priority="normal", db_path=db_path)
    completed_id = create_task("Done", priority="low", db_path=db_path)
    update_task(completed_id, done=1, db_path=db_path)

    assert [task["id"] for task in get_tasks_by_done(False, db_path)] == [pending_id]
    assert [task["id"] for task in get_tasks_by_done(True, db_path)] == [completed_id]


def test_create_and_list_task(db_path):
    task_id = create_task("Test task", "Opis", db_path=db_path)
    tasks = get_all_tasks(db_path)

    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == "Test task"
    assert tasks[0]["description"] == "Opis"
    assert tasks[0]["done"] == 0


def test_get_task_returns_task_by_id(db_path):
    task_id = create_task("Do pobrania", "Szczegóły zadania", db_path=db_path)

    task = get_task(task_id, db_path)

    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Do pobrania"
    assert task["description"] == "Szczegóły zadania"
    assert task["done"] == 0


def test_update_task_changes_selected_fields(db_path):
    task_id = create_task("Stary tytuł", "Stary opis", db_path=db_path)

    updated = update_task(
        task_id,
        title="Nowy tytuł",
        description="Nowy opis",
        done=1,
        db_path=db_path,
    )

    assert updated is True
    task = get_task(task_id, db_path)
    assert task["title"] == "Nowy tytuł"
    assert task["description"] == "Nowy opis"
    assert task["done"] == 1


def test_delete_task(db_path):
    task_id = create_task("Do usunięcia", "Opis", db_path=db_path)

    deleted = delete_task(task_id, db_path)

    assert deleted is True
    assert get_task(task_id, db_path) is None
    assert not any(task["id"] == task_id for task in get_all_tasks(db_path))


def test_task_field_length_limits(db_path):
    title = "A" * 200
    description = "B" * 300
    task_id = create_task(title, description, db_path=db_path)

    task = get_task(task_id, db_path)
    assert task["title"] == title
    assert task["description"] == description

    with pytest.raises(ValueError, match="200 characters"):
        create_task("A" * 201, db_path=db_path)
    with pytest.raises(ValueError, match="300 characters"):
        create_task("Valid", "B" * 301, db_path=db_path)

    with pytest.raises(ValueError, match="200 characters"):
        update_task(task_id, title="A" * 201, db_path=db_path)
    with pytest.raises(ValueError, match="300 characters"):
        update_task(task_id, description="B" * 301, db_path=db_path)
