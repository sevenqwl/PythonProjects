#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Celery主类
启动文件名必须为celery.py！！！
"""

from __future__ import absolute_import  # 为兼容Python版本
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True  # linux环境下，用于开启root也可以启动celery服务，默认是不允许root启动celery的
app = Celery(
    main='celery_tasks',  # celery启动包名称
    # broker='redis://localhost',
    # backend='redis://localhost',
    include=['celery_tasks.tasks', ]  # celery所有任务
)
app.config_from_object('celery_tasks.config')  # celery使用文件配置

if __name__ == '__main__':
    app.start()





#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import datetime

app = Celery('periodic_tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')


app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    sender.add_periodic_task(
        crontab(hour=17, minute=32, day_of_week="5"),
        test.s('Happy Wednesday!'),
    )


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def test(arg):
    print(datetime.datetime.now())
    print(arg)

