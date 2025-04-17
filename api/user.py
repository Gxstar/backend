from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from models.user import User
from database.config import get_db
from auth.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post(
    "/register",
    response_model=User,
    summary="用户注册",
    description="新用户注册接口",
    response_description="注册成功的用户信息"
)
async def register_user(user: User, db: Session = Depends(get_db)):
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
    
    user.is_admin = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post(
    "/",
    response_model=User,
    summary="创建用户",
    description="管理员创建新用户",
    response_description="创建成功的用户信息",
    dependencies=[Depends(get_current_admin)]
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
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
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.exec(
        select(User).where(User.id == user_id)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
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
    
    user_data = user_update.model_dump(exclude_unset=True)
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
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"ok": True}