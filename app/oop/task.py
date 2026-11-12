from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """A task represented as a Python object."""

    title: str
    description: Optional[str] = None
    done: bool = False
    id: Optional[int] = None
