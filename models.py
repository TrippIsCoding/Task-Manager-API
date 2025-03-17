from .database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

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
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str