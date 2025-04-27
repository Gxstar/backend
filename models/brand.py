from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Brand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    name_zh: Optional[str] = Field(max_length=100, default=None)
    country: Optional[str] = Field(max_length=50, default=None)
    founded_year: Optional[str] = Field(default=None)
    website: Optional[str] = Field(max_length=255, default=None)
    description: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})