from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Text
from models.base import BaseSQLModel
from models.user import User
from models.category import Category
from models.article_tag_link import ArticleTagLink
from models.tag import Tag

class Article(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, description="文章标题")
    title_zh: Optional[str] = Field(max_length=200, default=None, description="文章中文标题")
    slug: str = Field(max_length=255, unique=True, description="URL友好的标识符")
    # 将content字段类型改为TEXT以支持长文本
    content: str = Field(sa_type=Text(), description="文章内容")
    excerpt: Optional[str] = Field(max_length=500, default=None, description="文章摘要")
    author_id: int = Field(foreign_key="user.id", description="作者ID")
    category_id: int = Field(foreign_key="category.id", description="分类ID")
    status: str = Field(max_length=20, default="draft", description="文章状态: draft-草稿, published-已发布, archived-已归档")
    view_count: int = Field(default=0, ge=0, description="阅读量")
    like_count: int = Field(default=0, ge=0, description="点赞数")
    comment_count: int = Field(default=0, ge=0, description="评论数")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}, description="更新时间")
    published_at: Optional[datetime] = Field(default=None, description="发布时间")
    
    # 关系定义
    author: User = Relationship(back_populates="articles")
    category: Category = Relationship(back_populates="articles")
    tags: List[Tag] = Relationship(back_populates="articles", link_model=ArticleTagLink)
    comments: List["Comment"] = Relationship(back_populates="article", sa_relationship_kwargs={
        "primaryjoin": "and_(Article.id == Comment.target_id, Comment.target_type == 'article')"
    })

# 数据创建模型
class ArticleCreate(SQLModel):
    title: str = Field(max_length=200, description="文章标题")
    title_zh: Optional[str] = Field(max_length=200, default=None, description="文章中文标题")
    slug: str = Field(max_length=255, unique=True, description="URL友好的标识符")
    content: str = Field(description="文章内容")
    excerpt: Optional[str] = Field(max_length=500, default=None, description="文章摘要")
    category_id: int = Field(description="分类ID")
    status: str = Field(max_length=20, default="draft", description="文章状态: draft-草稿, published-已发布, archived-已归档")
    published_at: Optional[datetime] = Field(default=None, description="发布时间")

# 数据更新模型
class ArticleUpdate(SQLModel):
    title: Optional[str] = Field(max_length=200, default=None, description="文章标题")
    title_zh: Optional[str] = Field(max_length=200, default=None, description="文章中文标题")
    slug: Optional[str] = Field(max_length=255, default=None, description="URL友好的标识符")
    content: Optional[str] = Field(default=None, description="文章内容")
    excerpt: Optional[str] = Field(max_length=500, default=None, description="文章摘要")
    category_id: Optional[int] = Field(default=None, description="分类ID")
    status: Optional[str] = Field(max_length=20, default=None, description="文章状态")
    published_at: Optional[datetime] = Field(default=None, description="发布时间")

# 数据读取模型
class ArticleRead(SQLModel):
    id: int
    title: str
    title_zh: Optional[str]
    slug: str
    content: str
    excerpt: Optional[str]
    author_id: int
    category_id: int
    status: str
    view_count: int
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]