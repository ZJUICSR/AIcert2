#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import os, re, hashlib, random, string
from functools import wraps
from flask import request, redirect, url_for, session
from PIL import Image, ImageDraw, ImageFont
work_dir = os.path.dirname(os.path.dirname(__file__))


def is_email(email):
    """
    检测是否为邮箱地址
    :param email:
    :return:
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(pattern, email)):
        return True
    else:
        return False


def is_phone(phone):
    """
    检测是否为手机号码
    :param phone:
    :return:
    """
    if len(phone) == 11 and re.match('^(13|14|15|16|18)[0-9]{9}$', phone):
        return True
    else:
        return False


def check_password(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error)

    result = {
        'ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
    return result


def md5(key):
    """
    将key值进行MD5加密
    :param key:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(key.encode('utf-8'))
    key = md5.hexdigest()
    return key


def login_required(f):
    """
    需要用户登录的装饰器
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("login") is None:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    需要管理员登录的装饰器
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin") is None:
            return redirect(url_for('home.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def generate_captcha_image(k=5):
    # 定义图片大小及背景颜色
    image = Image.new('RGB', (135, 45), color=(73, 109, 137))

    # 使用系统自带字体，或指定字体文件路径
    font_path = os.path.join(work_dir, "static/fonts/arial.ttf")
    fnt = ImageFont.truetype(font_path, 30)
    d = ImageDraw.Draw(image)

    # 生成5位数的验证码文本
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    d.text((15, 10), captcha_text, font=fnt, fill=(255, 255, 0))

    # 添加干扰线条和噪点
    for _ in range(random.randint(3, 5)):
        start = (random.randint(0, image.width), random.randint(0, image.height))
        end = (random.randint(0, image.width), random.randint(0, image.height))
        d.line([start, end], fill=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))

    for _ in range(100):
        xy = (random.randrange(0, image.width), random.randrange(0, image.height))
        d.point(xy, fill=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))

    return image, captcha_text


