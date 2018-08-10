#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from apps.forms import BaseForm
from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import Regexp, EqualTo, InputRequired
from utils import ycache


# 注册表单验证
class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'^1[34578]\d{9}', message='手机号码格式错误!')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='短信验证码格式错误！')])
    username = StringField(validators=[Regexp(r'.{2,20}', message='用户名格式错误！')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{3,20}', message='密码格式错误！')])
    password2 = StringField(validators=[EqualTo("password1", message='两次密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='图形验证码格式错误！')])

    def validate_cms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = ycache.get(telephone)
        if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误！')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data

        graph_captcha_mem = ycache.get(graph_captcha.lower())
        if not graph_captcha_mem:
            raise ValidationError(message='图形验证码错误！')


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'^1[34578]\d{9}', message='手机号码格式错误!')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{3,20}', message='密码格式错误！')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入选择板块！')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])
    