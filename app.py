from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "欢迎使用相机数据管理系统后端服务"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)