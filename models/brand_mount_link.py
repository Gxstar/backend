from typing import Optional
from sqlmodel import SQLModel, Field
from models.base import BaseSQLModel

class BrandMountLink(BaseSQLModel, table=True):
    """
    品牌和卡口的关联表模型
    用于建立多对多关系
    """
    brand_id: Optional[int] = Field(
        default=None, 
        foreign_key="brand.id", 
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