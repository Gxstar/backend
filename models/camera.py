from typing import Optional, List
from sqlmodel import Field, Relationship
from models.base import BaseSQLModel
from models.brand import Brand

class Camera(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, description="相机名称")
    name_zh: Optional[str] = Field(max_length=200, default=None, description="相机中文名称")
    brand_id: int = Field(foreign_key="brand.id", description="品牌ID")
    model_code: Optional[str] = Field(max_length=50, default=None, description="型号代码")
    release_year: int = Field(description="发布年份")
    sensor_type: str = Field(max_length=50, description="传感器类型")
    sensor_size: str = Field(max_length=50, description="传感器尺寸")
    resolution: Optional[float] = Field(default=None, description="分辨率(MP)")
    max_iso: Optional[int] = Field(default=None, description="最高ISO")
    video_resolution: Optional[str] = Field(max_length=50, default=None, description="视频分辨率")
    body_weight: Optional[int] = Field(default=None, description="机身重量(g)")
    description: Optional[str] = Field(default=None, description="相机描述")
    mount_id: Optional[int] = Field(default=None, foreign_key="mount.id")
    type: Optional[str] = Field(max_length=50, default=None)
    iso_range: Optional[str] = Field(max_length=50, default=None)
    shutter_speed: Optional[str] = Field(max_length=50, default=None)
    dimensions: Optional[str] = Field(max_length=50, default=None)
    
    # 关系定义
    brand: Brand = Relationship(back_populates="cameras")
    ratings: List["Rating"] = Relationship(back_populates="camera")