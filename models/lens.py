from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, Text, CheckConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Lens(Base):
    __tablename__ = 'lens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(100), nullable=False)
    model_zh = Column(String(100))
    brand_id = Column(Integer, ForeignKey('brand.id'))
    mount_id = Column(Integer, ForeignKey('mount.id'))
    release_year = Column(Integer)
    focal_length = Column(String(50), nullable=False)
    aperture = Column(String(50), nullable=False)
    lens_type = Column(String(50))
    filter_size = Column(DECIMAL(5, 2))
    weight_grams = Column(Integer)
    dimensions = Column(String(50))
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
        CheckConstraint("lens_type IN ('Prime', 'Zoom', 'Macro', 'Wide', 'Telephoto', 'Other')", name='chk_lens_type'),
    )

    brand = relationship('Brand', back_populates='lenses')
    mount = relationship('Mount', back_populates='lenses')
    creator = relationship('User', back_populates='created_lenses')