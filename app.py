from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.brand import router as brand_router
from api.user import router as user_router
from api.camera import router as camera_router
from api.lens import router as lens_router
from api.mount import router as mount_router
from api.article import router as article_router
from api.comment import router as comment_router
from alembic.config import Config
from alembic import command

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 应用启动时执行数据库迁移
#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")
#     yield
    # 应用关闭时可以添加清理逻辑

app = FastAPI(
    title="相机数据管理系统API",
    description="相机数据管理后端服务，提供信息的增删改查功能",
    version="1.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brand_router)
app.include_router(user_router)
app.include_router(camera_router)
app.include_router(lens_router)
app.include_router(mount_router)
app.include_router(article_router)
app.include_router(comment_router)



@app.get("/")
async def read_root():
    return {"message": "欢迎使用相机数据管理系统后端服务"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)