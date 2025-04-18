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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间'
);

-- 在name字段上创建索引
CREATE INDEX idx_brand_name ON brand(name);

-- 在country字段上创建索引
CREATE INDEX idx_brand_country ON brand(country);

-- 在founded_year字段上创建索引
CREATE INDEX idx_brand_founded_year ON brand(founded_year);