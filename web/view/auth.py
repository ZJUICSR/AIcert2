#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import json, time, datetime, io
from flask import Blueprint, render_template, request, session, redirect, url_for
from web.model import User, InvitationCode
from web import app
from web.utils import helper

auth = Blueprint("auth", __name__, template_folder="../templates", static_folder="../static")
user_db = User(app.db)
invitation_db = InvitationCode(app.db)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    用户登录页面
    :return:
    """
    # 针对已登录用户，跳转到用户界面
    if session.get("login", None):
        url = request.args.get("next", url_for("home.index"))
        return redirect(url)

    # 针对未登录用户，执行登录操作
    if request.method == "GET":
        # 登录web页面
        return render_template("auth/login.html")
    else:
        # step1：检查验证码
        if request.form.get("captcha", "abc").upper() != session.get("captcha", "").upper():
            return json.dumps({"status": 0, "info": "invalid captcha 验证码错误！"})

        # step2：用户登录
        user = request.form.get("user")
        kwargs = {"password": helper.md5(request.form.get("password"))}
        flag1 = helper.is_email(user)
        flag2 = helper.is_phone(user)
        if flag1:
            kwargs["email"] = user
        if flag2:
            kwargs["phone"] = user
        if not flag1 and not flag2:
            kwargs["username"] = user
        data = user_db.find(**kwargs)

        # step3：登录成功，缓存用户信息
        if data is not None:
            session["login"] = True
            session["email"] = data["email"]
            session["group"] = data["group"]
            session["username"] = data["username"]
            session["admin"] = True if data["group"] == "admin" else False
            session.permanent = True
            return json.dumps(request.form)
        # 登录失败
        return json.dumps({"status": 0, "info": "用户名或密码错误！"})


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    用户注册页面，需要注册码
    :return:
    """
    # 针对已登录用户，跳转到用户界面
    if session.get("login", None):
        url = request.args.get("next", url_for("home.index"))
        return redirect(url)

    if request.method == "GET":
        # 注册web页面
        return render_template("auth/register.html")
    else:
        # step1：检查验证码
        if request.form.get("captcha", "abc").upper() != session.get("captcha", "").upper():
            return json.dumps({"status": 0, "info": "invalid captcha 验证码错误！"})

        # step2: 检查邀请码
        code = request.form.get("invitation_code")
        row = invitation_db.find(code=code)
        if row is None:
            return json.dumps({"status": 0, "info": "invalid invitation code 邀请码不存在！"})
        exp_time = datetime.datetime.timestamp(row["expire_time"])
        if (row["status"] != 1) or (exp_time < time.time()):
            return json.dumps({"status": 0, "info": "invitation code expired 邀请码过期！"})

        # step3：检查用户名是否重复
        username = request.form.get("username")
        row = user_db.find(**{"username": username})
        if row is not None:
            return json.dumps({"status": 0, "info": "username exists!"})

        # step4：检查邮箱是否重复
        email = request.form.get("email")
        if not helper.is_email(email):
            return json.dumps({"status": 0, "info": "invalid email address!"})
        row = user_db.find(**{"email": email})
        if row is not None:
            return json.dumps({"status": 0, "info": "email address exists!"})

        # step5：检查密码是否符合规则，大小写+数字+长度大于6
        password = request.form.get("password")
        result = helper.check_password(password)
        if result["length_error"]:
            return json.dumps({"status": 0, "info": "密码长度必须大于8位！"})
        if result["digit_error"] or result["uppercase_error"] or result["lowercase_error"]:
            return json.dumps({"status": 0, "info": "密码必须包含数字、大小写字母!"})

        # step6：写到用户表，将邀请表状态更新
        password = helper.md5(request.form.get("password"))
        user_db.insert_user(username, email, password, invitation_code=code)

        # 查找用户，顺便检测是否成功
        kwargs = {"password": password, "username": username, "email": email}
        user = user_db.find(**kwargs)
        if user is None:
            json.dumps({"status": 0, "info": "insert db error!"})

        # step7：添加session字段
        session["login"] = True
        session["email"] = user["email"]
        session["group"] = user["group"]
        session["username"] = user["username"]
        session["admin"] = True if user["group"] == "admin" else False
        session.permanent = True
        return json.dumps({"status": 1, "info": "ok"})


@auth.route("/logout", methods=["GET"])
def logout():
    """
    退出登录
    :return:
    """
    session.clear()
    return redirect(url_for("user.login"))


@auth.route("/captcha")
def captcha():
    """
    生成验证码并写入session
    :return:
    """
    # 生成验证码图片
    image, captcha_text = helper.generate_captcha_image()
    # 将验证码文本写入session
    session["captcha"] = captcha_text
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue(), 200, {
        "Content-Type": "image/png",
        "Content-Length": str(len(buf.getvalue()))
    }


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    """
    用户重设密码
    :return:
    """
    if request.method == "GET":
        # 登录web页面
        return render_template("auth/reset_password.html")
    else:
        # 登录api页面
        return json.dumps({"data": ""})