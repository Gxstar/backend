from typing import Optional, List
from sqlmodel import Field, Relationship
from models.base import BaseSQLModel
import sqlalchemy as sa

class UserBase(BaseSQLModel):
    username: str = Field(sa_column=sa.Column(sa.String(50), unique=True), description="用户名")
    email: str = Field(sa_column=sa.Column(sa.String(100), unique=True), description="电子邮箱")
    full_name: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="姓名")
    is_active: bool = Field(default=True, description="是否激活")
    is_staff: bool = Field(default=False, description="是否为管理员")

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(sa_column=sa.Column(sa.String(255)), description="密码哈希")
    
    # 关系定义
    articles: List["Article"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")
    ratings: List["Rating"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str = Field(description="用户密码")

class UserRead(UserBase):
    id: int

class UserUpdate(BaseSQLModel):
    email: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="电子邮箱")
    full_name: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="姓名")
    is_active: Optional[bool] = Field(default=None, description="是否激活")
    is_staff: Optional[bool] = Field(default=None, description="是否为管理员")
    password: Optional[str] = Field(default=None, description="用户密码")