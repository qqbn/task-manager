from typing import Optional

MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 300


def validate_title(title: str) -> str:
    if not title.strip():
        raise ValueError("Task title cannot be empty.")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError("Task title cannot be longer than 200 characters.")
    return title


def validate_description(description: Optional[str]) -> Optional[str]:
    if description is not None and len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError("Task description cannot be longer than 300 characters.")
    return description
