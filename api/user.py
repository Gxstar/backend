from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import timedelta
import os

from models.user import User, UserCreate, UserRead, UserUpdate
from database.config import get_db
from auth.auth import get_current_user, get_current_admin, get_password_hash, login_user

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post(
    "/login",
    summary="用户登录",
    description="用户登录接口，返回访问令牌",
    response_description="访问令牌"
)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    username = user.username
    password = user.password
    access_token = login_user(db, username, password)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    "/register",
    response_model=UserRead,
    summary="用户注册",
    description="新用户注册接口",
    response_description="注册成功的用户信息"
)
async def register_user(user_data: dict, db: Session = Depends(get_db)):
    # 检查用户名和邮箱是否已存在
    existing_user = db.exec(
        select(User).where(
            (User.username == user_data.get("username")) | 
            (User.email == user_data.get("email"))
        )
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="用户名或邮箱已存在"
        )
    
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post(
    "/",
    response_model=User,
    summary="创建用户",
    description="管理员创建新用户",
    response_description="创建成功的用户信息",
    dependencies=[Depends(get_current_admin)]
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
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
    
    user.password_hash = get_password_hash(user.password)
    db_user = User.from_orm(user)
    db.add(db_user)
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
    "/me",
    response_model=User,
    summary="获取当前用户信息",
    description="获取当前登录用户的详细信息",
    response_description="当前用户信息"
)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user

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
        raise HTTPException(status_code=404, detail="用户不存在")
    if not current_user.is_staff and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限")
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
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role != 'admin' and user_id != current_user.id:
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
    # 处理密码哈希
    if 'password' in user_data:
        user_data['password_hash'] = get_password_hash(user_data.pop('password'))
    
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