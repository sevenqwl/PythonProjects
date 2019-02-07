#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"


from __future__ import absolute_import

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'

# redis
BROKER_URL='redis://10.6.0.118:6379/0'
CELERY_RESULT_BACKEND='redis://10.6.0.118:6379/0'


# mongodb
# BROKER_BACKEND = 'mongodb'  # mongodb作为任务队列（或者说是缓存）
# BROKER_URL = 'mongodb://10.6.0.149:27017/'  # 队列地址
# CELERY_RESULT_BACKEND = 'mongodb://10.6.0.149:27017/'  # 消息结果存储地址
# CELERY_MONGODB_BACKEND_SETTINGS = {  # 消息结果存储配置
#     'host': '10.6.0.149',
#     'port': 27017,
#     'database': 'celery',
#     # 'user':'root',
#     # 'password':'root1234',
#     'taskmeta_collection': 'task_meta',  # 任务结果的存放collection
# }

CELERY_ROUTES = {  # 配置任务的先后顺序
    'celery_task.tasks.add': {'queue': 'for_add', 'router_key': 'for_add'},
    'celery_task.tasks.subtract': {'queue': 'for_subtract', 'router_key': 'for_subtract'}
}