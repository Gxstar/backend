from typing import Optional, List
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.brand_mount_link import BrandMountLink
from models.lens_mount_link import LensMountLink
import sqlalchemy as sa

class MountBase(SQLModel):
    """卡口基础模型，包含所有公共字段"""
    name: str = Field(sa_column=sa.Column(sa.String(100), unique=True), description="卡口名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="卡口中文名称")
    release_year: Optional[int] = Field(default=None, description="发布年份")
    flange_distance: Optional[float] = Field(default=None, description="法兰距")
    diameter: Optional[float] = Field(default=None, description="卡口直径")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="描述")

class Mount(MountBase, BaseSQLModel, table=True):
    """卡口数据库模型，映射到数据库表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    # 定义与Brand的多对多关系
    brands: List["Brand"] = Relationship(back_populates="mounts", link_model=BrandMountLink)
    # 定义与Lens的多对多关系
    lenses: List["Lens"] = Relationship(back_populates="mounts", link_model=LensMountLink)

class MountCreate(MountBase):
    """卡口创建模型，用于API创建请求"""
    pass

class MountRead(MountBase):
    """卡口读取模型，用于API响应"""
    id: int
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

    class Config:
        arbitrary_types_allowed = True

class MountUpdate(SQLModel):
    """卡口更新模型，用于API更新请求，所有字段为可选"""
    name: Optional[str] = Field(sa_column=sa.Column(sa.String(100), unique=True), default=None, description="卡口名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="卡口中文名称")
    release_year: Optional[int] = Field(default=None, description="发布年份")
    flange_distance: Optional[float] = Field(default=None, description="法兰距")
    diameter: Optional[float] = Field(default=None, description="卡口直径")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="描述")