# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bbs', '0007_auto_20170908_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('brief', models.CharField(blank=True, max_length=255, null=True)),
                ('max_members', models.IntegerField(default=200)),
                ('admins', models.ManyToManyField(blank=True, related_name='group_admins', to='bbs.UserProfile')),
                ('members', models.ManyToManyField(blank=True, related_name='group_members', to='bbs.UserProfile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.UserProfile')),
            ],
        ),
    ]
