import pytest
from models.task_mdl import Task
from orm.mappings import SQLAlchemyORM
from repositories.tasks_repo import SQLAlchemyTaskRepository
from schema.task_sch import SQLAlchemyTask
from services.tasks.add_task_srv import AddTaskService
from services.tasks.delete_task_srv import DeleteTaskService
from services.tasks.get_completed_tasks_srv import GetCompletedTasksService
from services.tasks.get_not_completed_tasks_srv import GetNotCompletedTasksService
from services.tasks.get_tasks_srv import GetTasksService
from services.tasks.mark_task_as_completed_srv import MarkTaskAsCompletedService
from services.tasks.mark_task_as_not_completed_srv import MarkTaskAsNotCompletedService
from services.tasks.update_task_description_srv import UpdateTaskDescriptionService


@pytest.fixture(autouse=True, name='repository')
def task_repository(test_db_session):
    """Task repository fixture"""
    return SQLAlchemyTaskRepository(session=test_db_session)


@pytest.fixture(name='orm')
def orm_implementation():
    """ORM fixture"""
    return SQLAlchemyORM()


def test_add_task_service(test_db_session, repository, orm):
    """Assert AddTaskService behaviour"""
    # arrange
    add_task_service = AddTaskService(task_repository=repository, orm=orm)
    test_task = Task(description='This is a test task')

    # act
    add_task_service.execute(task=test_task)

    # assert
    row_task = test_db_session.query(SQLAlchemyTask).all()[0]
    assert row_task
    assert row_task.description == 'This is a test task'


def test_get_tasks_service(test_db_session, repository, orm):
    """Assert GetTasksService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is a test task no 1'))
    test_db_session.add(SQLAlchemyTask(description='This is a test task no 2'))
    test_db_session.commit()

    # act
    get_tasks_service = GetTasksService(task_repository=repository, orm=orm)
    tasks_rows = get_tasks_service.execute()

    # assert
    assert len(tasks_rows) == 2


def test_update_task_description_service(test_db_session, repository, orm):
    """Assert UpdateTaskDescriptionService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is a test task no 3', id=1, completed=True))
    test_db_session.commit()

    # act
    update_task_description_service = UpdateTaskDescriptionService(task_repository=repository, orm=orm)
    update_task_description_service.execute(task=Task(id=1, description='This is another test task 5'))
    # assert

    task_row = test_db_session.query(SQLAlchemyTask).all()[0]
    assert task_row.description == 'This is another test task 5'


def test_get_completed_tasks_service(test_db_session, repository, orm):
    """Assert GetCompletedTasksService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is another test task 7', id=1, completed=True))
    test_db_session.add(SQLAlchemyTask(description='This is a test task no 9', id=2, completed=False))
    test_db_session.commit()

    # act
    get_completed_tasks_service = GetCompletedTasksService(task_repository=repository, orm=orm)
    tasks_rows = get_completed_tasks_service.execute()

    # assert
    assert len(tasks_rows) == 1
    assert tasks_rows[0].description == 'This is another test task 7'
    assert tasks_rows[0].completed
    assert tasks_rows[0].id == 1


def test_get_no_completed_tasks(test_db_session, repository, orm):
    """Assert GetNotCompletedTasksService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is another test task 8', id=1, completed=True))
    test_db_session.add(SQLAlchemyTask(description='This is another test task no 3', id=2, completed=False))
    test_db_session.commit()

    # act
    get_not_completed_tasks_service = GetNotCompletedTasksService(task_repository=repository, orm=orm)
    tasks_rows = get_not_completed_tasks_service.execute()

    # assert
    assert len(tasks_rows) == 1
    assert tasks_rows[0].description == 'This is another test task no 3'
    assert not tasks_rows[0].completed
    assert tasks_rows[0].id == 2


def test_delete_task_service(test_db_session, repository):
    """Assert DeleteTaskService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is another test task 9', id=1, completed=True))
    test_db_session.add(SQLAlchemyTask(description='This is another test task no 10', id=2, completed=False))
    test_db_session.commit()

    # act
    delete_task_service = DeleteTaskService(task_repository=repository)
    delete_task_service.execute(task_id=1)

    # assert
    tasks_rows = test_db_session.query(SQLAlchemyTask).all()
    assert len(tasks_rows) == 1
    assert tasks_rows[0].description == 'This is another test task no 10'
    assert not tasks_rows[0].completed
    assert tasks_rows[0].id == 2
    assert tasks_rows[0].completed is False


def test_mark_task_as_completed_service(test_db_session, repository):
    """Assert MarkTaskAsCompletedService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is another test task 11', id=1, completed=True))
    test_db_session.add(SQLAlchemyTask(description='This is another test task no 12', id=2, completed=False))
    test_db_session.commit()

    # act
    mark_task_as_completed_service = MarkTaskAsCompletedService(task_repository=repository)
    mark_task_as_completed_service.execute(task_id=2)

    # assert
    tasks_rows = test_db_session.query(SQLAlchemyTask).filter_by(completed=True).all()
    assert len(tasks_rows) == 2


def test_mark_task_as_not_completed_service(test_db_session, repository):
    """Assert MarkTaskAsNotCompletedService behaviour"""
    # arrange
    test_db_session.add(SQLAlchemyTask(description='This is another test task 11', id=1, completed=True))
    test_db_session.add(SQLAlchemyTask(description='This is another test task no 12', id=2, completed=True))
    test_db_session.commit()

    # act
    mark_task_as_not_completed_service = MarkTaskAsNotCompletedService(task_repository=repository)
    mark_task_as_not_completed_service.execute(task_id=2)

    # assert
    tasks_rows = test_db_session.query(SQLAlchemyTask).filter_by(completed=True).all()
    assert len(tasks_rows) == 1
