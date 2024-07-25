#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

"""
INFO: Dashboard 仅允许登录用户访问
"""


import json
from flask import Blueprint, render_template, request, session, redirect, url_for
from web.model.user import User
from web import app
from web.utils import helper

dashboard = Blueprint("dashboard", __name__, template_folder="../templates", static_folder="../static")
user_db = User(app.db)


@dashboard.route("/dashboard/index", methods=["GET"])
@helper.login_required
def index():
    return render_template("dashboard/index.html")