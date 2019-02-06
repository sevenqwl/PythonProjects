# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-06 12:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name_plural': '校区'},
        ),
        migrations.AlterModelOptions(
            name='classlist',
            options={'verbose_name_plural': '班级表'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name_plural': '课程表'},
        ),
        migrations.AlterModelOptions(
            name='courserecord',
            options={'verbose_name_plural': '上课记录'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': '客户表'},
        ),
        migrations.AlterModelOptions(
            name='customerfollowup',
            options={'verbose_name_plural': '客户跟进表'},
        ),
        migrations.AlterModelOptions(
            name='enrollment',
            options={'verbose_name_plural': '报名表'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name_plural': '缴费记录'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name_plural': '角色表'},
        ),
        migrations.AlterModelOptions(
            name='studyrecord',
            options={'verbose_name_plural': '学习记录'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '标签表'},
        ),
        migrations.AlterUniqueTogether(
            name='studyrecord',
            unique_together=set([('student', 'course_record')]),
        ),
    ]
