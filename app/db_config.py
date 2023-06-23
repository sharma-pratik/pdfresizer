from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DB_USER = os.environ["POSTGRES_USER"]
DB_PWD = os.environ["POSTGRES_PASSWORD"]
DB_NAME = os.environ["POSTGRES_DB"]
    

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PWD}@localhost/{DB_NAME}"

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

DB = session_maker()