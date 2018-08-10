#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm
from utils import ycache
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[InputRequired(message='请输入密码'), Length(3, 20, message='密码格式错误')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message='请输入密码'), Length(3, 20, message='旧密码格式错误')])
    newpwd = StringField(validators=[InputRequired(message='请输入密码'), Length(3, 20, message='新密码格式错误')])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message='两次新密码不等')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='验证码错误')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # 获取验证码
        captcha_cache = ycache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('验证码错误！')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if email == user.email:
            raise ValidationError('不能修改为相同邮箱！')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图的名称！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图的优先级！')])
    image_url = StringField(validators=[InputRequired(message='请上传轮播图！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])


class EditBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID！')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块的名称！')])

class EditBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID！')])