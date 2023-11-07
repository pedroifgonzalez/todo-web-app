"""Task description update service"""
from fastapi_injector import Injected
from models.task_mdl import Task
from orm.mappings import ORMBase
from repositories.tasks_repo import BaseTasksRepository


class UpdateTaskDescriptionService:
    """Service for updating a task description"""

    def __init__(
        self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository), orm: ORMBase = Injected(ORMBase)
    ) -> None:
        self.task_repository = task_repository
        self.orm = orm

    def execute(self, task: Task):
        """Service execution operations"""
        schema_task = self.orm.to_schema_db_task(task=task)
        return self.task_repository.update_task_description(task=schema_task)
