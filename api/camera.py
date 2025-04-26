from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from models.camera import Camera
from database.config import get_db
from auth.auth import get_current_admin

router = APIRouter(prefix="/cameras", tags=["相机管理"])

@router.post(
    "/", 
    response_model=Camera,
    summary="创建相机",
    description="添加一个新的相机到数据库",
    response_description="创建成功的相机信息",
    dependencies=[Depends(get_current_admin)]
)
async def create_camera(camera: Camera, db: Session = Depends(get_db)):
    existing_camera = db.exec(
        select(Camera).where(Camera.model == camera.model)
    ).first()
    if existing_camera:
        raise HTTPException(
            status_code=400,
            detail="Camera with this model already exists"
        )
    
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera

@router.get(
    "/",
    response_model=List[Camera],
    summary="获取相机列表",
    description="分页查询所有相机信息",
    response_description="相机列表"
)
async def read_cameras(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = select(Camera).offset(skip).limit(limit)
    if search:
        query = query.where(Camera.model.contains(search))
    cameras = db.exec(query).all()
    return cameras

@router.get(
    "/{camera_id}",
    response_model=Camera,
    summary="获取相机详情",
    description="根据ID查询特定相机信息",
    response_description="相机详细信息"
)
async def read_camera(camera_id: int, db: Session = Depends(get_db)):
    camera = db.exec(
        select(Camera).where(Camera.id == camera_id)
    ).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.put(
    "/{camera_id}",
    response_model=Camera,
    summary="更新相机信息",
    description="根据ID更新相机信息",
    response_description="更新后的相机信息",
    dependencies=[Depends(get_current_admin)]
)
async def update_camera(
    camera_id: int,
    camera_update: Camera,
    db: Session = Depends(get_db)
):
    db_camera = db.get(Camera, camera_id)
    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    if camera_update.model != db_camera.model:
        existing_camera = db.exec(
            select(Camera).where(Camera.model == camera_update.model)
        ).first()
        if existing_camera:
            raise HTTPException(
                status_code=400,
                detail="Camera with this model already exists"
            )
    
    camera_data = camera_update.dict(exclude_unset=True)
    for key, value in camera_data.items():
        setattr(db_camera, key, value)
    
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera

@router.delete(
    "/{camera_id}",
    summary="删除相机",
    description="根据ID删除相机记录",
    response_description="删除操作结果",
    dependencies=[Depends(get_current_admin)]
)
async def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    db.delete(camera)
    db.commit()
    return {"ok": True}