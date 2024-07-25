CREATE DATABASE IF NOT EXISTS AIcert;
DROP TABLE IF EXISTS `invitation_code`;
CREATE TABLE IF NOT EXISTS `invitation_code` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `code` varchar(64) NOT NULL COMMENT '邀请码',
    `creator_id` varchar(64) NOT NULL COMMENT '创建者ID',
    `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态（1：未使用，2：已使用）',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `expire_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '过期时间',
    PRIMARY KEY (`id`),  UNIQUE KEY `uk_code` (`code`))
    DEFAULT CHARSET=utf8mb4 COMMENT='邀请码表';

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(64) NOT NULL COMMENT '用户名',
    `group` varchar(64) NOT NULL COMMENT '用户分组',
    `mobile` varchar(64) DEFAULT NULL COMMENT '注册手机号',
    `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
    `password` varchar(64) NOT NULL COMMENT '登录密码',
    `invitation_code` varchar(64) NOT NULL COMMENT '邀请码',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),  UNIQUE KEY (`username`), UNIQUE KEY (`mobile`))
    DEFAULT CHARSET=utf8mb4 COMMENT='用户列表';