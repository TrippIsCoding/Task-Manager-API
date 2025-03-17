import jwt
from typing import Annotated
from sqlalchemy.orm import Session
from .models import Task, TaskModel, TokenResponse, User
from datetime import timedelta, timezone, datetime
from .config import SECRET_KEY, ALGORITHM
from .database import get_db, Base, engine
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    return User(username=payload['sub'])

@app.post('/token', response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != 'testuser' or form_data.password != 'testpassword':
        raise HTTPException(status_code=400, detail='Invalid credentials')
    
    access_token = create_access_token({'sub': form_data.username})
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/tasks')
def list_all_tasks(order: str = 'asc', db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if order.lower() == 'asc':
        tasks = db.query(TaskModel).order_by(TaskModel.priority.asc()).all()
    else:
        tasks = db.query(TaskModel).order_by(TaskModel.priority.desc()).all()

    if not tasks:
        raise HTTPException(status_code=404, detail='No tasks found')
    
    return {'tasks': tasks}

@app.get('/tasks/{id}')
def show_specific_task(id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task": task}

@app.post('/create/tasks')
def create_task(task: Task, db: Session = Depends(get_db)):
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        deadline=task.deadline,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return {"message": "Task created successfully", "task_id": db_task.id}

@app.put('/tasks/{id}')
def update_task(id: int, task: Task, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.priority = task.priority
    db_task.deadline = task.deadline

    db.commit()
    db.refresh(db_task)

    return {'message': 'Task updated successfully'}

@app.delete('/tasks/{id}')
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not db_task:
        raise HTTPException(status_code=404, datail='Task not found')

    db.delete(db_task)
    db.commit()

    return {'message': 'Task deleted successfully'}