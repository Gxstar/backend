import sqlalchemy as sa
from typing import Optional, List
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.brand_mount_link import BrandMountLink

# 基础模型 - 包含所有公共字段定义
class BrandBase(SQLModel):
    name: str = Field(sa_column=sa.Column(sa.String(100), unique=True, index=True), description="品牌名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="品牌中文名称")
    country: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="品牌国家")
    founded_year: Optional[int] = Field(default=None, description="成立年份")
    website: Optional[str] = Field(sa_column=sa.Column(sa.String(255)), default=None, description="官方网站")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="品牌描述")

# 数据库模型 - 继承基础模型和BaseSQLModel
class Brand(BrandBase, BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 定义与Mount的多对多关系
    mounts: List["Mount"] = Relationship(back_populates="brands", link_model=BrandMountLink)
    # 定义与Camera的一对多关系
    cameras: List["Camera"] = Relationship(back_populates="brand")

# 数据创建模型 - 继承基础模型
class BrandCreate(BrandBase):
    pass

# 数据更新模型 - 所有字段设为可选
class BrandUpdate(SQLModel):
    name: Optional[str] = Field(sa_column=sa.Column(sa.String(100), unique=True, index=True), default=None, description="品牌名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="品牌中文名称")
    country: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="品牌国家")
    founded_year: Optional[int] = Field(default=None, description="成立年份")
    website: Optional[str] = Field(sa_column=sa.Column(sa.String(255)), default=None, description="官方网站")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="品牌描述")

# 数据读取模型 - 继承基础模型并添加ID和时间戳字段
class BrandRead(BrandBase):
    id: int
    created_at: dt
    updated_at: dt
    
    class Config:
        arbitrary_types_allowed = True