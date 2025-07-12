from typing import Optional, List
from decimal import Decimal
from datetime import datetime as dt
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel
from models.brand import Brand
from models.lens_mount_link import LensMountLink
from models.mount import Mount
import sqlalchemy as sa

class LensBase(SQLModel):
    """镜头基础模型，包含所有公共字段"""
    model: str = Field(sa_column=sa.Column(sa.String(100)), description="镜头型号")
    model_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="镜头中文型号")
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id", description="品牌ID")
    # 添加评分字段：0-5分，精确到小数点后一位
    rating: Optional[Decimal] = Field(default=None, ge=Decimal('0.0'), le=Decimal('5.0'), max_digits=2, decimal_places=1, description="评分")
    # 添加评分人数字段：非负整数
    rating_count: int = Field(default=0, ge=0, description="评分人数")
    focal_length: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="焦距范围")
    aperture_range: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="光圈范围")
    lens_type: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="镜头类型")
    min_focus_distance: Optional[float] = Field(default=None, description="最小对焦距离")
    max_aperture: Optional[float] = Field(default=None, description="最大光圈")
    weight_grams: Optional[int] = Field(default=None, description="重量(克)")
    dimensions: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="尺寸")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="描述")

class Lens(LensBase, BaseSQLModel, table=True):
    """镜头数据库模型，映射到数据库表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    # 关系定义
    brand: Brand = Relationship(back_populates="lenses")
    mounts: List[Mount] = Relationship(back_populates="lenses", link_model=LensMountLink)
    ratings: List["Rating"] = Relationship(back_populates="lens")

class LensCreate(LensBase):
    """镜头创建模型，用于API创建请求"""
    pass

class LensRead(LensBase):
    """镜头读取模型，用于API响应"""
    id: int
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

    class Config:
        arbitrary_types_allowed = True

class LensUpdate(SQLModel):
    """镜头更新模型，用于API更新请求，所有字段为可选"""
    model: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="镜头型号")
    model_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(100)), default=None, description="镜头中文型号")
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id", description="品牌ID")
    rating: Optional[Decimal] = Field(default=None, ge=Decimal('0.0'), le=Decimal('5.0'), max_digits=2, decimal_places=1, description="评分")
    rating_count: Optional[int] = Field(default=None, ge=0, description="评分人数")
    focal_length: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="焦距范围")
    aperture_range: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="光圈范围")
    lens_type: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="镜头类型")
    min_focus_distance: Optional[float] = Field(default=None, description="最小对焦距离")
    max_aperture: Optional[float] = Field(default=None, description="最大光圈")
    weight_grams: Optional[int] = Field(default=None, description="重量(克)")
    dimensions: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="尺寸")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="描述")