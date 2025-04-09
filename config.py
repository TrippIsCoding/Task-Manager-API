import os
from dotenv import load_dotenv

if os.getenv('RENDER') != True:
    load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ADMIN_KEY = os.getenv('ADMIN_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')