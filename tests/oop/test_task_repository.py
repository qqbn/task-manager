import pytest

from app import database
from app.oop.task import Task
from app.oop.task_repository import TaskRepository


@pytest.fixture
def repository(tmp_path):
    # No monkeypatch needed: the repository gets a temporary file directly
    # through its constructor. The real tasks.db is never touched here.
    db_path = str(tmp_path / "tasks.db")
    database.init_db(db_path)
    return TaskRepository(db_path)


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

    main(repository)  # pass the test repository instead of the default one

    assert repository.get_all_tasks() == [Task("CLI task", "Opis", id=1)]

def test_get_all_tasks_returns_empty_list_for_empty_db(repository):
    assert repository.get_all_tasks() == []

def test_get_task_returns_created_task(repository):
    task = repository.create_task(Task("New task", "Desc"))
    task_id = task.id
    selected_task = repository.get_task(task_id)

    assert selected_task == task

def test_get_all_tasks_returns_tasks_ordered_by_id(repository):
    t1 = repository.create_task(Task("New task 1", "Desc 1"))
    t2 = repository.create_task(Task("New task 2", "Desc 2"))
    t3 = repository.create_task(Task("New task 3", "Desc 3"))
    tasks = repository.get_all_tasks()

    assert tasks == [t1, t2, t3]


def test_update_task_can_set_done_back_to_false(repository):
    task = repository.create_task(Task("Test task", "Test description", done=True))
    repository.update_task(task.id, done=False)
    updated = repository.get_task(task.id)

    assert repository.update_task(task.id, done=False) is True
    assert updated.done is False

def test_update_task_returns_false_for_missing_id(repository):
    assert repository.update_task(999, title="Nowy") is False

def test_data_persists_between_repository_instances(repository, tmp_path):
    # Create a task with the first repository instance
    task = repository.create_task(Task("Persistent task", "Persistent description"))
    task_id = task.id

    # Create a new repository instance pointing to the same database file
    new_repository = TaskRepository(str(tmp_path / "tasks.db"))

    # Retrieve the task using the new repository instance
    retrieved_task = new_repository.get_task(task_id)

    assert retrieved_task == task

def test_create_task_with_empty_title_raises(repository):
    with pytest.raises(ValueError):
        repository.create_task(Task("", "Description"))

def test_update_task_with_only_title_keeps_other_fields(repository):
    task = repository.create_task(Task("New task", "Desc", done=True))
    result = repository.update_task(task.id, title="Updated task")
    updated_task = repository.get_task(task.id)

    assert result is True
    assert updated_task.id == task.id
    assert updated_task.title == "Updated task"
    assert updated_task.description == task.description
    assert updated_task.done == task.done