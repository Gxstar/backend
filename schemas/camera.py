from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CameraBase(BaseModel):
    model: str
    model_zh: Optional[str] = None
    brand_id: Optional[int] = None
    mount_id: Optional[int] = None
    release_year: Optional[int] = None
    type: Optional[str] = None
    sensor_size: Optional[str] = None
    megapixels: Optional[float] = None
    iso_range: Optional[str] = None
    shutter_speed: Optional[str] = None
    weight_grams: Optional[int] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[int] = None


class CameraCreate(CameraBase):
    pass


class Camera(CameraBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True