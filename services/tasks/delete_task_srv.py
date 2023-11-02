from typing import Any

from repositories.tasks_repo import BaseTasksRepository


class DeleteTaskService:
    """Service for deleting task"""

    def __init__(self, task_repository: BaseTasksRepository) -> None:
        self.task_repository = task_repository

    def execute(self, task_id: Any):
        """Service execution operations"""
        return self.task_repository.delete_task(task_id=task_id)
