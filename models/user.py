from typing import Optional, List
from sqlmodel import Field, Relationship
from models.base import BaseSQLModel

class User(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, description="用户名")
    email: str = Field(max_length=100, unique=True, description="电子邮箱")
    password_hash: str = Field(max_length=255, description="密码哈希")
    full_name: Optional[str] = Field(max_length=100, default=None, description="姓名")
    is_active: bool = Field(default=True, description="是否激活")
    is_staff: bool = Field(default=False, description="是否为管理员")
    
    # 关系定义
    articles: List["Article"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")
    ratings: List["Rating"] = Relationship(back_populates="user")