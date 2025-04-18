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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    UNIQUE (model, brand_id) COMMENT '相机型号和品牌组合唯一'
);
CREATE INDEX idx_camera_brand_id ON camera(brand_id);
CREATE INDEX idx_camera_mount_id ON camera(mount_id);
CREATE INDEX idx_camera_created_by ON camera(created_by);