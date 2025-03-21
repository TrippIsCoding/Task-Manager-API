from fastapi import FastAPI
from auth import auth_router
from database import Base, engine
from task_crud import task_router

app = FastAPI()
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(task_router, prefix='/task', tags=['task'])

Base.metadata.create_all(bind=engine)
