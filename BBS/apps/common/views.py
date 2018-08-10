#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from flask import Blueprint, request, make_response, jsonify
from exts import qcloud_sms
from utils import restful, ycache
from .forms import SMSCaptchaForm
from utils.captcha import Captcha
from io import BytesIO
import qiniu
import tasks

bp = Blueprint('common', __name__, url_prefix='/c')


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    # 接口加密
    # 1. telephone
    # 2. timestamp
    # 3. md5(timestamp+telephone+salt)
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        # 发送验证码
        captcha = Captcha.gene_text(number=4)
        # if qcloud_sms.singleSender([telephone], [captcha]):
        #     # 存储短信验证码到memcached中
        #     ycache.set(telephone, captcha)
        #     return restful.success()
        # else:
        #     return restful.params_error('短信验证码发送失败！')
        tasks.send_sms_captcha.delay([telephone], [captcha])
        ycache.set(telephone, captcha)
        return restful.success()
    else:
        return restful.params_error(message="参数错误！")


@bp.route('/captcha/')
def graph_captcha():
    """获取图形验证码"""
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    # 存储验证码， 转换为小写
    ycache.set(text.lower(), text.lower())
    # 字节流
    out = BytesIO()
    image.save(out, 'png')
    # 把文件指针设置到文件开头处，否则下次文件读取的时候无法读取
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = '9stGBqaVysP4-aSGFBIOwpKMkNI7huQDA2XFKFPt'
    secret_key = 'ExOh5sfxm__ZK0t0YGT8ItSYvFamvrhhNb-_7yed'
    q = qiniu.Auth(access_key, secret_key)

    bucket = 'yingjoy'
    token = q.upload_token(bucket)
    return jsonify({'uptoken': token})
