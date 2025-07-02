from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseSQLModel

class Camera(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model: str = Field(max_length=100)
    model_zh: Optional[str] = Field(max_length=100, default=None)
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    release_year: Optional[int] = Field(default=None)
    # 添加评分字段：0-5分，精确到小数点后一位
    rating: Optional[Decimal] = Field(default=None, ge=Decimal('0.0'), le=Decimal('5.0'), max_digits=2, decimal_places=1)
    # 添加评分人数字段：非负整数
    rating_count: int = Field(default=0, ge=0)
    mount_id: Optional[int] = Field(default=None, foreign_key="mount.id")
    release_year: Optional[int] = Field(default=None)
    type: Optional[str] = Field(max_length=50, default=None)
    sensor_size: Optional[str] = Field(max_length=50, default=None)
    megapixels: Optional[float] = Field(default=None)
    iso_range: Optional[str] = Field(max_length=50, default=None)
    shutter_speed: Optional[str] = Field(max_length=50, default=None)
    weight_grams: Optional[int] = Field(default=None)
    dimensions: Optional[str] = Field(max_length=50, default=None)
    description: Optional[str] = Field(default=None,max_length=500)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)