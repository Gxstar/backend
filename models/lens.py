from typing import Optional, List
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.brand import Brand
from models.lens_mount_link import LensMountLink
from models.mount import Mount

class Lens(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model: str = Field(max_length=100)
    model_zh: Optional[str] = Field(max_length=100, default=None)
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    # 添加评分字段：0-5分，精确到小数点后一位
    rating: Optional[Decimal] = Field(default=None, ge=Decimal('0.0'), le=Decimal('5.0'), max_digits=2, decimal_places=1)
    # 添加评分人数字段：非负整数
    rating_count: int = Field(default=0, ge=0)
    focal_length: Optional[str] = Field(max_length=50, default=None)
    aperture_range: Optional[str] = Field(max_length=50, default=None)
    mount_id: Optional[int] = Field(default=None, foreign_key="mount.id")
    lens_type: Optional[str] = Field(max_length=50, default=None)
    min_focus_distance: Optional[float] = Field(default=None)
    max_aperture: Optional[float] = Field(default=None)
    weight_grams: Optional[int] = Field(default=None)
    dimensions: Optional[str] = Field(max_length=50, default=None)
    description: Optional[str] = Field(default=None, max_length=500)
    # 定义与Mount的多对多关系
    mounts: List["Mount"] = Relationship(back_populates="lenses", link_model=LensMountLink)
    
    # 关系定义
    brand: Brand = Relationship(back_populates="lenses")
    mounts: List[Mount] = Relationship(back_populates="lenses", link_model=LensMountLink)
    ratings: List["Rating"] = Relationship(back_populates="lens")