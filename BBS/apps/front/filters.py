#!usr/bin/env python  
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/08/09 
"""

from apps.front import bp
from datetime import datetime

def handle_time(time):
    if isinstance(time, datetime):
        now = datetime.now()
        # 获取两个时间之间相差的秒数
        timestamps = (now - time).total_seconds()
        if timestamps < 60:
            return "刚刚"
        elif timestamps >= 60 and timestamps < 60 * 60:
            minutes = timestamps / 60
            return "%s分钟前" % int(minutes)
        elif timestamps >= 60 * 60 and timestamps < 60 * 60 * 24:
            hours = timestamps / (60 * 60)
            return '%s小时前' % int(hours)
        elif timestamps >= 60 * 60 * 24 and timestamps < 60 * 60 * 24 * 30:
            days = timestamps / (60 * 60 * 24)
            return "%s天以前" % days
        else:
            # return "%s年%s月%s日" % (time.year, time.month, time.day)
            return time.strftime("%Y-%m-%d %H:%M")
    else:
        return time

bp.add_app_template_filter(handle_time, 'handle_time')