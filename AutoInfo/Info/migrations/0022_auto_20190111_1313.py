# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-11 05:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Info', '0021_auto_20190111_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celerytaskrecord',
            name='args',
        ),
        migrations.RemoveField(
            model_name='celerytaskrecord',
            name='kwargs',
        ),
        migrations.RemoveField(
            model_name='celerytaskrecord',
            name='result',
        ),
        migrations.RemoveField(
            model_name='celerytaskrecord',
            name='task_name',
        ),
    ]
