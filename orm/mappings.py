from abc import ABC
from abc import abstractmethod
from typing import Any

from models.task_mdl import Task
from schema.task_sch import SQLAlchemyTask


def map_task_model_to_sqlalchemy_task(task: Task) -> SQLAlchemyTask:
    """Map from a task model to a SQLAlchemy row object"""
    return SQLAlchemyTask(description=task.description, completed=task.completed, id=task.id)


def map_sqlalchemy_task_to_task_model(task: SQLAlchemyTask) -> Task:
    """Map from a SQLAlchemy row object to a task model"""
    return Task(description=task.description, completed=task.completed, id=task.id)


class ORMBase(ABC):
    """ORM Base class"""

    @abstractmethod
    def to_task_model(self, schema_task: Any):
        """Convert to a Task model object"""
        raise NotImplementedError()

    @abstractmethod
    def to_schema_db_task(self, task: Task) -> Any:
        """Convert to a schema database equivalent object"""
        raise NotImplementedError()


class SQLAlchemyORM(ORMBase):
    """SQLAlchemy ORM class"""

    def to_task_model(self, schema_task: SQLAlchemyTask) -> Task:
        """Convert SQLAlchemyTask to Task"""
        return map_sqlalchemy_task_to_task_model(schema_task)

    def to_schema_db_task(self, task: Task) -> SQLAlchemyTask:
        """Convert Task to SQLAlchemyTask"""
        return map_task_model_to_sqlalchemy_task(task)
