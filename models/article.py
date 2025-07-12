from typing import Optional, List
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship, Text
from models.base import BaseSQLModel
from models.user import User
from models.category import Category
from models.article_tag_link import ArticleTagLink
from models.tag import Tag
import sqlalchemy as sa

class ArticleBase(SQLModel):
    title: str = Field(sa_column=sa.Column(sa.String(200)), description="文章标题")
    title_zh: Optional[str] = Field(max_length=200, default=None, description="文章中文标题")
    slug: str = Field(sa_column=sa.Column(sa.String(255), unique=True), description="URL友好的标题")
    content: str = Field(sa_column=sa.Column(sa.Text), description="文章内容")
    excerpt: Optional[str] = Field(max_length=500, default=None, description="文章摘要")
    category_id: int = Field(foreign_key="category.id", description="分类ID")
    status: str = Field(sa_column=sa.Column(sa.String(20)), default="draft", description="文章状态")
    view_count: int = Field(default=0, ge=0, description="阅读量")
    like_count: int = Field(default=0, ge=0, description="点赞数")
    comment_count: int = Field(default=0, ge=0, description="评论数")
    published_at: Optional[dt] = Field(default=None, description="发布时间")

class Article(ArticleBase, BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id", description="作者ID")
    # 关系定义
    author: User = Relationship(back_populates="articles")
    category: Category = Relationship(back_populates="articles")
    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)
    comments: List["Comment"] = Relationship(back_populates="article", sa_relationship_kwargs={
        "primaryjoin": "and_(Article.id == Comment.target_id, Comment.target_type == 'article')"
    })

# 数据创建模型
class ArticleCreate(ArticleBase):
    pass

# 数据更新模型
class ArticleUpdate(ArticleBase):
    title: Optional[str] = Field(max_length=200, default=None, description="文章标题")
    title_zh: Optional[str] = Field(max_length=200, default=None, description="文章中文标题")
    slug: Optional[str] = Field(max_length=255, default=None, description="URL友好的标识符")
    content: Optional[str] = Field(default=None, description="文章内容")
    excerpt: Optional[str] = Field(max_length=500, default=None, description="文章摘要")
    category_id: Optional[int] = Field(default=None, description="分类ID")
    status: Optional[str] = Field(max_length=20, default=None, description="文章状态")
    published_at: Optional[dt] = Field(default=None, description="发布时间")

# 数据读取模型
class ArticleRead(ArticleBase):
    id: int
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None