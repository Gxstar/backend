from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, server_default='user')
    full_name = Column(String(100))
    avatar_url = Column(String(255))
    bio = Column(Text)
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    created_cameras = relationship('Camera', back_populates='creator')
    created_lenses = relationship('Lens', back_populates='creator')