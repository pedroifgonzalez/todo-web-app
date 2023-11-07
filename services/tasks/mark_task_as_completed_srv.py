"""Task completion service"""
from typing import Any

from fastapi_injector import Injected
from repositories.tasks_repo import BaseTasksRepository


class MarkTaskAsCompletedService:
    """Service for mark a task as completed"""

    def __init__(self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository)) -> None:
        self.task_repository = task_repository

    def execute(self, task_id: Any):
        """Service execution operations"""
        return self.task_repository.mark_task_as_completed(task_id=task_id)
