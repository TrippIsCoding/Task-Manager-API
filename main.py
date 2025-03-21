from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from auth import auth_router, oauth2_scheme
from models import Task, TaskModel
from database import get_db, Base, engine
from task_crud import task_router

app = FastAPI()
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(task_router, prefix='/task', tags=['task'])

Base.metadata.create_all(bind=engine)
