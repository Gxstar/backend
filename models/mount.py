from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, Text
from sqlalchemy.orm import relationship

from .base import Base


class Mount(Base):
    __tablename__ = 'mount'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    release_year = Column(Integer)
    flange_distance = Column(DECIMAL(5, 2))
    diameter = Column(DECIMAL(5, 2))
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    brand = relationship('Brand', back_populates='mounts')
    cameras = relationship('Camera', back_populates='mount')
    lenses = relationship('Lens', back_populates='mount')