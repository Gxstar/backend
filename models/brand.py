from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.brand_mount_link import BrandMountLink

class Brand(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    name_zh: Optional[str] = Field(max_length=100, default=None)
    country: Optional[str] = Field(max_length=50, default=None)
    founded_year: Optional[int] = Field(default=None)
    website: Optional[str] = Field(max_length=255, default=None)
    description: Optional[str] = Field(default=None, max_length=500)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    # 定义与Mount的多对多关系
    mounts: List["Mount"] = Relationship(back_populates="brands", link_model=BrandMountLink)