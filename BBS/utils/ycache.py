#!usr/bin/env python  
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/08/03 
"""

import memcache

cache = memcache.Client(['192.168.1.200:11211'], debug=True)


def set(key, value, timeout=60):
    return cache.set(key, value, timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)