"""All tasks completion reversal service"""
from fastapi_injector import Injected
from repositories.tasks_repo import BaseTasksRepository


class MarkTasksAsNotCompletedService:
    """Service for mark all tasks as not completed"""

    def __init__(self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository)) -> None:
        self.task_repository = task_repository

    def execute(self):
        """Service execution operations"""
        return self.task_repository.mark_tasks_as_not_completed()
