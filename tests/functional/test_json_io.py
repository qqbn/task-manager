import pytest

from app.functional import json_io
from app.functional.json_io import (
    ask_done,
    delete_task,
    get_all_tasks,
    get_task,
    save_all_tasks,
    update_task,
)


@pytest.fixture(autouse=True)
def isolated_tasks_file(tmp_path, monkeypatch):
    # json_io reads "tasks.json" from the current directory, so the tests
    # run in a temporary directory and never touch the real file.
    monkeypatch.chdir(tmp_path)


def test_save_and_list_tasks():
    save_all_tasks([{"id": 1, "title": "Test task", "description": "Opis", "done": 0}])

    tasks = get_all_tasks()

    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "Test task"
    assert tasks[0]["description"] == "Opis"
    assert tasks[0]["done"] == 0


def test_get_task_returns_task_by_id():
    save_all_tasks([
        {"id": 1, "title": "Pierwszy", "description": "Opis 1", "done": 0},
        {"id": 2, "title": "Do pobrania", "description": "Szczegóły zadania", "done": 1},
    ])

    task = get_task(2)

    assert task is not None
    assert task["id"] == 2
    assert task["title"] == "Do pobrania"
    assert task["description"] == "Szczegóły zadania"
    assert task["done"] == 1


def test_get_task_returns_none_for_missing_id():
    save_all_tasks([{"id": 1, "title": "Zadanie", "description": None, "done": 0}])

    assert get_task(999) is None


def test_update_task_changes_selected_fields():
    save_all_tasks([{"id": 1, "title": "Stary tytuł", "description": "Stary opis", "done": 0}])

    updated = update_task(1, title="Nowy tytuł", description="Nowy opis", done=1)

    assert updated is True
    task = get_task(1)
    assert task["title"] == "Nowy tytuł"
    assert task["description"] == "Nowy opis"
    assert task["done"] == 1


def test_update_task_keeps_old_values_when_empty():
    save_all_tasks([{"id": 1, "title": "Tytuł", "description": "Opis", "done": 1}])

    update_task(1, title="", description="", done=None)

    task = get_task(1)
    assert task["title"] == "Tytuł"
    assert task["description"] == "Opis"
    assert task["done"] == 1


def test_update_task_can_set_done_back_to_zero():
    save_all_tasks([{"id": 1, "title": "Zadanie", "description": None, "done": 1}])

    update_task(1, done=0)

    assert get_task(1)["done"] == 0


def test_update_task_returns_false_for_missing_id():
    save_all_tasks([{"id": 1, "title": "Zadanie", "description": None, "done": 0}])

    assert update_task(999, title="Nowy") is False
    assert get_task(1)["title"] == "Zadanie"


def test_delete_task():
    save_all_tasks([
        {"id": 1, "title": "Zostaje", "description": None, "done": 0},
        {"id": 2, "title": "Do usunięcia", "description": "Opis", "done": 0},
    ])

    deleted = delete_task(2)

    assert deleted is True
    assert get_task(2) is None
    assert not any(task["id"] == 2 for task in get_all_tasks())
    assert get_task(1) is not None


def test_delete_task_returns_false_for_missing_id():
    save_all_tasks([{"id": 1, "title": "Zadanie", "description": None, "done": 0}])

    assert delete_task(999) is False
    assert len(get_all_tasks()) == 1


def test_ask_done_returns_int_and_default(monkeypatch):
    answers = iter(["1", "0", ""])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert ask_done("Done: ", default=None) == 1
    assert ask_done("Done: ", default=None) == 0
    assert ask_done("Done: ", default=None) is None


def test_ask_done_repeats_until_valid(monkeypatch):
    answers = iter(["2", "abc", "1"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert ask_done("Done: ", default=None) == 1


def test_menu_add_task_with_done(monkeypatch):
    save_all_tasks([{"id": 1, "title": "Istniejące", "description": None, "done": 0}])
    answers = iter(["1", "Nowy", "Opis", "1", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    json_io.main()

    task = get_task(2)
    assert task == {"id": 2, "title": "Nowy", "description": "Opis", "done": 1}


def test_menu_add_task_does_not_duplicate_id_after_delete(monkeypatch):
    save_all_tasks([
        {"id": 1, "title": "Pierwszy", "description": None, "done": 0},
        {"id": 3, "title": "Trzeci", "description": None, "done": 0},
    ])
    answers = iter(["1", "Nowy", "", "", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    json_io.main()

    assert [task["id"] for task in get_all_tasks()] == [1, 3, 4]


def test_menu_update_task(monkeypatch):
    save_all_tasks([{"id": 1, "title": "Stary", "description": "Opis", "done": 0}])
    answers = iter(["4", "1", "Nowy", "", "1", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    json_io.main()

    task = get_task(1)
    assert task["title"] == "Nowy"
    assert task["description"] == "Opis"
    assert task["done"] == 1


def test_menu_update_missing_task_prints_message(monkeypatch, capsys):
    save_all_tasks([{"id": 1, "title": "Zadanie", "description": None, "done": 0}])
    answers = iter(["4", "999", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    json_io.main()

    assert "Task not found." in capsys.readouterr().out
