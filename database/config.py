import os
from typing import Generator
from dotenv import load_dotenv
from sqlmodel import create_engine,Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db()->Generator[Session,None,None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()