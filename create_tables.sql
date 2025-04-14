-- 摄影数据库表结构设计

-- 品牌表
CREATE TABLE brand (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '品牌ID，自增主键',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '品牌英文名称，唯一',
    name_zh VARCHAR(100) COMMENT '品牌中文名称',
    country VARCHAR(50) COMMENT '品牌所属国家',
    founded_year INTEGER COMMENT '品牌创立年份',
    website VARCHAR(255) COMMENT '品牌官方网站URL',
    description TEXT COMMENT '品牌详细描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录更新时间'
);

-- 卡口表
CREATE TABLE mount (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '卡口ID，自增主键',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '卡口名称，唯一',
    brand_id INTEGER COMMENT '所属品牌ID',
    FOREIGN KEY (brand_id) REFERENCES brand(id),
    release_year INTEGER COMMENT '卡口发布年份',
    flange_distance DECIMAL(5,2) COMMENT '法兰距(单位:mm)',
    diameter DECIMAL(5,2) COMMENT '卡口直径(单位:mm)',
    description TEXT COMMENT '卡口详细描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录更新时间'
);

-- 用户表
CREATE TABLE `user` (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID，自增主键',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名，唯一',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT '用户邮箱，唯一',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希值',
    role VARCHAR(20) NOT NULL DEFAULT 'user' COMMENT '用户角色(admin/user)',
    full_name VARCHAR(100) COMMENT '用户全名',
    avatar_url VARCHAR(255) COMMENT '用户头像URL',
    bio TEXT COMMENT '用户个人简介',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录更新时间'
);

-- 相机表
CREATE TABLE camera (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '相机ID，自增主键',
    model VARCHAR(100) NOT NULL COMMENT '相机型号英文名称',
    model_zh VARCHAR(100) COMMENT '相机型号中文名称',
    brand_id INTEGER COMMENT '所属品牌ID',
    FOREIGN KEY (brand_id) REFERENCES brand(id),
    mount_id INTEGER COMMENT '卡口ID',
    FOREIGN KEY (mount_id) REFERENCES mount(id),
    release_year INTEGER COMMENT '相机发布年份',
    type VARCHAR(50) COMMENT '相机类型(DSLR/微单/卡片机/胶片机/其他)',
    CONSTRAINT chk_camera_type CHECK (type IN ('DSLR', 'Mirrorless', 'Compact', 'Film', 'Other')),
    sensor_size VARCHAR(50) COMMENT '传感器尺寸',
    megapixels DECIMAL(5,2) COMMENT '有效像素(单位:百万)',
    iso_range VARCHAR(50) COMMENT 'ISO感光度范围',
    shutter_speed VARCHAR(50) COMMENT '快门速度范围',
    weight_grams INTEGER COMMENT '相机重量(单位:克)',
    dimensions VARCHAR(50) COMMENT '相机尺寸(长宽高)',
    description TEXT COMMENT '相机详细描述',
    created_by INTEGER COMMENT '创建者ID，外键关联用户表',
    FOREIGN KEY (created_by) REFERENCES `user`(id) ON DELETE SET NULL ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录更新时间',
    UNIQUE (model, brand_id) COMMENT '相机型号和品牌组合唯一'
);

-- 镜头表
CREATE TABLE lens (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '镜头ID，自增主键',
    model VARCHAR(100) NOT NULL COMMENT '镜头型号英文名称',
    model_zh VARCHAR(100) COMMENT '镜头型号中文名称',
    brand_id INTEGER COMMENT '所属品牌ID',
    FOREIGN KEY (brand_id) REFERENCES brand(id),
    mount_id INTEGER COMMENT '卡口ID',
    FOREIGN KEY (mount_id) REFERENCES mount(id),
    release_year INTEGER COMMENT '镜头发布年份',
    focal_length VARCHAR(50) NOT NULL COMMENT '焦距范围(单位:mm)',
    aperture VARCHAR(50) NOT NULL COMMENT '光圈范围',
    lens_type VARCHAR(50) COMMENT '镜头类型(定焦/变焦/微距/广角/长焦/其他)',
    CONSTRAINT chk_lens_type CHECK (lens_type IN ('Prime', 'Zoom', 'Macro', 'Wide', 'Telephoto', 'Other')),
    filter_size DECIMAL(5,2) COMMENT '滤镜尺寸(单位:mm)',
    weight_grams INTEGER COMMENT '镜头重量(单位:克)',
    dimensions VARCHAR(50) COMMENT '镜头尺寸(长宽高)',
    description TEXT COMMENT '镜头详细描述',
    created_by INTEGER COMMENT '创建者ID，外键关联用户表',
    FOREIGN KEY (created_by) REFERENCES `user`(id) ON DELETE SET NULL ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录更新时间',
    UNIQUE (model, brand_id) COMMENT '镜头型号和品牌组合唯一'
);

-- 创建索引
CREATE INDEX idx_camera_brand ON camera(brand_id) COMMENT '相机表品牌ID索引';
CREATE INDEX idx_camera_mount ON camera(mount_id) COMMENT '相机表卡口ID索引';
CREATE INDEX idx_lens_brand ON lens(brand_id) COMMENT '镜头表品牌ID索引';
CREATE INDEX idx_lens_mount ON lens(mount_id) COMMENT '镜头表卡口ID索引';
CREATE INDEX idx_mount_brand ON mount(brand_id) COMMENT '卡口表品牌ID索引';