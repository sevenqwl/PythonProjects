# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-01 15:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduled_tasks', '0005_database'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataBase',
            new_name='DataBaseInfo',
        ),
        migrations.AlterModelTable(
            name='databaseinfo',
            table='databaseinfo',
        ),
    ]
