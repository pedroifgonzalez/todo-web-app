"""Task repositories implementations"""
from typing import Any

from schema.task_sch import SQLAlchemyTask
from sqlalchemy import not_

from . import BaseTasksRepository


class SQLAlchemyTaskRepository(BaseTasksRepository):
    """SQLAlchemy task repository implementation"""

    def __init__(self, session) -> None:
        self.session = session

    def get_tasks(self):
        """Get all tasks"""
        return self.session.query(SQLAlchemyTask).all()

    def add_task(self, task: SQLAlchemyTask):
        """Add a new task"""
        self.session.add(task)
        self.session.commit()
        return task

    def update_task_description(self, task: SQLAlchemyTask):
        """Update a task description"""
        self.session.query(SQLAlchemyTask).filter(SQLAlchemyTask.id == task.id).update(
            {SQLAlchemyTask.description: task.description}
        )
        self.session.commit()
        return True

    def mark_task_as_completed(self, task_id: Any):
        """Mark a task as completed"""
        self.session.query(SQLAlchemyTask).filter(SQLAlchemyTask.id == task_id).update({SQLAlchemyTask.completed: True})
        self.session.commit()
        return True

    def mark_task_as_not_completed(self, task_id: Any):
        """Mark a task as not completed"""
        self.session.query(SQLAlchemyTask).filter(SQLAlchemyTask.id == task_id).update(
            {SQLAlchemyTask.completed: False}
        )
        self.session.commit()
        return True

    def get_completed_tasks(self):
        """Get all completed tasks"""
        return self.session.query(SQLAlchemyTask).filter(SQLAlchemyTask.completed).all()

    def get_not_completed_tasks(self):
        """Get all not completed tasks"""
        return self.session.query(SQLAlchemyTask).filter(not_(SQLAlchemyTask.completed)).all()

    def delete_task(self, task_id: Any):
        """Delete a task"""
        self.session.query(SQLAlchemyTask).filter(SQLAlchemyTask.id == task_id).delete()
        self.session.commit()
        return True
