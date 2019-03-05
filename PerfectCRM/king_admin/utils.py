#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

def table_filter(request, admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}
    for k,v in request.GET.items():
        if k == 'page':  # 保留的分页关键字
            continue
        if v:
            filter_conditions[k] = v

    print('filter_conditions', filter_conditions)

    return admin_class.model.objects.filter(**filter_conditions), filter_conditions