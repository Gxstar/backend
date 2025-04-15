from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base

class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='品牌ID，自增主键')
    name = Column(String(100), unique=True, nullable=False, comment='品牌英文名称，唯一')
    name_zh = Column(String(100), comment='品牌中文名称')
    country = Column(String(50), comment='品牌所属国家')
    founded_year = Column(Integer, comment='品牌创立年份')
    website = Column(String(255), comment='品牌官方网站URL')
    description = Column(Text, comment='品牌详细描述')
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='记录创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='记录更新时间')