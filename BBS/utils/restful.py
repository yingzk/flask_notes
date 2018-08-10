#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/08/03 
"""
from flask import jsonify


class HttpCode(object):
    """状态码"""
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500


def restful_result(code, message, data):
    return jsonify({
        "code": code,
        "message": message,
        "data": data or {}
    })

def success(message=None, data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)

def unauth_error(message=''):
    return restful_result(code=HttpCode.unautherror, message=message, data=None)

def params_error(message=''):
    return restful_result(code=HttpCode.paramserror, message=message, data=None)

def server_error(message=''):
    return restful_result(code=HttpCode.servererror, message=message or "服务器内部错误", data=None)