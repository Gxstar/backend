from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from models.base import BaseSQLModel

class LensMountLink(BaseSQLModel, table=True):
    """
    镜头和卡口的关联表模型
    用于建立多对多关系
    """
    lens_id: Optional[int] = Field(
        default=None, 
        foreign_key="lens.id", 
        primary_key=True, 
        index=True
    )
    mount_id: Optional[int] = Field(
        default=None, 
        foreign_key="mount.id", 
        primary_key=True, 
        index=True
    )
    is_primary: bool = Field(default=False, description="是否为主打卡口")