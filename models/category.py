from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel

class Category(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, description="分类名称")
    name_zh: Optional[str] = Field(max_length=100, default=None, description="分类中文名称")
    slug: str = Field(max_length=100, unique=True, description="URL友好的分类标识符")
    description: Optional[str] = Field(max_length=500, default=None, description="分类描述")
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id", description="父分类ID，用于实现分类层级")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}, description="更新时间")
    
    # 关系定义
    parent: Optional["Category"] = Relationship(back_populates="children", sa_relationship_kwargs={'remote_side': 'Category.id'})
    children: List["Category"] = Relationship(back_populates="parent")
    articles: List["Article"] = Relationship(back_populates="category")