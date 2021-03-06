# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-09 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '客户表', 'verbose_name_plural': '客户表'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name_plural': '菜单'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': '账号表'},
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '已报名'), (1, '未报名')], default=1),
        ),
    ]
