"""Base repositories module"""

from abc import ABC
from abc import abstractmethod
from typing import Any

from models.task_mdl import Task


class BaseTasksRepository(ABC):
    """Task opertations repository"""

    @abstractmethod
    def get_tasks(self):
        """Get all tasks"""
        raise NotImplementedError()

    @abstractmethod
    def update_task_description(self, task: Task):
        """Update a task description"""
        raise NotImplementedError()

    @abstractmethod
    def add_task(self, task: Task):
        """Add a new task"""
        raise NotImplementedError()

    @abstractmethod
    def delete_task(self, task_id: Any):
        """Delete a task"""
        raise NotImplementedError()

    @abstractmethod
    def mark_task_as_completed(self, task_id: Any):
        """Mark a task as completed"""
        raise NotImplementedError()

    @abstractmethod
    def get_completed_tasks(self):
        """Get all completed tasks"""
        raise NotImplementedError()

    @abstractmethod
    def get_not_completed_tasks(self):
        """Get all not completed tasks"""
        raise NotImplementedError()
