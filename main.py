import json
from typing import Annotated
from typing import Any

import sqlalchemy
from db.sqlalchemy_database import Base
from db.sqlalchemy_database import engine
from db.sqlalchemy_database import SessionLocal
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Form
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_injector import attach_injector
from injector import Injector
from injector import singleton
from models.task_mdl import Task
from orm import mappings
from repositories import tasks_repo
from schema.task_sch import SQLAlchemyTask
from services.tasks.add_task_srv import AddTaskService
from services.tasks.delete_completed_tasks_srv import DeleteCompletedTasksService
from services.tasks.delete_task_srv import DeleteTaskService
from services.tasks.get_completed_tasks_srv import GetCompletedTasksService
from services.tasks.get_not_completed_tasks_srv import GetNotCompletedTasksService
from services.tasks.get_tasks_srv import GetTasksService
from services.tasks.mark_task_as_completed_srv import MarkTaskAsCompletedService
from services.tasks.mark_task_as_not_completed_srv import MarkTaskAsNotCompletedService
from services.tasks.mark_tasks_as_completed_srv import MarkTasksAsCompletedService
from services.tasks.mark_tasks_as_not_completed_srv import MarkTasksAsNotCompletedService


templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def load_initial_data():
    """Load sample data"""
    session = SessionLocal()
    with open('data/tasks.json', encoding='utf8') as f:
        json_data = json.load(f)
        try:
            for data in json_data:
                session.add(SQLAlchemyTask(**data))
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass


def setup_app():
    """Set initial settings for running the app"""
    Base.metadata.create_all(bind=engine)
    injector = Injector()
    injector.binder.bind(
        tasks_repo.BaseTasksRepository, tasks_repo.SQLAlchemyTaskRepository(session=SessionLocal()), scope=singleton
    )
    injector.binder.bind(mappings.ORMBase, mappings.SQLAlchemyORM, scope=singleton)
    attach_injector(app, injector)


setup_app()
load_initial_data()


@app.get("/")
def home_page(request: Request, get_tasks_service: GetTasksService = Depends()):
    """Home page route"""
    tasks = get_tasks_service.execute()
    items_left = len([task for task in tasks if task.completed is not True])
    completed_tasks = [task for task in tasks if task.completed is True]

    return templates.TemplateResponse(
        'index.html',
        {
            "request": request,
            "tasks": tasks,
            "items_left": items_left,
            "start": True,
            "completed": None,
            "completed_tasks": True if completed_tasks else False,
        },
    )


@app.get('/tasks')
def get_tasks(
    request: Request,
    completed: bool = None,
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    get_tasks_service: GetTasksService = Depends(),
):
    """Get all tasks"""
    if completed:
        tasks = get_completed_tasks_service.execute()
    elif completed is False:
        tasks = get_not_completed_tasks_service.execute()
    else:
        tasks = get_tasks_service.execute()

    items_left = len([task for task in tasks if task.completed is not True])

    return templates.TemplateResponse(
        '/tasks.html',
        {
            "request": request,
            "tasks": tasks,
            "items_left": items_left,
            "completed": completed,
        },
    )


@app.post('/tasks')
def add_task(
    request: Request,
    description: Annotated[str, Form()],
    completed: bool = None,
    get_tasks_service: GetTasksService = Depends(),
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    add_task_service: AddTaskService = Depends(),
):
    """Add a task"""
    task = Task(description=description)
    add_task_service.execute(task=task)
    return get_tasks(
        request=request,
        completed=completed,
        get_tasks_service=get_tasks_service,
        get_completed_tasks_service=get_completed_tasks_service,
        get_not_completed_tasks_service=get_not_completed_tasks_service,
    )


@app.delete('/task/{task_id}')
def delete_task(
    request: Request,
    task_id: Any,
    completed: bool = None,
    get_tasks_service: GetTasksService = Depends(),
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    delete_task_service: DeleteTaskService = Depends(),
):
    """Delete a task"""
    delete_task_service.execute(task_id=task_id)
    return get_tasks(
        request=request,
        completed=completed,
        get_tasks_service=get_tasks_service,
        get_completed_tasks_service=get_completed_tasks_service,
        get_not_completed_tasks_service=get_not_completed_tasks_service,
    )


@app.post('/tasks/clear')
def clear_completed(
    request: Request,
    completed: bool = None,
    get_tasks_service: GetTasksService = Depends(),
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    delete_completed_tasks_service: DeleteCompletedTasksService = Depends(),
):
    """Delete completed tasks"""
    delete_completed_tasks_service.execute()
    return get_tasks(
        request=request,
        completed=completed,
        get_tasks_service=get_tasks_service,
        get_completed_tasks_service=get_completed_tasks_service,
        get_not_completed_tasks_service=get_not_completed_tasks_service,
    )


@app.put('/tasks/{task_id}/complete')
def mark_task_as_completed(
    request: Request,
    task_id: Any,
    completed: bool = None,
    get_tasks_service: GetTasksService = Depends(),
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    mark_task_as_completed_service: MarkTaskAsCompletedService = Depends(),
):
    """Mark a task as completed"""
    mark_task_as_completed_service.execute(task_id=task_id)
    return get_tasks(
        request=request,
        completed=completed,
        get_tasks_service=get_tasks_service,
        get_completed_tasks_service=get_completed_tasks_service,
        get_not_completed_tasks_service=get_not_completed_tasks_service,
    )


@app.put('/tasks/{task_id}/uncomplete')
def mark_task_as_not_completed(
    request: Request,
    task_id: Any,
    completed: bool = None,
    get_tasks_service: GetTasksService = Depends(),
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    mark_task_as_not_completed_service: MarkTaskAsNotCompletedService = Depends(),
):
    """Mark a task as completed"""
    mark_task_as_not_completed_service.execute(task_id=task_id)
    return get_tasks(
        request=request,
        completed=completed,
        get_tasks_service=get_tasks_service,
        get_completed_tasks_service=get_completed_tasks_service,
        get_not_completed_tasks_service=get_not_completed_tasks_service,
    )


@app.get('/status')
def get_status(request: Request, completed: bool = None, get_tasks_service: GetTasksService = Depends()):
    """Get tasks status information"""
    all_selected = False
    active_selected = False
    completed_selected = False
    match completed:
        case True:
            completed_selected = True
        case False:
            active_selected = True
        case _:
            all_selected = True

    tasks = get_tasks_service.execute()
    items_left = len([task for task in tasks if task.completed is not True])
    completed_tasks = [task for task in tasks if task.completed is True]

    return templates.TemplateResponse(
        '/footer.html',
        {
            "request": request,
            'all_selected': all_selected,
            'active_selected': active_selected,
            'completed_selected': completed_selected,
            "items_left": items_left,
            "completed_tasks": True if completed_tasks else False,
        },
    )


@app.get('/header')
def get_header(request: Request, completed: bool = None):
    """Get header"""
    return templates.TemplateResponse(
        '/header.html',
        {
            "request": request,
            "completed": completed,
        },
    )


@app.post('/tasks/toggle')
def toggle_all_tasks(
    request: Request,
    completed: bool = None,
    get_tasks_service: GetTasksService = Depends(),
    get_completed_tasks_service: GetCompletedTasksService = Depends(),
    get_not_completed_tasks_service: GetNotCompletedTasksService = Depends(),
    mark_tasks_as_not_completed_service: MarkTasksAsNotCompletedService = Depends(),
    mark_tasks_as_completed_service: MarkTasksAsCompletedService = Depends(),
):
    """Toggle all tasks' statuses"""
    tasks = get_tasks_service.execute()
    completed_tasks = [task for task in tasks if task.completed is True]
    if len(completed_tasks) == len(tasks):
        mark_tasks_as_not_completed_service.execute()
    else:
        mark_tasks_as_completed_service.execute()

    return get_tasks(
        request=request,
        completed=completed,
        get_tasks_service=get_tasks_service,
        get_completed_tasks_service=get_completed_tasks_service,
        get_not_completed_tasks_service=get_not_completed_tasks_service,
    )
