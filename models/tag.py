from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.article_tag_link import ArticleTagLink

class Tag(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, description="标签名称")
    slug: str = Field(max_length=50, unique=True, description="URL友好的标签标识符")
    description: Optional[str] = Field(max_length=200, default=None, description="标签描述")
    
    # 关系定义
    articles: List["Article"] = Relationship(back_populates="tags", link_model=ArticleTagLink)