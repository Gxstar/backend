from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from models.brand import Brand, BrandCreate, BrandUpdate, BrandRead
from models.brand_mount_link import BrandMountLink
from models.mount import Mount
from database.config import get_db
from auth.auth import get_current_admin

router = APIRouter(prefix="/brands", tags=["品牌管理"])

@router.post(
    "/", 
    response_model=BrandRead,
    summary="创建品牌",
    description="添加一个新的相机品牌到数据库，并可关联多个卡口",
    response_description="创建成功的品牌信息",
    dependencies=[Depends(get_current_admin)]
)
async def create_brand(
    brand: BrandCreate,
    mount_ids: Optional[List[int]] = Query(None, description="关联的卡口ID列表"),
    db: Session = Depends(get_db)
):
    existing_brand = db.exec(
        select(Brand).where(Brand.name == brand.name)
    ).first()
    if existing_brand:
        raise HTTPException(
            status_code=400,
            detail="Brand with this name already exists"
        )
    
    db_brand = Brand.from_orm(brand)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    
    # 处理品牌与卡口的关联
    if mount_ids:
        for mount_id in mount_ids:
            mount = db.get(Mount, mount_id)
            if not mount:
                raise HTTPException(
                    status_code=400,
                    detail=f"卡口ID {mount_id} 不存在"
                )
            brand_mount = BrandMountLink(brand_id=brand.id, mount_id=mount_id)
            db.add(brand_mount)
        db.commit()
        db.refresh(brand)
    
    return brand

@router.get(
    "/",
    response_model=List[BrandRead],
    summary="获取品牌列表",
    description="分页查询所有相机品牌信息，包含关联的卡口信息",
    response_description="品牌列表"
)
async def read_brands(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = select(Brand).offset(skip).limit(limit).options(selectinload(Brand.mounts))
    if keyword:
        query = query.where((Brand.name.contains(keyword)) | (Brand.name_zh.contains(keyword)))
    brands = db.exec(query).all()
    return brands

@router.get(
    "/{brand_id}",
    response_model=BrandRead,
    summary="获取品牌详情",
    description="根据ID查询特定相机品牌信息，包含关联的卡口信息",
    response_description="品牌详细信息"
)
async def read_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.exec(
        select(Brand)
        .where(Brand.id == brand_id)
        .options(selectinload(Brand.mounts))  # 预加载关联的卡口信息
    ).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.put(
    "/{brand_id}",
    response_model=BrandRead,
    summary="更新品牌信息",
    description="根据ID更新相机品牌信息，并可更新关联的卡口",
    response_description="更新后的品牌信息",
    dependencies=[Depends(get_current_admin)]
)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdate,
    mount_ids: Optional[List[int]] = Query(None, description="关联的卡口ID列表，为null则不修改关联，为空列表则清除所有关联"),
    db: Session = Depends(get_db)
):
    db_brand = db.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    if brand_update.name != db_brand.name:
        existing_brand = db.exec(
            select(Brand).where(Brand.name == brand_update.name)
        ).first()
        if existing_brand:
            raise HTTPException(
                status_code=400,
                detail="Brand with this name already exists"
            )
    
    brand_data = brand_update.dict(exclude_unset=True)
    for key, value in brand_data.items():
        setattr(db_brand, key, value)
    
    # 处理品牌与卡口的关联更新
    if mount_ids is not None:
        # 删除现有关联
        db.exec(select(BrandMountLink).where(BrandMountLink.brand_id == brand_id)).delete()
        
        # 添加新关联
        if mount_ids:
            for mount_id in mount_ids:
                mount = db.get(Mount, mount_id)
                if not mount:
                    raise HTTPException(
                        status_code=400,
                        detail=f"卡口ID {mount_id} 不存在"
                    )
                brand_mount = BrandMountLink(brand_id=brand_id, mount_id=mount_id)
                db.add(brand_mount)
    
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.delete(
    "/{brand_id}",
    summary="删除品牌",
    description="根据ID删除相机品牌记录，并级联删除关联的卡口关系",
    response_description="删除操作结果",
    dependencies=[Depends(get_current_admin)]
)
async def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # 先删除关联的卡口关系
    db.exec(select(BrandMountLink).where(BrandMountLink.brand_id == brand_id)).delete()
    
    db.delete(brand)
    db.commit()
    return {"ok": True}