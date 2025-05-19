# 相机数据管理系统

## 项目简介
相机数据管理系统是一个基于FastAPI的后端服务，用于管理相机、镜头、品牌等相关数据。系统提供完整的RESTful API接口，支持数据的增删改查操作。

## 主要功能
- 品牌管理：相机品牌的增删改查
- 相机管理：相机型号的增删改查
- 镜头管理：相机镜头的增删改查
- 用户管理：系统用户权限管理
- 卡口管理：相机/镜头卡口兼容性管理

## 技术栈
- 后端框架：FastAPI
- ORM工具：SQLModel
- 数据库：MariaDB
- 数据库迁移：Alembic
- API文档：自动生成OpenAPI文档

## 运行环境
- Python 3.9+
- MariaDB 10.5+

## 安装与运行
1. 克隆项目
```bash
git clone https://github.com/your-repo/camera-data.git
cd camera-data
```

2. 安装依赖
```bash
uv sync
```

3. 配置数据库
- 创建数据库并修改`.env`文件中的数据库连接配置
- 数据库迁移
```bash
# 修改模型后创建迁移
alembic revision --autogenerate -m "迁移描述"
# 执行迁移
alembic upgrade head
```

4. 启动服务
```bash
uvicorn app:app --reload

5. 生产环境启动
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```
```

## API文档
启动服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构
```
backend/
├── api/            # API路由
├── models/         # 数据模型
├── database/       # 数据库配置
├── auth/           # 认证模块
├── alembic/        # 数据库迁移
└── app.py          # 主应用
```

## 贡献指南
1. Fork项目
2. 创建新分支 (`git checkout -b feature/your-feature`)
3. 提交修改 (`git commit -am 'Add some feature'`)
4. 推送分支 (`git push origin feature/your-feature`)
5. 创建Pull Request