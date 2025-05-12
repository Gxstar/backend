from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from models.mount import Mount
from database.config import get_db
from auth.auth import get_current_admin

router = APIRouter(prefix="/mounts", tags=["卡口管理"])

@router.post(
    "/", 
    response_model=Mount,
    summary="创建卡口",
    description="添加一个新的卡口到数据库",
    response_description="创建成功的卡口信息",
    dependencies=[Depends(get_current_admin)]
)
async def create_mount(mount: Mount, brand_ids: List[int] = None, db: Session = Depends(get_db)):
    """
    创建卡口并关联品牌
    :param mount: 卡口基本信息
    :param brand_ids: 关联的品牌ID列表
    :param db: 数据库会话
    :return: 创建成功的卡口信息
    """
    existing_mount = db.exec(
        select(Mount).where(Mount.name == mount.name)
    ).first()
    if existing_mount:
        raise HTTPException(
            status_code=400,
            detail="Mount with this name already exists"
        )
    
    db.add(mount)
    db.commit()
    db.refresh(mount)
    
    # 处理品牌关联
    if brand_ids:
        from models.brand_mount_link import BrandMountLink
        for brand_id in brand_ids:
            # 确保brand_id有效且存在
            brand_exists = db.exec(select(Brand).where(Brand.id == brand_id)).first()
            if not brand_exists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Brand with id {brand_id} not found"
                )
            brand_mount = BrandMountLink(brand_id=brand_id, mount_id=mount.id)
            db.add(brand_mount)
        db.commit()
    
    return mount

@router.get(
    "/",
    response_model=List[Mount],
    summary="获取卡口列表",
    description="分页查询所有卡口信息",
    response_description="卡口列表"
)
async def read_mounts(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db)
):
    # 查询卡口列表并关联品牌中文名称
    mounts = db.exec(
        select(Mount)
        .offset(skip)
        .limit(limit)
    ).all()
    
    # 为每个卡口加载关联的品牌信息
    for mount in mounts:
        db.refresh(mount)
        if mount.brands:
            for brand in mount.brands:
                db.refresh(brand)
    
    return mounts

@router.get(
    "/{mount_id}",
    response_model=Mount,
    summary="获取卡口详情",
    description="根据ID查询特定卡口信息",
    response_description="卡口详细信息"
)
async def read_mount(mount_id: int, db: Session = Depends(get_db)):
    mount = db.exec(
        select(Mount).where(Mount.id == mount_id)
    ).first()
    if not mount:
        raise HTTPException(status_code=404, detail="Mount not found")
    
    # 加载关联的品牌信息
    db.refresh(mount)
    if mount.brands:
        for brand in mount.brands:
            db.refresh(brand)
    
    return mount

@router.put(
    "/{mount_id}",
    response_model=Mount,
    summary="更新卡口信息",
    description="根据ID更新卡口信息",
    response_description="更新后的卡口信息",
    dependencies=[Depends(get_current_admin)]
)
async def update_mount(
    mount_id: int,
    mount_update: Mount,
    db: Session = Depends(get_db)
):
    db_mount = db.get(Mount, mount_id)
    if not db_mount:
        raise HTTPException(status_code=404, detail="Mount not found")
    
    if mount_update.name != db_mount.name:
        existing_mount = db.exec(
            select(Mount).where(Mount.name == mount_update.name)
        ).first()
        if existing_mount:
            raise HTTPException(
                status_code=400,
                detail="Mount with this name already exists"
            )
    
    mount_data = mount_update.dict(exclude_unset=True)
    for key, value in mount_data.items():
        setattr(db_mount, key, value)
    
    db.add(db_mount)
    db.commit()
    db.refresh(db_mount)
    return db_mount

@router.delete(
    "/{mount_id}",
    summary="删除卡口",
    description="根据ID删除卡口记录",
    response_description="删除操作结果",
    dependencies=[Depends(get_current_admin)]
)
async def delete_mount(mount_id: int, db: Session = Depends(get_db)):
    mount = db.get(Mount, mount_id)
    if not mount:
        raise HTTPException(status_code=404, detail="Mount not found")
    
    db.delete(mount)
    db.commit()
    return {"ok": True}