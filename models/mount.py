from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.brand_mount_link import BrandMountLink
from models.lens_mount_link import LensMountLink
import sqlalchemy as sa

class Mount(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String(100), unique=True))
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None)
    release_year: Optional[int] = Field(default=None)
    flange_distance: Optional[float] = Field(default=None)
    diameter: Optional[float] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=500)
    # 定义与Brand的多对多关系
    brands: List["Brand"] = Relationship(back_populates="mounts", link_model=BrandMountLink)
    # 定义与Lens的多对多关系
    lenses: List["Lens"] = Relationship(back_populates="mounts", link_model=LensMountLink)