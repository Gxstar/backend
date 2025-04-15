from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BrandBase(BaseModel):
    name: str
    name_zh: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True