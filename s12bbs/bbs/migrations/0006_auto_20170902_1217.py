# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-02 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0005_auto_20170902_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='head_img',
            field=models.ImageField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
