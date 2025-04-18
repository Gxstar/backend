from fastapi import FastAPI
from api.brand import router as brand_router
from api.user import router as user_router
from api.camera import router as camera_router
from api.lens import router as lens_router
from api.mount import router as mount_router

app = FastAPI(
    title="相机数据管理系统API",
    description="相机数据管理后端服务，提供信息的增删改查功能"
)

app.include_router(brand_router)
app.include_router(user_router)
app.include_router(camera_router)
app.include_router(lens_router)
app.include_router(mount_router)

@app.get("/")
async def read_root():
    return {"message": "欢迎使用相机数据管理系统后端服务"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)