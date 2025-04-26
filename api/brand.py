from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from models.brand import Brand
from database.config import get_db
from auth.auth import get_current_admin

router = APIRouter(prefix="/brands", tags=["品牌管理"])

@router.post(
    "/", 
    response_model=Brand,
    summary="创建品牌",
    description="添加一个新的相机品牌到数据库",
    response_description="创建成功的品牌信息",
    dependencies=[Depends(get_current_admin)]
)
async def create_brand(brand: Brand, db: Session = Depends(get_db)):
    existing_brand = db.exec(
        select(Brand).where(Brand.name == brand.name)
    ).first()
    if existing_brand:
        raise HTTPException(
            status_code=400,
            detail="Brand with this name already exists"
        )
    
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand

@router.get(
    "/",
    response_model=List[Brand],
    summary="获取品牌列表",
    description="分页查询所有相机品牌信息",
    response_description="品牌列表"
)
async def read_brands(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = select(Brand).offset(skip).limit(limit)
    if keyword:
        query = query.where((Brand.name.contains(keyword)) | (Brand.name_zh.contains(keyword)))
    brands = db.exec(query).all()
    return brands

@router.get(
    "/{brand_id}",
    response_model=Brand,
    summary="获取品牌详情",
    description="根据ID查询特定相机品牌信息",
    response_description="品牌详细信息"
)
async def read_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.exec(
        select(Brand).where(Brand.id == brand_id)
    ).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.put(
    "/{brand_id}",
    response_model=Brand,
    summary="更新品牌信息",
    description="根据ID更新相机品牌信息",
    response_description="更新后的品牌信息",
    dependencies=[Depends(get_current_admin)]
)
async def update_brand(
    brand_id: int,
    brand_update: Brand,
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
    
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.delete(
    "/{brand_id}",
    summary="删除品牌",
    description="根据ID删除相机品牌记录",
    response_description="删除操作结果",
    dependencies=[Depends(get_current_admin)]
)
async def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    db.delete(brand)
    db.commit()
    return {"ok": True}