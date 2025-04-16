import os
from dotenv import load_dotenv
from sqlmodel import create_engine,Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")
if not DATABASE_URL:
    raise ValueError("Missing SQLALCHEMY_DATABASE_URI in environment variables")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,      # 建议根据实际负载调整
    max_overflow=10,  # 生产环境可能需要更大
    pool_recycle=3600,
    connect_args={"connect_timeout": 5}  # 新增关键参数
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,class_=Session)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()