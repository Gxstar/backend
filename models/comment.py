from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.user import User
from sqlmodel import Field, SQLModel
from sqlalchemy import Text

class Comment(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(sa_type=Text(), description="评论内容")
    author_id: int = Field(foreign_key="user.id", description="评论作者ID")
    target_type: str = Field(max_length=20, description="关联目标类型: article-文章, camera-相机, lens-镜头")
    target_id: int = Field(description="关联目标ID")
    parent_id: Optional[int] = Field(default=None, foreign_key="comment.id", description="父评论ID，用于实现评论回复")
    is_approved: bool = Field(default=True, description="是否审核通过")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}, description="更新时间")
    
    # 关系定义
    author: User = Relationship(back_populates="comments")
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
class CommentCreate(SQLModel):
    content: str = Field(description="评论内容")
    target_type: str = Field(max_length=20, description="关联目标类型: article-文章, camera-相机, lens-镜头")
    target_id: int = Field(description="关联目标ID")
    parent_id: Optional[int] = Field(default=None, description="父评论ID，用于实现评论回复")

# 数据更新模型
class CommentUpdate(SQLModel):
    content: Optional[str] = Field(default=None, description="评论内容")
    is_approved: Optional[bool] = Field(default=None, description="是否审核通过")

# 数据读取模型
class CommentRead(SQLModel):
    id: int
    content: str
    author_id: int
    target_type: str
    target_id: int
    parent_id: Optional[int]
    is_approved: bool
    created_at: datetime
    updated_at: datetime