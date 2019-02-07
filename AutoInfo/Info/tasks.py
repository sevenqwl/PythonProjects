#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.schedules import crontab
from AutoInfo.celery import app
import datetime


# 检测时间范围
def check_time(time1, time2):
    flag = False
    now_time = datetime.datetime.now()
    try:
        d_time1 = datetime.datetime.strptime(str(now_time.date())+time1, '%Y-%m-%d%H:%M')
        d_time2 = datetime.datetime.strptime(str(now_time.date())+time2, '%Y-%m-%d%H:%M')

        if now_time > d_time1 and now_time < d_time2:
            flag = True
        else:
            flag = False
    except Exception as e:
        print(e)
    return flag


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


# @shared_task
# def reboot_phone(device_id, device_ip):
#     import subprocess
#
#     # device_id = "000B82-GXP1625-000b827fd280"
#     # device_ip = "10.6.39.241"
#     if device_id:
#         Genieacs_http_url = "http://10.6.0.149:7557"
#         parameter_str = '{"name":"reboot"}'
#         request_api = "'%s/devices/%s/tasks?timeout=10000&connection_request' -X POST --data '%s'" % (Genieacs_http_url, device_id, parameter_str)
#         print(request_api)
#         request_command = "curl -i %s" % request_api
#         request_obj = subprocess.Popen([request_command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
#                                        stderr=subprocess.PIPE)
#         request_result = request_obj.stdout.read().decode('utf-8')
#         print(request_result)
#         # logcontent = acs_script.request_logcontent(request_result, device_ip, isrepeat=False, extension="")  # 返回执行结果匹配
#         logcontent = "%s Reboot Successful..." %device_ip
#     else:
#         logcontent = "%s Reboot Faild..." %device_ip
#     return logcontent

@shared_task
def reboot_phone(device_id, device_ip):
    from Info.utils import acs_script
    # device_id = "000B82-GXP1625-000b827fd280"
    # device_ip = "10.6.39.241"
    if device_id:
        api_obj = acs_script.Genieacs_api()
        request_api = api_obj.reboot(device_id)
        print(request_api)
        request_result = acs_script.request_exec_command(request_api)
        print(request_result)
        logcontent = acs_script.request_logcontent(request_result, device_ip, isrepeat=False, extension="")  # 返回执行结果匹配
        # logcontent = "%s Reboot Successful..." %device_ip
    else:
        logcontent = "%s Reboot Faild..." %device_ip
    return logcontent

@shared_task
def crontab_reboot():
    import pymongo, re, datetime, time
    from Info.utils import area
    from Info.templatetags.custom import truncate_dict

    Mongodb_IP = "10.6.0.144"
    Port = 27017
    # 获取区域信息
    area_code = "yz"
    area_dict = area.area_dict
    area_info = area.area_info(area_dict, area_code)  # 获取对应区域节点的信息
    rearea = area_info.get('pattern')  # 获取区域的正则表达式

    client = pymongo.MongoClient(Mongodb_IP, Port)
    db = client.genieacs
    collection = db.devices

    conditions_list = []
    sortstr = [("Device.LAN.IPAddress._value", 1)]
    now_utctime = datetime.datetime.utcnow()
    diff_time = 480*60*60
    # yes_time = now_utctime + datetime.timedelta(hours=inhours)
    lastInform_diff_time = now_utctime + datetime.timedelta(hours=-0.25)
    # print(yes_time)
    search_conditions = {
        "$and": [
            # {"$or": conditions_list},
            {'Device.LAN.IPAddress._value': re.compile(rearea, re.I)},
            {"Device.DeviceInfo.UpTime._value": {"$gt": diff_time}},
            {"_lastInform": {"$gt": lastInform_diff_time}},
        ]
    }
    print(search_conditions)
    limit_count = 300
    genieacs_list = collection.find(search_conditions, {"Device.LAN.IPAddress": 1, "Device.LAN.MACAddress": 1,
                                                        "_lastInform": 1, "Device.DeviceInfo.UpTime": 1}).sort(sortstr).limit(limit_count)
    for i in genieacs_list:
        timer = check_time("4:00", "6:00")
        if timer:
            device_id = i.get('_id')
            device_ip = truncate_dict(i, "Device.LAN.IPAddress._value")
            print("IP, ID: ", device_ip, device_id)
            res = reboot_phone.delay(device_id, device_ip)
            time.sleep(5)
        else:
            print("未在计划重启的时间范围...")


    # device_id = "000B82-GXP1625-000b827fd280"
    # device_ip = "10.6.39.241"
    # res = reboot_phone.delay(device_id, device_ip)
    # device_id = "000B82-GXP1625-000b827fd249"
    # device_ip = "10.7.28.250"
    # res = reboot_phone.delay(device_id, device_ip)

    return "Crontab Tasks is Finished..."



