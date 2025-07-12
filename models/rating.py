from typing import Optional, List
import sqlalchemy as sa
from sqlmodel import Field, Relationship
from models.base import BaseSQLModel
from models.user import User
from models.camera import Camera
from models.lens import Lens

class RatingBase(BaseSQLModel):
    target_type: str = Field(sa_column=sa.Column(sa.String(20)), description="评分对象类型: camera-相机, lens-镜头")
    target_id: int = Field(description="评分对象ID")
    score: float = Field(ge=1, le=5, description="评分值，范围1-5分")
    comment: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="评分评论")

class Rating(RatingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 关系定义
    user: Optional[User] = Relationship(back_populates="ratings")
    camera: Optional[Camera] = Relationship(
        back_populates="ratings",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Rating.target_id == Camera.id, Rating.target_type == 'camera')",
            "foreign_keys": "Rating.target_id"
        }
    )
    lens: Optional[Lens] = Relationship(
        back_populates="ratings",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Rating.target_id == Lens.id, Rating.target_type == 'lens')",
            "foreign_keys": "Rating.target_id"
        }
    )

    class Config:
        # 添加联合唯一索引，确保一个用户只能对一个对象评一次分
        indexes = [
            ["user_id", "target_type", "target_id"],
        ]

class RatingCreate(RatingBase):
    pass

class RatingRead(RatingBase):
    id: int

class RatingUpdate(BaseSQLModel):
    target_type: Optional[str] = Field(sa_column=sa.Column(sa.String(20)), default=None, description="评分对象类型: camera-相机, lens-镜头")
    target_id: Optional[int] = Field(default=None, description="评分对象ID")
    score: Optional[float] = Field(ge=1, le=5, default=None, description="评分值，范围1-5分")
    comment: Optional[str] = Field(sa_column=sa.Column(sa.String(500)), default=None, description="评分评论")