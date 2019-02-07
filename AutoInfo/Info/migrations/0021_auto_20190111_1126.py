# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-11 03:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Info', '0020_auto_20190110_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='celerytaskrecord',
            name='args',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='celerytaskrecord',
            name='kwargs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='celerytaskrecord',
            name='result',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='celerytaskrecord',
            name='task_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
