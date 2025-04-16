from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True)
    email: str = Field(max_length=255, unique=True)
    password_hash: str = Field(max_length=255)
    role: str = Field(default='user', max_length=20)
    full_name: Optional[str] = Field(max_length=100, default=None)
    avatar_url: Optional[str] = Field(max_length=255, default=None)
    bio: Optional[str] = Field(default=None)
    last_login: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)