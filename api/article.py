from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime as dt

from database.config import get_db
from models.article import Article, ArticleCreate, ArticleUpdate, ArticleRead
from models.user import User
from auth.auth import get_current_user

# 辅助函数：检查文章所有权
def check_article_ownership(article_id: int, user_id: int, session: Session):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="没有权限操作此文章")
    return article

# 创建文章路由实例
router = APIRouter(tags=["文章"], prefix="/articles")

@router.get(
    '/', 
    response_model=list[ArticleRead], 
    summary='获取文章列表',
    description='获取所有文章的列表，支持分页查询',
    response_description='成功返回文章列表数据'
)
def read_articles(
    session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """获取文章列表，支持分页"""
    articles = session.exec(select(Article).offset(skip).limit(limit)).all()
    return articles

@router.get(
    '/{article_id}', 
    response_model=ArticleRead, 
    summary='获取文章详情',
    description='根据ID获取文章详情',
    response_description='成功返回文章详情数据'
)
def read_article(
    article_id: int,
    session: Session = Depends(get_db)
):
    """获取单篇文章详情"""
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article

@router.post(
    '/', 
    response_model=ArticleRead, 
    status_code=status.HTTP_201_CREATED, 
    summary='创建文章',
    description='创建新文章，需要用户认证',
    response_description='成功创建并返回新文章数据'
)
def create_article(
    article: ArticleCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新文章，需要登录权限"""
    # 将Pydantic模型转换为数据库模型
    db_article = Article.from_orm(article)
    # 设置文章作者为当前登录用户
    db_article.author_id = current_user.id
    # 设置创建时间
    # 时间戳由BaseSQLModel自动管理
    
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article

@router.patch(
    '/{article_id}', 
    response_model=ArticleRead, 
    summary='更新文章',
    description='更新文章，仅文章作者可操作',
    response_description='成功更新并返回文章数据'
)
def update_article(
    article_id: int,
    article: ArticleUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新文章，仅文章作者可操作"""
    db_article = check_article_ownership(article_id, current_user.id, session)
    
    # 更新文章内容
    article_data = article.dict(exclude_unset=True)
    for key, value in article_data.items():
        setattr(db_article, key, value)
    
    # 更新修改时间
    # 时间戳由BaseSQLModel自动管理
    
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article

@router.delete(
    '/{article_id}', 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary='删除文章',
    description='删除文章，仅文章作者可操作',
    response_description='成功删除文章，无返回内容'
)
def delete_article(
    article_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除文章，仅文章作者可操作"""
    article = check_article_ownership(article_id, current_user.id, session)
    
    session.delete(article)
    session.commit()
    return {}