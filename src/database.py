from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

def setup_database(DATABASE_URL=""):
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_db = os.getenv('POSTGRES_DB')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = os.getenv('POSTGRES_PORT')

    if DATABASE_URL == "":
        DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    database = Database(DATABASE_URL)
    Base = declarative_base()

    return SessionLocal, database, Base, engine
