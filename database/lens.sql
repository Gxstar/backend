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