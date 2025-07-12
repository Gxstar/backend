from typing import Optional, List
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.article_tag_link import ArticleTagLink
import sqlalchemy as sa

class TagBase(SQLModel):
    name: str = Field(sa_column=sa.Column(sa.String(50), unique=True), description="标签名称")
    slug: str = Field(sa_column=sa.Column(sa.String(50), unique=True), description="URL友好的标签标识符")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(200)), default=None, description="标签描述")

class Tag(TagBase, BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 关系定义
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)

class TagCreate(TagBase):
    """用于创建标签的模型"""
    pass

class TagRead(TagBase):
    """用于读取标签的模型，包含ID"""
    id: int

class TagUpdate(SQLModel):
    """用于更新标签的模型，所有字段均为可选"""
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None