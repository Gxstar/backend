from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from database.config import get_db
from models.rating import Rating, RatingCreate, RatingRead, RatingUpdate
from models.user import User
from auth.auth import get_current_user

router = APIRouter(tags=["ratings"], prefix="/ratings")

@router.post("/", response_model=RatingRead, status_code=status.HTTP_201_CREATED)
def create_rating(
    rating: RatingCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 检查是否已存在相同用户对同一对象的评分
    existing_rating = session.exec(
        select(Rating)
        .where(Rating.user_id == current_user.id)
        .where(Rating.target_type == rating.target_type)
        .where(Rating.target_id == rating.target_id)
    ).first()
    
    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"您已对{rating.target_type}:{rating.target_id}进行过评分"
        )
    
    # 创建新评分
    db_rating = Rating.from_orm(rating)
    db_rating.user_id = current_user.id
    session.add(db_rating)
    session.commit()
    session.refresh(db_rating)
    return db_rating

@router.get("/", response_model=List[RatingRead])
def read_ratings(
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db)
):
    query = select(Rating)
    
    # 筛选条件
    if target_type:
        query = query.where(Rating.target_type == target_type)
    if target_id:
        query = query.where(Rating.target_id == target_id)
    
    ratings = session.exec(query.offset(skip).limit(limit)).all()
    return ratings

@router.get("/{rating_id}", response_model=RatingRead)
def read_rating(
    rating_id: int,
    session: Session = Depends(get_db)
):
    rating = session.get(Rating, rating_id)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评分不存在"
        )
    return rating

@router.put("/{rating_id}", response_model=RatingRead)
def update_rating(
    rating_id: int,
    rating_update: RatingUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_rating = session.get(Rating, rating_id)
    if not db_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评分不存在"
        )
    
    # 检查权限：只有评分创建者或管理员可以更新
    if db_rating.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限更新此评分"
        )
    
    # 如果更新了target_type或target_id，需要检查新的组合是否已存在评分
    if rating_update.target_type or rating_update.target_id:
        new_target_type = rating_update.target_type or db_rating.target_type
        new_target_id = rating_update.target_id or db_rating.target_id
        
        existing_rating = session.exec(
            select(Rating)
            .where(Rating.id != rating_id)
            .where(Rating.user_id == current_user.id)
            .where(Rating.target_type == new_target_type)
            .where(Rating.target_id == new_target_id)
        ).first()
        
        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"您已对{new_target_type}:{new_target_id}进行过评分"
            )
    
    # 更新评分
    rating_data = rating_update.dict(exclude_unset=True)
    for key, value in rating_data.items():
        setattr(db_rating, key, value)
    
    session.add(db_rating)
    session.commit()
    session.refresh(db_rating)
    return db_rating

@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    rating_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rating = session.get(Rating, rating_id)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评分不存在"
        )
    
    # 检查权限：只有评分创建者或管理员可以删除
    if rating.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此评分"
        )
    
    session.delete(rating)
    session.commit()
    return None