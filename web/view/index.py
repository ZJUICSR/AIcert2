#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import json
from flask import Blueprint, render_template, request, session, redirect, url_for
from web.model.user import User
from web import app

index = Blueprint("index", __name__, template_folder="../templates", static_folder="../static")
user_db = User(app.db)


@index.route("/index", methods=["GET"])
def index():
    pass