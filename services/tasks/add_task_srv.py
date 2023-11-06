from fastapi_injector import Injected
from models.task_mdl import Task
from orm.mappings import ORMBase
from repositories.tasks_repo import BaseTasksRepository


class AddTaskService:
    """Add a task service"""

    def __init__(
        self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository), orm: ORMBase = Injected(ORMBase)
    ) -> None:
        self.task_repository = task_repository
        self.orm = orm

    def execute(self, task: Task):
        """Service execution operations"""
        schema_db_task = self.orm.to_schema_db_task(task=task)
        return self.task_repository.add_task(task=schema_db_task)
