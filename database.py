from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = 'sqlite:///task_manager.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    '''
    get_db is for dependancy injection so i can access the database easily
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()