# 相机数据管理系统后端服务

## 项目简介

相机数据管理系统是一个基于FastAPI开发的RESTful API服务，用于管理相机、镜头、品牌和卡口等摄影器材相关数据。系统提供了完整的用户认证和权限管理功能，支持数据的增删改查操作。

## 技术栈

- **Web框架**: [FastAPI](https://fastapi.tiangolo.com/) - 高性能的现代Python Web框架
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) - 结合了SQLAlchemy和Pydantic的ORM库
- **数据库**: [MariaDB](https://mariadb.org/) - 开源的关系型数据库
- **数据库迁移**: [Alembic](https://alembic.sqlalchemy.org/) - SQLAlchemy的数据库迁移工具
- **认证**: JWT (JSON Web Tokens) - 使用[python-jose](https://github.com/mpdavis/python-jose)实现
- **密码加密**: [Passlib](https://passlib.readthedocs.io/) 和 [Bcrypt](https://github.com/pyca/bcrypt/) - 安全的密码哈希处理
- **服务器**: [Uvicorn](https://www.uvicorn.org/) - 高性能的ASGI服务器
- **包管理**: [uv](https://github.com/astral-sh/uv) - 高性能的Python包管理器和安装器

## 项目结构

```
├── alembic/                # 数据库迁移相关文件
│   └── versions/          # 数据库迁移版本文件
├── api/                   # API路由模块
│   ├── brand.py           # 品牌管理API
│   ├── camera.py          # 相机管理API
│   ├── lens.py            # 镜头管理API
│   ├── mount.py           # 卡口管理API
│   └── user.py            # 用户管理API
├── auth/                  # 认证授权模块
│   └── auth.py            # JWT认证和权限控制
├── database/              # 数据库配置
│   └── config.py          # 数据库连接配置
├── models/                # 数据模型
│   ├── base.py            # 基础模型
│   ├── brand.py           # 品牌模型
│   ├── camera.py          # 相机模型
│   ├── lens.py            # 镜头模型
│   ├── mount.py           # 卡口模型
│   ├── user.py            # 用户模型
│   ├── brand_mount_link.py # 品牌-卡口关联表
│   └── lens_mount_link.py  # 镜头-卡口关联表
├── app.py                 # 应用入口
├── alembic.ini            # Alembic配置文件
└── pyproject.toml         # 项目依赖配置
```

## 核心功能

### 1. 用户认证与授权

系统实现了基于JWT的用户认证机制，支持用户注册、登录和权限控制。主要功能包括：

- 用户注册和登录
- 基于JWT的身份验证
- 基于角色的权限控制（用户/管理员）
- 密码加密存储

### 2. 数据模型

系统使用SQLModel定义了多个数据模型，包括用户、品牌、相机、镜头和卡口等，并实现了它们之间的关联关系。主要模型包括：

- **用户模型**：包含用户基本信息、认证信息和权限角色
- **品牌模型**：相机和镜头品牌信息
- **相机模型**：相机详细规格和参数
- **镜头模型**：镜头详细规格和参数
- **卡口模型**：相机卡口规格信息

### 3. 多对多关系

系统实现了品牌与卡口、镜头与卡口之间的多对多关系，通过关联表实现：

- **品牌-卡口关联**：一个品牌可以支持多种卡口，一种卡口可以被多个品牌使用
- **镜头-卡口关联**：一个镜头可以适配多种卡口，一种卡口可以适配多种镜头

### 4. API路由

系统提供了完整的RESTful API，包括用户、品牌、相机、镜头和卡口等资源的CRUD操作：

- **用户管理**：注册、登录、查询、更新和删除用户
- **品牌管理**：创建、查询、更新和删除品牌
- **相机管理**：创建、查询、更新和删除相机
- **镜头管理**：创建、查询、更新和删除镜头
- **卡口管理**：创建、查询、更新和删除卡口

## 环境配置

项目使用`.env`文件管理环境变量，主要包括：

- `SQLALCHEMY_DATABASE_URI`: 数据库连接URI
- `AUTH_SECRET_KEY`: JWT认证密钥
- `AUTH_ALGORITHM`: JWT算法（默认HS256）
- `AUTH_TOKEN_EXPIRE_MINUTES`: 令牌过期时间（分钟）

## 数据库迁移

项目使用Alembic进行数据库迁移管理，迁移文件位于`alembic/versions/`目录下。

## 运行项目

1. 安装依赖：

```bash
# 使用uv安装项目依赖
uv sync
```

2. 设置环境变量（创建`.env`文件）：

```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost/camera_data
AUTH_SECRET_KEY=your_secret_key
AUTH_ALGORITHM=HS256
AUTH_TOKEN_EXPIRE_MINUTES=30
```

3. 运行数据库迁移：

```bash
alembic upgrade head
```

4. 启动服务：

```bash
python app.py
```

或者使用uvicorn：

```bash
uvicorn app:app --reload
```

服务将在 http://localhost:8000 上运行，API文档可在 http://localhost:8000/docs 访问。