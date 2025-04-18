from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from models.lens import Lens
from database.config import get_db
from auth.auth import get_current_admin

router = APIRouter(prefix="/lenses", tags=["镜头管理"])

@router.post(
    "/", 
    response_model=Lens,
    summary="创建镜头",
    description="添加一个新的镜头到数据库",
    response_description="创建成功的镜头信息",
    dependencies=[Depends(get_current_admin)]
)
async def create_lens(lens: Lens, db: Session = Depends(get_db)):
    existing_lens = db.exec(
        select(Lens).where(Lens.model == lens.model)
    ).first()
    if existing_lens:
        raise HTTPException(
            status_code=400,
            detail="Lens with this model already exists"
        )
    
    db.add(lens)
    db.commit()
    db.refresh(lens)
    return lens

@router.get(
    "/",
    response_model=List[Lens],
    summary="获取镜头列表",
    description="分页查询所有镜头信息",
    response_description="镜头列表"
)
async def read_lenses(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db)
):
    lenses = db.exec(
        select(Lens).offset(skip).limit(limit)
    ).all()
    return lenses

@router.get(
    "/{lens_id}",
    response_model=Lens,
    summary="获取镜头详情",
    description="根据ID查询特定镜头信息",
    response_description="镜头详细信息"
)
async def read_lens(lens_id: int, db: Session = Depends(get_db)):
    lens = db.exec(
        select(Lens).where(Lens.id == lens_id)
    ).first()
    if not lens:
        raise HTTPException(status_code=404, detail="Lens not found")
    return lens

@router.put(
    "/{lens_id}",
    response_model=Lens,
    summary="更新镜头信息",
    description="根据ID更新镜头信息",
    response_description="更新后的镜头信息",
    dependencies=[Depends(get_current_admin)]
)
async def update_lens(
    lens_id: int,
    lens_update: Lens,
    db: Session = Depends(get_db)
):
    db_lens = db.get(Lens, lens_id)
    if not db_lens:
        raise HTTPException(status_code=404, detail="Lens not found")
    
    if lens_update.model != db_lens.model:
        existing_lens = db.exec(
            select(Lens).where(Lens.model == lens_update.model)
        ).first()
        if existing_lens:
            raise HTTPException(
                status_code=400,
                detail="Lens with this model already exists"
            )
    
    lens_data = lens_update.dict(exclude_unset=True)
    for key, value in lens_data.items():
        setattr(db_lens, key, value)
    
    db.add(db_lens)
    db.commit()
    db.refresh(db_lens)
    return db_lens

@router.delete(
    "/{lens_id}",
    summary="删除镜头",
    description="根据ID删除镜头记录",
    response_description="删除操作结果",
    dependencies=[Depends(get_current_admin)]
)
async def delete_lens(lens_id: int, db: Session = Depends(get_db)):
    lens = db.get(Lens, lens_id)
    if not lens:
        raise HTTPException(status_code=404, detail="Lens not found")
    
    db.delete(lens)
    db.commit()
    return {"ok": True}