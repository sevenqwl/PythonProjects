#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"


# pattern = "10\.([7]\.[579]|6\.[0-64])"
# pattern = "10\.([7]\.([1-5][0-9]|6[0-4]|[0-9])\.|6\.([1-5][0-9]|6[0-4]|[0-9])\.)"  # 10.6.0-64, 10.7.0-64
pattern = "10\.([7]\.([1-5][0-9]|6[0-4]|[0-9])|6\.([1-5][0-9]|6[0-4]|[0-9]))\.\d+"
sq_pattern = "10\.[45]\.\d+"
sq_104 = "10\.[4]\.\d+"
sq_105 = "10\.[5]\.\d+"

xq_hacj = "10.7.255.\d+"
xq_xys = "10.7.254.\d+"
area_dict = {
    'all': {"pattern": ".*", "name": "所有区域"},
    'yz': {"pattern": "^(%s)" %pattern, "name": "扬州"},
    'sq': {"pattern": "^(%s)" %sq_pattern, "name": "宿迁"},
    'sq_104': {"pattern": "^(%s)" %sq_104, "name": "宿迁-10.4网段"},
    'sq_105': {"pattern": "^(%s)" %sq_105, "name": "宿迁-10.5网段"},
    'xq': {"pattern": "^(?!(%s|%s))" %(pattern, sq_pattern), "name": "校企"},
    'xq_hacj': {"pattern": "^(%s)" %(xq_hacj), "name": "校企-淮安财经"},
    'xq_xys': {"pattern": "^(%s)" %(xq_xys), "name": "校企-西亚斯"},

}

def area_info(area_dict, area_code):
    area_info = area_dict.get(area_code)
    if not area_info:
        area_code = "all"
        area_info = area_dict.get(area_code)
    return area_info
