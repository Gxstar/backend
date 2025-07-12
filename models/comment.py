import sqlalchemy as sa
from typing import Optional, List
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.user import User
from sqlmodel import Field, SQLModel
from sqlalchemy import Text

class CommentBase(SQLModel):
    content: str = Field(sa_column=sa.Column(sa.Text), description="评论内容")
    target_type: str = Field(max_length=20, description="关联目标类型: article-文章, camera-相机, lens-镜头")
    target_id: int = Field(description="关联目标ID")
    parent_id: Optional[int] = Field(default=None, foreign_key="comment.id", description="父评论ID，用于实现评论回复")

class Comment(CommentBase, BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="user.id", description="评论作者ID")
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", description="文章ID")
    is_approved: bool = Field(default=True, description="是否审核通过")
    
    # 一对多关系：一个评论属于一篇文章
    article: Optional["Article"] = Relationship(back_populates="comments")
    # 一对多关系：一个评论属于一个作者
    author: Optional["User"] = Relationship(back_populates="comments")
    # 自引用关系：评论回复功能
    parent: Optional["Comment"] = Relationship(back_populates="children")
    children: List["Comment"] = Relationship(back_populates="parent")
    
    # 修正关系定义：显式指定外键关联
    article: Optional["Article"] = Relationship(
        back_populates="comments",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Comment.target_type == 'article', Comment.target_id == Article.id)",
            "foreign_keys": "Comment.target_id",
            "overlaps": "children,parent"
        }
    )

# 数据创建模型
class CommentCreate(CommentBase):
    """用于创建评论的模型"""
    pass

# 数据更新模型
class CommentUpdate(SQLModel):
    content: Optional[str] = Field(default=None, description="评论内容")
    is_approved: Optional[bool] = Field(default=None, description="是否审核通过")

# 数据读取模型
class CommentRead(CommentBase):
    """用于读取评论的模型，包含ID和审核状态"""
    id: int
    author_id: int
    is_approved: bool