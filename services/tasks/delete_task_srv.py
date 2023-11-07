"""Deletion of a task service"""
from typing import Any

from fastapi_injector import Injected
from repositories.tasks_repo import BaseTasksRepository


class DeleteTaskService:
    """Service for deleting task"""

    def __init__(self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository)) -> None:
        self.task_repository = task_repository

    def execute(self, task_id: Any):
        """Service execution operations"""
        return self.task_repository.delete_task(task_id=task_id)
