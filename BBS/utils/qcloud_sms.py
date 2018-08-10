#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/08/05 
"""

# 腾讯云短信验证码sdk
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from config import QCLOUD_APPID, QCLOUD_APPKEY, QCLOUD_SIGN, QCLOUD_TEMPLATE_ID

class QCloudSMSAPI(object):
    def __init__(self):
        self.appid = QCLOUD_APPID
        self.appkey = QCLOUD_APPKEY
        self.sign = QCLOUD_SIGN
        self.template_id = QCLOUD_TEMPLATE_ID

    def singleSender(self, phone_numbers, params):
        """发送短信，需要传入手机号和模板参数"""
        ssender = SmsSingleSender(self.appid, self.appkey)
        try:
            result = ssender.send_with_param(
                86,
                phone_numbers[0],
                self.template_id, params
            )
        except Exception:
            print('发送验证码失败')
            return False

        if result.get('result') == 0:
            return True
        else:
            return False

