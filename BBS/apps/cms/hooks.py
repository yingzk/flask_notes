#!usr/bin/env python  
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/07/30 
"""

from .views import bp
from config import CMS_USER_ID
from flask import session, g
from .models import CMSUser, CMSPermission


@bp.before_request
def before_request():
    if CMS_USER_ID in session:
        user_id = session.get(CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor
def cms_context_processor():
    return {"CMSPermission":CMSPermission}