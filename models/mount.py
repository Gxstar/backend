from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.lens_mount_link import LensMountLink

class Mount(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    release_year: Optional[int] = Field(default=None)
    flange_distance: Optional[float] = Field(default=None)
    diameter: Optional[float] = Field(default=None)
    description: Optional[str] = Field(default=None,max_length=500)
    # 定义与Lens的多对多关系
    lenses: List["Lens"] = Relationship(back_populates="mounts", link_model=LensMountLink)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)