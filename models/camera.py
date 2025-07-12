from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime as dt
import sqlalchemy as sa
from .base import BaseSQLModel
from .brand import Brand

# 基础模型 - 包含所有公共字段定义
class CameraBase(SQLModel):
    name: str = Field(sa_column=sa.Column(sa.String(200)), description="相机名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(200)), default=None, description="相机中文名称")
    brand_id: int = Field(foreign_key="brand.id", description="品牌ID")
    model_code: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="型号代码")
    release_year: int = Field(description="发布年份")
    sensor_type: str = Field(sa_column=sa.Column(sa.String(50)), description="传感器类型")
    sensor_size: str = Field(sa_column=sa.Column(sa.String(50)), description="传感器尺寸")
    resolution: Optional[float] = Field(default=None, description="分辨率(MP)")
    max_iso: Optional[int] = Field(default=None, description="最高ISO")
    video_resolution: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="视频分辨率")
    body_weight: Optional[int] = Field(default=None, description="机身重量(g)")
    description: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="相机描述")
    mount_id: Optional[int] = Field(default=None, description="卡口ID")
    type: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="相机类型")
    iso_range: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="ISO范围")
    shutter_speed: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="快门速度范围")
    dimensions: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="尺寸")

# 数据库模型 - 继承基础模型和BaseSQLModel
class Camera(CameraBase, BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 关系定义
    brand: Brand = Relationship(back_populates="cameras")
    ratings: List["Rating"] = Relationship(back_populates="camera")

# 数据创建模型 - 继承基础模型
class CameraCreate(CameraBase):
    pass

# 数据更新模型 - 所有字段设为可选
class CameraUpdate(SQLModel):
    name: Optional[str] = Field(sa_column=sa.Column(sa.String(200)), default=None, description="相机名称")
    name_zh: Optional[str] = Field(sa_column=sa.Column(sa.String(200)), default=None, description="相机中文名称")
    brand_id: Optional[int] = Field(default=None, description="品牌ID")
    model_code: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="型号代码")
    release_year: Optional[int] = Field(default=None, description="发布年份")
    sensor_type: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="传感器类型")
    sensor_size: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="传感器尺寸")
    resolution: Optional[float] = Field(default=None, description="分辨率(MP)")
    max_iso: Optional[int] = Field(default=None, description="最高ISO")
    video_resolution: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="视频分辨率")
    body_weight: Optional[int] = Field(default=None, description="机身重量(g)")
    description: Optional[str] = Field(default=None, description="相机描述")
    mount_id: Optional[int] = Field(default=None, description="卡口ID")
    type: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="相机类型")
    iso_range: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="ISO范围")
    shutter_speed: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="快门速度范围")
    dimensions: Optional[str] = Field(sa_column=sa.Column(sa.String(50)), default=None, description="尺寸")

# 数据读取模型 - 继承基础模型并添加ID和时间戳字段
class CameraRead(CameraBase):
    id: int
    created_at: dt
    updated_at: dt
    
    class Config:
        arbitrary_types_allowed = True