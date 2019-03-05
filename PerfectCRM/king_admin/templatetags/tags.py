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


@register.simple_tag
def render_page_ele(loop_counter,query_sets, filter_conditions):
    filters = ''
    for k,v in filter_conditions.items():
        filters += "&%s=%s" %(k,v)
    if abs(query_sets.number - loop_counter) <= 1:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class, loop_counter, filters, loop_counter)

        return mark_safe(ele)

    return ''


@register.simple_tag
def render_filter_ele(condition,admin_class,filter_conditions):
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %condition
    field_obj = admin_class.model._meta.get_field(condition)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            # print("choice",choice_item,filter_conditions.get(condition),type(filter_conditions.get(condition)))
            if filter_conditions.get(condition) == str(choice_item[0]):
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(condition) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def build_paginators(query_sets, filter_conditions):
    '''返回整个分页元素'''
    page_btns = ''
    filters = ''
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)
    added_dot_ele = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages -2 or abs(query_sets.number - page_num) <= 1:  # 代表最前或最后2页
            ele_class = ''
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns = '''<li class='%s'><a href='?page=%s%s'>%s</li>''' % (
            ele_class, page_num, filters, page_num)
        # elif abs(query_sets.number - page_num) <= 1:  # 判断当前页面的前后1页
        #     ele_class = ''
        #     if query_sets.number == page_num:
        #         ele_class = "active"
        #     page_btns = '''<li class='%s'><a href='?page=%s%s'>%s</li>''' % (
        #     ele_class, page_num, filters, page_num)
        else:  # 显示...
            if added_dot_ele == 'False':
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True

    return mark_safe(page_btns)

