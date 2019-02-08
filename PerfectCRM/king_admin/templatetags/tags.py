#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_app_name(admin_class):
    # print(admin_class.model._meta.verbose_name)
    return admin_class.model._meta.verbose_name_plural

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(obj, admin_class):
    row_ele = ''
    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_data = getattr(obj, "get_%s_display" % column)()
        else:
            column_data = getattr(obj, column)
        row_ele += "<td>%s</td>" %column_data

    return mark_safe(row_ele)