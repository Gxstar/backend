from typing import Optional, List
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
import sqlalchemy as sa

class CategoryBase(BaseSQLModel):
    name: str = Field(sa_column=sa.Column(sa.String(100), unique=True), description="分类名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="分类中文名称")
    slug: str = Field(sa_column=sa.Column(sa.String(100), unique=True), description="URL友好的分类标识符")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="分类描述")
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id", description="父分类ID，用于实现分类层级")

class Category(CategoryBase, BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 关系定义
    parent: Optional["Category"] = Relationship(back_populates="children", sa_relationship_kwargs={'remote_side': 'Category.id'})
    children: List["Category"] = Relationship(back_populates="parent")
    articles: List["Article"] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    """用于创建分类的模型"""
    pass

class CategoryRead(CategoryBase):
    """用于读取分类的模型，包含ID"""
    id: int

class CategoryUpdate(SQLModel):
    """用于更新分类的模型，所有字段均为可选"""
    name: Optional[str] = None
    name_zh: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None