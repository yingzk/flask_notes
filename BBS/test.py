#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/08/04 
"""

# from utils.captcha import Captcha
# Captcha.gene_graph_captcha()

# from utils.qcloud_sms import QCloudSMSAPI
#
# QCloudSMSAPI().singleSender(['18582326523'], ['1234'])

from tasks import send_sms_captcha

send_sms_captcha.delay(['18582326523'], ['1234'])