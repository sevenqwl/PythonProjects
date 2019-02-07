#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoInfo.settings')

app = Celery('AutoInfo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object('AutoInfo.celery_config')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# 定时任务
app.conf.beat_schedule = {
    'add-crontab-reboot': {
        'task': 'Info.tasks.crontab_reboot',
        'schedule': crontab(hour=4, minute=1, day_of_week="*"),
        'args': (),
    }
}

# app.conf.beat_schedule = {
#     'add-every-minute': {
#         'task': 'Info.tasks.add',
#         'schedule': crontab(hour=19, minute="*", day_of_week="*"),
#         'args': (1, 2),
#     }
# }
