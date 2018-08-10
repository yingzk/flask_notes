#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


class CMSPermission(object):
    # 255的二进制来表示权限  1111 1111
    # 所有权限
    ALL_PERMISSION = 0b11111111
    # 访问者权限，只可以访问
    VISITOR = 0b00000001
    # 管理帖子权限
    POSTER = 0b00000010
    # 管理评论
    COMMENTER = 0b00000100
    # 管理板块权限
    BOARDER = 0b00001000
    # 管理前台用户权限
    FRONTUSER = 0b00010000
    # 管理后台用户权限
    CMSUSER = 0b00100000
    # 管理后台管理员
    ADMINISTRATOR = 0b01000000


# 角色和用户是多对多关系，所以建立三方表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)

class CMSRole(db.Model):
    """CMS 角色/组"""
    __tablename__ = 'cms_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, nullable=False, default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')




class CMSUser(db.Model):
    """后台用户"""
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    # 将密码设置为保护的，在定义get函数返回
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    @property
    def permissions(self):
        """获取用户所有权限"""
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            # 获取用户所属角色，所有权限
            all_permissions |= permissions
        return all_permissions

    def has_permission(self, permission):
        """判断是否有某个权限"""
        all_permissions = self.permissions
        result = all_permissions & permission == permission
        return result

    @property
    def is_develop(self):
        """判断是否是开发者"""
        return self.has_permission(CMSPermission.ALL_PERMISSION)