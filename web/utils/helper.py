#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import re, hashlib
from functools import wraps
from flask import g, request, redirect, url_for, session

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





