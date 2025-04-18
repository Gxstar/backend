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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间'
);
CREATE INDEX idx_user_username ON `user`(username);
CREATE INDEX idx_user_email ON `user`(email);