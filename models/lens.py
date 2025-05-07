from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from models.base import BaseSQLModel

class Lens(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model: str = Field(max_length=100)
    model_zh: Optional[str] = Field(max_length=100, default=None)
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    mount_id: Optional[int] = Field(default=None, foreign_key="mount.id")
    release_year: Optional[int] = Field(default=None)
    focal_length: str = Field(max_length=50)
    aperture: str = Field(max_length=50)
    lens_type: Optional[str] = Field(max_length=50, default=None)
    filter_size: Optional[float] = Field(default=None)
    weight_grams: Optional[int] = Field(default=None)
    dimensions: Optional[str] = Field(max_length=50, default=None)
    description: Optional[str] = Field(default=None,max_length=500)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)