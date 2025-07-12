from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.config import get_db
from models.tag import Tag, TagCreate, TagRead, TagUpdate

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, session: Session = Depends(get_db)):
    """创建新标签"""
    # 检查名称和slug是否已存在
    existing_name = session.exec(select(Tag).where(Tag.name == tag.name)).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"标签名称 '{tag.name}' 已存在"
        )
    
    existing_slug = session.exec(select(Tag).where(Tag.slug == tag.slug)).first()
    if existing_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"标签slug '{tag.slug}' 已存在"
        )
    
    db_tag = Tag.from_orm(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.get("/", response_model=list[TagRead])
def read_tags(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db)
):
    """获取标签列表"""
    tags = session.exec(select(Tag).offset(skip).limit(limit)).all()
    return tags

@router.get("/{tag_id}", response_model=TagRead)
def read_tag(tag_id: int, session: Session = Depends(get_db)):
    """通过ID获取标签"""
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag

@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    tag: TagUpdate,
    session: Session = Depends(get_db)
):
    """更新标签信息"""
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    # 如果更新名称或slug，检查是否已存在
    if tag.name and tag.name != db_tag.name:
        existing_name = session.exec(select(Tag).where(Tag.name == tag.name)).first()
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"标签名称 '{tag.name}' 已存在"
            )
    
    if tag.slug and tag.slug != db_tag.slug:
        existing_slug = session.exec(select(Tag).where(Tag.slug == tag.slug)).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"标签slug '{tag.slug}' 已存在"
            )
    
    tag_data = tag.dict(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(db_tag, key, value)
    
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, session: Session = Depends(get_db)):
    """删除标签"""
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    # 检查标签是否关联文章
    if tag.articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"标签 '{tag.name}' 已关联文章，无法删除"
        )
    
    session.delete(tag)
    session.commit()
    return None