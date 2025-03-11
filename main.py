from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

DATABASE_URL = 'sqlite:///task_manager.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(Integer)
    deadline = Column(String)

class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: int
    deadline: str

    class Config:
        orm_mode = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

@app.get('/tasks')
def list_all_tasks(order: str = 'asc', db: Session = Depends(get_db)):
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

@app.post('/tasks')
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