from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import postgresql_password

DATABASE_URL = f'postgresql://postgres:{postgresql_password}@localhost:5432/taskdb'
engine = create_engine(DATABASE_URL)
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