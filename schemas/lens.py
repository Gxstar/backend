from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LensBase(BaseModel):
    model: str
    model_zh: Optional[str] = None
    brand_id: Optional[int] = None
    mount_id: Optional[int] = None
    release_year: Optional[int] = None
    focal_length: str
    aperture: str
    lens_type: Optional[str] = None
    filter_size: Optional[float] = None
    weight_grams: Optional[int] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[int] = None


class LensCreate(LensBase):
    pass


class Lens(LensBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True