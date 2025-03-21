from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password = Column(String)
    email = Column(String, index=True, nullable=False, unique=True)
    full_name = Column(String)

    task = relationship('TaskModel', back_populates='user', cascade='all, delete-orphan')

class User(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None

    class Config:
        from_attributes = True


class TaskModel(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(Integer)
    deadline = Column(String)

    user = relationship('UserModel', back_populates='task')

class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: int
    deadline: str

    class Config:
        from_attributes = True