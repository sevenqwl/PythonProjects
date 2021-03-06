#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERY_RESULT_BACKEND='redis://localhost:6379/1'
# BROKER_URL='redis://localhost:6379/2'
BROKER_BACKEND = 'mongodb'  # mongodb作为任务队列（或者说是缓存）
<<<<<<< HEAD
BROKER_URL = 'mongodb://10.6.0.149:27017/'  # 队列地址
CELERY_RESULT_BACKEND = 'mongodb://10.6.0.149:27017/'  # 消息结果存储地址
=======
BROKER_URL = 'mongodb://127.0.0.1:27017/for_celery'  # 队列地址
CELERY_RESULT_BACKEND = 'mongodb://127.0.0.1:27017/for_celery'  # 消息结果存储地址
>>>>>>> 8fe8c958956fbce6a95b4d1d541449de074a987b
CELERY_MONGODB_BACKEND_SETTINGS = {  # 消息结果存储配置
    'host': '127.0.0.1',
    'port': 27017,
    'database': 'celery',
    # 'user':'root',
    # 'password':'root1234',
    'taskmeta_collection': 'task_meta',  # 任务结果的存放collection
}
CELERY_ROUTES = {  # 配置任务的先后顺序
    'celery_task.tasks.add': {'queue': 'for_add', 'router_key': 'for_add'},
    'celery_task.tasks.subtract': {'queue': 'for_subtract', 'router_key': 'for_subtract'}
}