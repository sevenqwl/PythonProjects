#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter()
# 字典取值
def truncate_value(dict, key_name):
    # print(dict)
    return dict.get(key_name, '')

# 三重字典取值
@register.filter()
def truncate_dict(dict, key_name):
    # print(dict)

    # m,n,k = key_name.split(',')
    # print(m,n,k)
    # print(dict.get(m))
    # if dict.get(m) is not None:
    #     if dict.get(m).get(n) is not None:
    #         return dict.get(m).get(n).get(k)
    #
    # return ""

    key_name_list = key_name.split('.')
    for i in key_name_list:
        if dict.get(i) is not None:
            dict = dict.get(i)
        else:
            return ""
    dict_value = dict
    return dict_value

@stringfilter
@register.filter()
# page url处理
def pageurl(pagenum, url):
    new_page = 'page=%s' % pagenum
    if 'page' in url:
        pattern = re.compile(r'page=\d+')
        new_url = re.sub(pattern, new_page, url)
    else:
        if '?' in url:
            new_url = url + '&' + new_page
        else:
            new_url = url + '?' + new_page
    return new_url

@register.filter()
def pagecounter(url, counter):
    return counter+url

@register.filter()
# 工位号取值
def truncate_position(ip, positions_data):
    position = positions_data.get(ip)
    return position

@register.filter()
# # MAC地址解析
def parsemac(sourcemac):
    if len(sourcemac) == 17:
        mac = sourcemac
    elif len(sourcemac) == 12:
        mac = re.sub('(\w{2})', r'\1:', sourcemac).rsplit(':', 1)[0]
    else:
        mac = ""
    return mac

@register.filter()
def nowtime(utctime, typestr):
    import datetime
    nowtime = utctime + datetime.timedelta(hours=+8)
    if typestr == "date":
        nowtime = nowtime.strftime("%Y-%m-%d")
    if typestr == "time":
        nowtime = nowtime.strftime("%H:%M:%S")
    return nowtime
