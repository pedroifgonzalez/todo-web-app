from orm.mappings import ORMBase
from repositories.tasks_repo import BaseTasksRepository


class GetTasksService:
    """Get tasks service"""

    def __init__(self, task_repository: BaseTasksRepository, orm: ORMBase) -> None:
        self.task_repository = task_repository
        self.orm = orm

    def execute(self):
        """Service execution operations"""
        schema_tasks = self.task_repository.get_tasks()
        tasks = [self.orm.to_task_model(schema_task=schema_task) for schema_task in schema_tasks]
        return tasks
