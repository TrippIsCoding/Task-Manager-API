from database import Base
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class UserModel(Base):
    '''
    the UserModel class is inheriting from database.py Base class to create database tables for users
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    email = Column(String, index=True, unique=True)
    full_name = Column(String, nullable=True)

    task = relationship('TaskModel', back_populates='user', cascade='all, delete-orphan')

class User(BaseModel):
    '''
    the User class is inheriting from pydantic BaseModel for validation
    '''
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=8, max_length=72)]
    email: Annotated[str, Field(max_length=100)]
    full_name: Annotated[str, Field(max_length=100)] | None = None

    class Config:
        from_attributes = True


class TaskModel(Base):
    '''
    the TaskModel class is inheriting from database.py Base class to create database tables for tasks
    '''
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(Integer)
    deadline = Column(Date)

    user = relationship('UserModel', back_populates='task')

class Task(BaseModel):
    '''
    the Task class is inheriting from pydantic BaseModel for validation
    '''
    title: Annotated[str, Field(max_length=60)]
    description: Annotated[str, Field(max_length=300)]
    status: Literal['Ongoing', 'Completed']
    priority: Annotated[int, Field(ge=1, le=5)]
    deadline: Annotated[date, Field(ge=date.today())]

    class Config:
        from_attributes = True