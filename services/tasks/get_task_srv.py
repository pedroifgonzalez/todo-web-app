"""Obtention of a task service"""
from typing import Any

from fastapi_injector import Injected
from orm.mappings import ORMBase
from repositories.tasks_repo import BaseTasksRepository


class GetTaskService:
    """Service for getting a task"""

    def __init__(
        self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository), orm: ORMBase = Injected(ORMBase)
    ) -> None:
        self.task_repository = task_repository
        self.orm = orm

    def execute(self, task_id: Any):
        """Service execution operations"""
        schema_task = self.task_repository.get_task(task_id=task_id)
        task = self.orm.to_task_model(schema_task=schema_task)
        return task
