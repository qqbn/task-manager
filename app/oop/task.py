from dataclasses import dataclass
from typing import Optional


# Reminder: @dataclass generates __init__, __repr__ and __eq__ for us.
# Without it, the same class would look like this:
#
#   class Task:
#       def __init__(self, title, description=None, done=False, id=None):
#           self.title = title              # `self` = the object being created
#           self.description = description  # `self.x = ...` makes an attribute
#           self.done = done
#           self.id = id
#
#       def __repr__(self):                 # how the object looks in print()
#           return (f"Task(id={self.id!r}, title={self.title!r}, "
#                   f"description={self.description!r}, done={self.done!r})")
#
#       def __eq__(self, other):            # compare by content, not address
#           if not isinstance(other, Task):
#               return NotImplemented
#           return (self.id == other.id and self.title == other.title
#                   and self.description == other.description
#                   and self.done == other.done)
@dataclass
class Task:
    """A task represented as a Python object."""

    title: str
    description: Optional[str] = None
    done: bool = False
    id: Optional[int] = None
