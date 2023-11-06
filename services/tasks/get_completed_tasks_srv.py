from fastapi_injector import Injected
from orm.mappings import ORMBase
from repositories.tasks_repo import BaseTasksRepository


class GetCompletedTasksService:
    """Get completed tasks service"""

    def __init__(
        self, task_repository: BaseTasksRepository = Injected(BaseTasksRepository), orm: ORMBase = Injected(ORMBase)
    ) -> None:
        self.task_repository = task_repository
        self.orm = orm

    def execute(self):
        """Service execution operations"""
        schema_tasks = self.task_repository.get_completed_tasks()
        tasks = [self.orm.to_task_model(schema_task=schema_task) for schema_task in schema_tasks]
        return tasks
