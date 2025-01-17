#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import os

''' SERVER SETTINGS '''
class Config(object):
    ''' GENERATE SECRET KEY '''
    if not os.environ.get('SECRET_KEY'):
        # Attempt to read the secret from the secret file
        # This will fail if the secret has not been written
        try:
            with open('.aicert.key', 'rb') as secret:
                key = secret.read()
        except (OSError, IOError):
            key = None

        if not key:
            key = os.urandom(64)
            # Attempt to write the secret file
            # This will fail if the filesystem is read-only
            try:
                with open('.aicert.key', 'wb') as secret:
                    secret.write(key)
                    secret.flush()
            except (OSError, IOError):
                print("Write file error for read-only system!")
                exit(1)
    SECRET_KEY = key

    ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = "{:s}/static".format(os.path.dirname(os.path.abspath(__file__)))

    # MYSQL config
    MYSQL_DATABASE_HOST = "0.0.0.0"
    MYSQL_DATABASE_PORT = 13306
    MYSQL_DATABASE_USER = "root"
    MYSQL_DATABASE_PASSWORD = ""
    MYSQL_DATABASE_DB = "AIcert"
    MYSQL_DATABASE_CHARSET = "utf8"
    MYSQL_URL = "mysql://{:s}:{:d}".format(MYSQL_DATABASE_HOST, MYSQL_DATABASE_PORT)

    '''
    SQLALCHEMY_TRACK_MODIFICATIONS is automatically disabled to suppress warnings and save memory. You should only enable
    this if you need it.
    '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''
    SESSION_TYPE is a configuration value used for Flask-Session. It is currently unused in SecNews.
    http://pythonhosted.org/Flask-Session/#configuration
    '''
    SESSION_TYPE = "filesystem"

    '''
    SESSION_FILE_DIR is a configuration value used for Flask-Session. It is currently unused in SecNews.
    http://pythonhosted.org/Flask-Session/#configuration
    '''
    SESSION_FILE_DIR = "/tmp/flask_session"

    '''
    SESSION_COOKIE_HTTPONLY controls if cookies should be set with the HttpOnly flag.
    '''
    SESSION_COOKIE_HTTPONLY = True

    '''
    PERMANENT_SESSION_LIFETIME is the lifetime of a session.
    '''
    PERMANENT_SESSION_LIFETIME = 604800  # 7 days in seconds

    '''
    HOST specifies the hostname where the SecNews instance will exist. It is currently unused.
    '''
    HOST = "icsr.zju.edu.cn"

    '''
    MAILFROM_ADDR is the email address that emails are sent from if not overridden in the configuration panel.
    '''
    MAILFROM_ADDR = "noreply@zju.edu.cn"

    '''
    LOG_FOLDER is the location where logs are written
    These are the logs for SecNews key submissions, registrations, and logins
    The default location is the SecNews/logs folder
    '''
    LOG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs') or os.environ.get('LOG_FOLDER')

    '''
    UPLOAD_FOLDER is the location where files are uploaded.
    The default destination is the SecNews/uploads folder.
    '''
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                    'uploads')

    '''
    TEMPLATES_AUTO_RELOAD specifies whether Flask should check for modifications to templates and
    reload them automatically
    '''
    TEMPLATES_AUTO_RELOAD = True

    '''
    TRUSTED_PROXIES defines a set of regular expressions used for finding a user's IP address if the SecNews instance
    is behind a proxy. 

    SecNews only uses IP addresses for cursory tracking purposes. It is ill-advised to do anything complicated based
    solely on IP addresses.
    '''
    TRUSTED_PROXIES = [
        '^127\.0\.0\.1$',
        # Remove the following proxies if you do not trust the local network
        '^::1$',
        '^fc00:',
        '^10\.',
        '^172\.(1[6-9]|2[0-9]|3[0-1])\.',
        '^192\.168\.'
    ]

    '''
    CACHE_TYPE specifies how SecNews should cache configuration values. If CACHE_TYPE is set to 'redis', SecNews will make use
    of the REDIS_URL specified in environment variables. You can also choose to hardcode the REDIS_URL here.

    It is important that you specify some sort of cache as SecNews uses it to store values received from the database.

    CACHE_REDIS_URL is the URL to connect to Redis server.
    Example: redis://user:password@localhost:6379

    http://pythonhosted.org/Flask-Caching/#configuring-flask-caching
    '''


    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    if CACHE_REDIS_URL:
        CACHE_TYPE = 'redis'
    else:
        CACHE_TYPE = 'simple'

    '''
    UPDATE_CHECK specifies whether or not SecNews will check whether or not there is a new version of SecNews
    '''
    UPDATE_CHECK = True
    SPIDER_FLOAD = os.path.join(STATIC_FOLDER, "website")


class TestingConfig(Config):
    SECRET_KEY = 'AAAAAAAAAAAAAAAAAAAA'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL') or 'sqlite://'
    SERVER_NAME = 'localhost'
    UPDATE_CHECK = False
    CACHE_REDIS_URL = None
    CACHE_TYPE = 'simple'