#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

#-*- coding:utf-8 -*-

def get_excel_value(paratemers, dict):

    if '.' in paratemers:
        paratemer_list = paratemers.split('.')
        for i in paratemer_list:
            # print(dict)
            if dict is not None:
                dict = dict.get(i)
            else:
                excel_value = ""
                return excel_value
        if dict is not None:
            excel_value = dict.get('_value')
        else:
            excel_value = ""
    else:
        excel_value = ""
    return excel_value
