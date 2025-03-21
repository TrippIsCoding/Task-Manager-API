from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Task, TaskModel, UserModel
from database import get_db
from auth import verify_token, oauth2_scheme

task_router = APIRouter()

@task_router.get('')
def list_all_tasks(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_info = verify_token(token)

    user = db.query(UserModel).filter_by(username=user_info['sub']).first()

    if not user:
        raise HTTPException(status_code=404, detail='Could not find user')
    if not user.task:
        raise HTTPException(status_code=404, detail='User has no tasks')

    return [{'Owner': user_info['sub'], 'task': task} for task in user.task]

@task_router.post('/create')
def create_task(task: Task, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_info = verify_token(token)

    new_task = TaskModel(
        user_id=user_info['user_id'],
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        deadline=task.deadline,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": f"Task created successfully for {user_info['sub']}", "task_id": new_task.task_id}

@task_router.put('/update/{id}')
def update_task(id: int, new_task: Task, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_info = verify_token(token)
    task = db.query(TaskModel).filter(TaskModel.task_id==id).first()

    if not task:
        raise HTTPException(status_code=404, detail='Task not found in database')
    if user_info['user_id'] != task.user_id:
        raise HTTPException(status_code=401, detail='User does not own task')

    task.title = new_task.title
    task.description = new_task.description
    task.status = new_task.status
    task.priority = new_task.priority
    task.deadline = new_task.deadline

    db.commit()
    db.refresh(task)

    return {'message': 'Task updated successfully', 'Task_id': task.task_id}

@task_router.delete('/delete/{id}')
def delete_task(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_info = verify_token(token)
    task = db.query(TaskModel).filter(TaskModel.task_id == id).first()

    if not task:
        raise HTTPException(status_code=404, datail='Task not found')
    if user_info['user_id'] != task.user_id:
        raise HTTPException(status_code=401, detail='User does not own this task')
    
    db.delete(task)
    db.commit()

    return {'message': 'Task deleted successfully'}