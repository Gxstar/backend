from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

# 定义一个用于 Alembic 的基类，包含所有模型的通用字段
class BaseSQLModel(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="创建时间")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}, description="更新时间")
    created_by: Optional[int] = Field(default=None, foreign_key="user.id", description="创建人ID")