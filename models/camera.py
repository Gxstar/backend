from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, Text, CheckConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Camera(Base):
    __tablename__ = 'camera'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(100), nullable=False)
    model_zh = Column(String(100))
    brand_id = Column(Integer, ForeignKey('brand.id'))
    mount_id = Column(Integer, ForeignKey('mount.id'))
    release_year = Column(Integer)
    type = Column(String(50))
    sensor_size = Column(String(50))
    megapixels = Column(DECIMAL(5, 2))
    iso_range = Column(String(50))
    shutter_speed = Column(String(50))
    weight_grams = Column(Integer)
    dimensions = Column(String(50))
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
        CheckConstraint("type IN ('DSLR', 'Mirrorless', 'Compact', 'Film', 'Other')", name='chk_camera_type'),
    )

    brand = relationship('Brand', back_populates='cameras')
    mount = relationship('Mount', back_populates='cameras')
    creator = relationship('User', back_populates='created_cameras')