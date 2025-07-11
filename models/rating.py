from typing import Optional, List
from sqlmodel import Field, Relationship
from models.base import BaseSQLModel
from models.user import User
from models.camera import Camera
from models.lens import Lens

class Rating(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_type: str = Field(max_length=20, description="评分对象类型: camera-相机, lens-镜头")
    target_id: int = Field(description="评分对象ID")
    score: float = Field(ge=1, le=5, description="评分值，范围1-5分")
    comment: Optional[str] = Field(max_length=500, default=None, description="评分评论")
    
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
            ["created_by", "target_type", "target_id"],
        ]