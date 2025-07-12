from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.config import get_db
from models.category import Category, CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, session: Session = Depends(get_db)):
    """创建新分类"""
    # 检查slug是否已存在
    existing_category = session.exec(select(Category).where(Category.slug == category.slug)).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"分类slug '{category.slug}' 已存在"
        )
    db_category = Category.from_orm(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.get("/", response_model=list[CategoryRead])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db)
):
    """获取分类列表"""
    categories = session.exec(select(Category).offset(skip).limit(limit)).all()
    return categories

@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, session: Session = Depends(get_db)):
    """通过ID获取分类"""
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Session = Depends(get_db)
):
    """更新分类信息"""
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 如果更新slug，检查新slug是否已存在
    if category.slug and category.slug != db_category.slug:
        existing_category = session.exec(select(Category).where(Category.slug == category.slug)).first()
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"分类slug '{category.slug}' 已存在"
            )
    
    category_data = category.dict(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, session: Session = Depends(get_db)):
    """删除分类"""
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    session.delete(category)
    session.commit()
    return None