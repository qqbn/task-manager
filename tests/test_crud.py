from app.crud import create_task, get_all_tasks, delete_task
from app.database import init_db

def test_create_and_list_task():
    init_db()
    task_id = create_task("Test task", "Opis")
    tasks = get_all_tasks()
    assert any(task["id"] == task_id for task in tasks)

def test_delete_task():
    init_db()
    task_id = create_task("Do usunięcia", "Opis")
    delete_task(task_id)
    tasks = get_all_tasks()
    assert not any(task["id"] == task_id for task in tasks)