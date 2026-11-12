from app.functional.crud import create_task, delete_task, get_all_tasks, get_task, update_task
from app.database import get_connection, init_db


def setup_function():
    init_db()
    conn = get_connection()
    conn.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()


def test_create_and_list_task():
    task_id = create_task("Test task", "Opis")
    tasks = get_all_tasks()

    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == "Test task"
    assert tasks[0]["description"] == "Opis"
    assert tasks[0]["done"] == 0


def test_get_task_returns_task_by_id():
    task_id = create_task("Do pobrania", "Szczegóły zadania")

    task = get_task(task_id)

    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Do pobrania"
    assert task["description"] == "Szczegóły zadania"
    assert task["done"] == 0


def test_update_task_changes_selected_fields():
    task_id = create_task("Stary tytuł", "Stary opis")

    updated = update_task(task_id, title="Nowy tytuł", description="Nowy opis", done=1)

    assert updated is True
    task = get_task(task_id)
    assert task["title"] == "Nowy tytuł"
    assert task["description"] == "Nowy opis"
    assert task["done"] == 1


def test_delete_task():
    task_id = create_task("Do usunięcia", "Opis")

    deleted = delete_task(task_id)

    assert deleted is True
    assert get_task(task_id) is None
    assert not any(task["id"] == task_id for task in get_all_tasks())