#!usr/bin/env python  
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/08/10 
"""

from celery import Celery
# 任务 队列 工人 存储
# task 中间人（broker） worker backend
# celery -A tasks.celery worker --pool=eventlet --loglevel=info

from flask_mail import Message
from exts import mail
from flask import Flask
import config
from exts import qcloud_sms

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)

@celery.task
def send_sms_captcha(phone_numbers, params):
    qcloud_sms.singleSender(phone_numbers=phone_numbers, params=params)