from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MountBase(BaseModel):
    name: str
    brand_id: Optional[int] = None
    release_year: Optional[int] = None
    flange_distance: Optional[float] = None
    diameter: Optional[float] = None
    description: Optional[str] = None


class MountCreate(MountBase):
    pass


class Mount(MountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True