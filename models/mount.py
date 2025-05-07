from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from models.base import BaseSQLModel

class Mount(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    release_year: Optional[int] = Field(default=None)
    flange_distance: Optional[float] = Field(default=None)
    diameter: Optional[float] = Field(default=None)
    description: Optional[str] = Field(default=None,max_length=500)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)