#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import pymysql
from flask import Flask
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
CORS(app, supports_credentials=True)


def run(args):
    # 加载配置文件
    web_config = {'host': args.host, 'port': args.port, 'debug': args.debug}
    app.config.from_object('web.config.Config')

    # 连接数据库
    app.db = pymysql.connect(host=app.config["MYSQL_DATABASE_HOST"],
                           port=app.config["MYSQL_DATABASE_PORT"],
                           user=app.config["MYSQL_DATABASE_USER"],
                           password=app.config["MYSQL_DATABASE_PASSWORD"],
                           database=app.config["MYSQL_DATABASE_DB"],
                           charset=app.config["MYSQL_DATABASE_CHARSET"])

    # 初始化session会话
    app.secret_key = app.config["SECRET_KEY"]

    # 注册blueprint路由表
    from web.view import auth, dashboard, index
    app.register_blueprint(auth)
    app.register_blueprint(index)
    app.register_blueprint(dashboard)

    app.run(**web_config)