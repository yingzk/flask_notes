#!usr/bin/env python  
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.qcloud_sms import QCloudSMSAPI

db = SQLAlchemy()
mail = Mail()
qcloud_sms = QCloudSMSAPI()