#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

from crm import models

enabled_admins = {}
''''
enabled_admins最终的字典形式如下
{"crm":
     {'userprofile': admin_class,
      'customer': customer_admin}
}'''

class BaseAdmin(object):
    list_display = []
    list_filter = []
    list_per_page = 20

class CustomerAdmin(BaseAdmin):
    list_display = ['qq', 'name', 'source', 'consultant', 'consult_course', 'date', 'status']
    list_filters = ['source', 'consultant', 'consult_course', 'status']
    list_per_page = 2
    # model = models.Customer

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:  # model_class._meta.app_label 获取app名称
        enabled_admins[model_class._meta.app_label] = {}

    # admin_obj = admin_class()
    admin_class.model = model_class  # 绑定model对象和admin类  相当于model = models.Customer
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class  # 相当于enabled_admins['crm']['customer'] = CustomerAdmin


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)