"""Code related to a Task model properties and definition"""

from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    """A user task representing class"""

    id: Optional[int] = None
    description: str
    completed: bool = False
