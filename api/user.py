from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from models.user import User
from database.config import get_db

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post(
    "/",
    response_model=User,
    summary="创建用户",
    description="添加一个新用户到数据库",
    response_description="创建成功的用户信息"
)
async def create_user(user: User, db: Session = Depends(get_db)):
    # 检查用户名和邮箱是否已存在
    existing_user = db.exec(
        select(User).where(
            (User.username == user.username) | 
            (User.email == user.email)
        )
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get(
    "/",
    response_model=List[User],
    summary="获取用户列表",
    description="分页查询所有用户信息",
    response_description="用户列表"
)
async def read_users(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db)
):
    users = db.exec(
        select(User).offset(skip).limit(limit)
    ).all()
    return users

@router.get(
    "/{user_id}",
    response_model=User,
    summary="获取用户详情",
    description="根据ID查询特定用户信息",
    response_description="用户详细信息"
)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.exec(
        select(User).where(User.id == user_id)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put(
    "/{user_id}",
    response_model=User,
    summary="更新用户信息",
    description="根据ID更新用户信息",
    response_description="更新后的用户信息"
)
async def update_user(
    user_id: int,
    user_update: User,
    db: Session = Depends(get_db)
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 检查更新后的用户名和邮箱是否与其他用户冲突
    if (user_update.username != db_user.username or 
        user_update.email != db_user.email):
        existing_user = db.exec(
            select(User).where(
                (User.username == user_update.username) | 
                (User.email == user_update.email)
            )
        ).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Username or email already exists"
            )
    
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete(
    "/{user_id}",
    summary="删除用户",
    description="根据ID删除用户记录",
    response_description="删除操作结果"
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"ok": True}