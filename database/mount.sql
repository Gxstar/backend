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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间'
);
CREATE INDEX idx_mount_brand_id ON mount(brand_id);