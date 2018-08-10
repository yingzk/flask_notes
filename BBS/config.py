#!usr/bin/env python  
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/07/29 
"""

import os
from datetime import timedelta

# Debug
DEBUG = True
TEMPLATES_AUTO_RELOAD = True

SECRET_KEY = os.urandom(24)

# PERMANENT_SESSION_LIFETIME = timedelta(days=30)

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
                        'root', '123456', 'localhost', '3306', 'bbs')
SQLALCHEMY_TRACK_MODIFICATIONS = False


# SESSION
CMS_USER_ID = 'cms user id'
FRONT_USER_ID = 'front user id'

# Flask Mail
# TLS 587
# SSL 465
# QQ邮箱不支持加密发送邮件
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL = default False
MAIL_USERNAME = "xxxxxxxxxx@qq.com"
MAIL_PASSWORD = "xxxxxxxxxxxxxxxx"
MAIL_DEFAULT_SENDER = "xxxxxxxxxx@qq.com"


# QCloud SMS
QCLOUD_APPID = xxxxxxxxxx
QCLOUD_APPKEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
QCLOUD_SIGN = xxxxxx
QCLOUD_TEMPLATE_ID = xxxxxx

# UEditor
# UEDITOR_UPLOAD_PATH = ""
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
UEDITOR_QINIU_SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
UEDITOR_QINIU_BUCKET_NAME = "yingjoy"
UEDITOR_QINIU_DOMAIN = "http://xxxxxxxxxxxx.xxx.clouddn.com/"


# Flask Paginate
# 一页显示多少
PER_PAGE = 10


# Celery
CELERY_RESULT_BACKEND = "redis://:123456@192.168.1.200:6379/0"
CELERY_BROKER_URL = "redis://:123456@192.168.1.200:6379/0"