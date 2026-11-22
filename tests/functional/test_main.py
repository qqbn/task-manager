from app.functional.crud import get_all_tasks


def test_menu_reports_invalid_ids_missing_tasks_and_empty_list(
    tmp_path, monkeypatch, caplog
):
    monkeypatch.chdir(tmp_path)
    answers = iter(["2", "3", "bad", "3", "404", "4", "bad", "4", "404", "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.main import main

    caplog.set_level("INFO", logger="app.main")
    main()

    assert "No tasks found." in caplog.text
    assert caplog.text.count("ID must be a number.") == 2
    assert caplog.text.count("Task not found.") == 2
    assert "Task deleted." not in caplog.text
    assert "Task updated." not in caplog.text


def test_menu_rejects_empty_title_and_retries_invalid_done(
    tmp_path, monkeypatch, caplog
):
    monkeypatch.chdir(tmp_path)
    answers = iter(
        [
            "1",
            "   ",
            "1",
            "Task",
            "",
            "1",
            "normal",
            "4",
            "1",
            "",
            "",
            "bad",
            "1",
            "",
            "7",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.main import main

    caplog.set_level("INFO", logger="app.main")
    main()

    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task"
    assert tasks[0]["done"] == 1
    assert "Task title cannot be empty." in caplog.text
    assert "Enter 0 or 1." in caplog.text


def test_menu_adds_completed_task(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    answers = iter(["1", "Completed task", "", "1", "normal", "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.main import main

    main()

    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Completed task"
    assert tasks[0]["done"] == 1


def test_menu_rejects_overlong_fields(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    answers = iter(["1", "A" * 201, "7"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    from app.main import main

    caplog.set_level("INFO", logger="app.main")
    main()

    assert get_all_tasks() == []
    assert "Task title cannot be longer than 200 characters" in caplog.text
