from typing import Optional
from sqlmodel import SQLModel, Field
from models.base import BaseSQLModel

class ArticleTagLink(BaseSQLModel, table=True):
    """
    文章和标签的关联表模型
    用于建立多对多关系
    """
    article_id: Optional[int] = Field(
        default=None, 
        foreign_key="article.id", 
        primary_key=True, 
        description="文章ID"
    )
    tag_id: Optional[int] = Field(
        default=None, 
        foreign_key="tag.id", 
        primary_key=True, 
        description="标签ID"
    )