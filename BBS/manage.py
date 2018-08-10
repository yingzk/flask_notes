#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""
import random

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel, BoardModel, PostModel

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser = front_models.FrontUser

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


# 添加CMS用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('CMS 用户添加成功！')


# 创建角色
@manager.command
def create_role():
    # 1. 访问者
    visitor = CMSRole(name='访问者', desc='只能访问，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    # 2. 运营人员
    operator = CMSRole(name='运营', desc='可以修改个人信息，可管理帖子、评论、前台用户')
    # 多个权限取或
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | \
                           CMSPermission.FRONTUSER | CMSPermission.COMMENTER | \
                           CMSPermission.BOARDER
    # 3. 管理员
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.ALL_PERMISSION - CMSPermission.ADMINISTRATOR - 0b10000000

    # 4. 开发者
    developer = CMSRole(name='开发者', desc='超级管理员')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()
    print('角色添加成功！')


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('添加用户到角色中成功！')
        else:
            print('没有这个角色： %s ！' % name)
    else:
        print('没有这个用户： %s ！' % email)


@manager.command
def test_permission():
    """测试权限"""
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('有访问者权限！')
    else:
        print('没有访问者权限！')


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_fuser(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('前台用户添加成功')


@manager.command
def create_test_posts():
    for _ in range(0, 200):
        title = '标题%s' % _
        board = random.choice(BoardModel.query.all())
        content = '内容为：%s 板块为：%s' % (_ , board.name)
        author = FrontUser.query.first()
        post = PostModel(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('插入帖子测试成功！')


if __name__ == '__main__':
    manager.run()
