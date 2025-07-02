from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from database.config import get_db
from models.comment import Comment, CommentCreate, CommentUpdate, CommentRead
from models.article import Article
from models.user import User
from auth.auth import get_current_user

# 创建评论路由实例，路径包含文章ID以关联评论所属文章
router = APIRouter(tags=["评论"], prefix="/articles/{article_id}/comments")

@router.get(
    '/', 
    response_model=list[CommentRead], 
    summary='获取评论列表',
    description='获取所有评论，支持按文章ID筛选',
    response_description='成功返回评论列表数据'
)
def read_comments(
    article_id: int = Path(..., description="文章ID"),
    session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """获取指定文章的评论列表，支持分页"""
    # 验证文章是否存在
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 查询该文章的所有评论
    comments = session.exec(
        select(Comment)
        .where(Comment.article_id == article_id)
        .offset(skip)
        .limit(limit)
    ).all()
    return comments

@router.get(
    '/{comment_id}', 
    response_model=CommentRead, 
    summary='获取评论详情',
    description='根据ID获取评论详情',
    response_description='成功返回评论详情数据'
)
def read_comment(
    article_id: int = Path(..., description="文章ID"),
    comment_id: int = Path(..., description="评论ID"),
    session: Session = Depends(get_db)
):
    """获取指定文章的特定评论"""
    # 验证文章是否存在
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 验证评论是否存在且属于该文章
    comment = session.get(Comment, comment_id)
    if not comment or comment.article_id != article_id:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    return comment

@router.post(
    '/', 
    response_model=CommentRead, 
    status_code=status.HTTP_201_CREATED, 
    summary='创建评论',
    description='创建新评论，需要用户认证',
    response_description='成功创建并返回新评论数据'
)
def create_comment(
    *, 
    article_id: int = Path(..., description="文章ID"),
    comment: CommentCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """为指定文章创建新评论，需要登录权限"""
    # 验证文章是否存在
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 创建评论对象并关联文章和作者
    db_comment = Comment.from_orm(comment)
    db_comment.article_id = article_id
    db_comment.author_id = current_user.id
    db_comment.created_at = datetime.utcnow()
    db_comment.updated_at = datetime.utcnow()
    
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment

@router.patch(
    '/{comment_id}', 
    response_model=CommentRead, 
    summary='更新评论',
    description='部分更新评论内容，仅评论作者可操作，支持修改评论正文',
    response_description='成功更新并返回评论数据'
)
def update_comment(
    *, 
    article_id: int = Path(..., description="文章ID"),
    comment_id: int = Path(..., description="评论ID"),
    comment: CommentUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新评论，仅评论作者可操作"""
    # 验证文章是否存在
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 验证评论是否存在且属于该文章
    db_comment = session.get(Comment, comment_id)
    if not db_comment or db_comment.article_id != article_id:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    # 检查权限：只有评论作者可以更新
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此评论")
    
    # 更新评论内容
    comment_data = comment.dict(exclude_unset=True)
    for key, value in comment_data.items():
        setattr(db_comment, key, value)
    
    # 更新修改时间
    db_comment.updated_at = datetime.utcnow()
    
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment

@router.delete(
    '/{comment_id}', 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary='删除评论',
    description='删除评论，仅评论作者可操作',
    response_description='成功删除评论，无返回内容'
)
def delete_comment(
    article_id: int = Path(..., description="文章ID"),
    comment_id: int = Path(..., description="评论ID"),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除评论，仅评论作者可操作"""
    # 验证文章是否存在
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 验证评论是否存在且属于该文章
    comment = session.get(Comment, comment_id)
    if not comment or comment.article_id != article_id:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    # 检查权限：只有评论作者可以删除
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除此评论")
    
    session.delete(comment)
    session.commit()
    return {}