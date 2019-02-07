#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

from Info import models

import os
import xlrd
import subprocess
import json
import time
import datetime
import yaml
import urllib.parse, urllib.request


'''
# SIP1 参数
"Sip1_Enable" # 是否启用SIP1
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable",
"Sip1_DisplayName" # SIP1显示名称
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_DisplayName",
"Sip1_Label" # SIP1标签
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_Label",
"Sip1_UserName" # SIP1用户
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_UserName",
"Sip1_AuthUserName" # SIP1注册名称
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName",
"Sip1_AuthPassword" # SIP1密码
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword",
"Sip1_RegistrarServer" # SIP1注册服务器地址
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.RegistrarServer",
"Sip1_OutboundProxy" # SIP1出局代理服务器地址
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxy",

# SIP2 参数
"Sip2_Enable" # 是否启用SIP2
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.Enable",
"Sip2_DisplayName" # SIP2显示名称
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_DisplayName",
"Sip2_Label" # SIP2标签
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_Label",
"Sip2_UserName" # SIP2用户名称
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_UserName",
"Sip2_AuthUserName" # SIP2注册名称
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthUserName",
"Sip2_AuthPassword" # SIP2密码
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthPassword",
"Sip2_RegistrarServer" # SIP2注册服务器地址
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.RegistrarServer",
"Sip2_OutboundProxy" # SIP2出局代理服务器地址
    "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.OutboundProxy",
'''
Genieacs_Server_IP = "10.6.0.149"
Port = 7557

Yealink_SIP_INFO = {
    # SIP1 参数
    "Sip1_Enable": {  # 是否启用SIP1
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip1_DisplayName": {  # SIP1显示名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_DisplayName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip1_Label": {  # SIP1标签
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_Label",
        "value": "1235",
        "type": "xsd:string",
    },
    "Sip1_UserName": {  # SIP1用户
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_UserName",
        "value": "1236",
        "type": "xsd:string",
    },
    "Sip1_AuthUserName": {  # SIP1注册名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName",
        "value": "1237",
        "type": "xsd:string",
    },
    "Sip1_AuthPassword": {  # SIP1密码
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip1_RegistrarServer": {  # SIP1注册服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.RegistrarServer",
        "value": "10.6.0.100",
        "type": "xsd:string",
    },
    "Sip1_UseOutboundProxy": {  # 是否启用SIP1出局代理
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.UseOutboundProxy",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip1_OutboundProxy": {  # SIP1出局代理服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxy",
        "value": "10.6.0.101",
        "type": "xsd:string",
    },
    "Sip1_AutoAnswerEnable": {  # 话机自动接听设置
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.X_001565_AutoAnswerEnable",
        "value": "",
        "type": "xsd:boolean"
    },

# SIP2 参数
    "Sip2_Enable": {  # 是否启用SIP2
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.Enable",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip2_DisplayName": {  # SIP2显示名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_DisplayName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_Label": {  # SIP2标签
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_Label",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_UserName": {  # SIP2用户名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_UserName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_AuthUserName": {  # SIP2注册名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthUserName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_AuthPassword": {  # SIP2密码
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthPassword",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_RegistrarServer": {  # SIP2注册服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.RegistrarServer",
        "value": "10.6.0.100",
        "type": "xsd:string",
    },
    "Sip2_UseOutboundProxy": {  # 是否启用SIP2出局代理
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.UseOutboundProxy",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip2_OutboundProxy": {  # SIP2出局代理服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.OutboundProxy",
        "value": "10.6.0.101",
        "type": "xsd:string",
    },
    "Sip2_AutoAnswerEnable": {  # 话机自动接听设置
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.X_001565_AutoAnswerEnable",
        "value": "",
        "type": "xsd:boolean"
    },

    # 其他参数
    "AdminPassword": {  # 设置管理员密码
        "parameter": "Device.UserInterface.X_001565_Update.X_001565_AdminPassword",
        "value": "wnwxwGJ",
        "type": "xsd:string",
    },
    "AutopServerAddress": {  # 配置文件升级地址
        "parameter": "Device.UserInterface.X_001565_Update.X_001565_AutoProvision.X_001565_AutopServerAddress",
        "value": "",
        "type": "xsd:string",
    },

}

Grandstream_SIP_INFO = {
    # SIP1 参数
    "Sip1_Enable": {  # 是否启用SIP1
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip1_DisplayName": {  # SIP1显示名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_GRANDSTREAM_DisplayName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip1_Label": {  # SIP1标签
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Name",
        "value": "1235",
        "type": "xsd:string",
    },
    "Sip1_UserName": {  # SIP1用户名称，注册时使用的分机号
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.DirectoryNumber",
        "value": "1236",
        "type": "xsd:string",
    },
    "Sip1_AuthUserName": {  # SIP1注册名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName",
        "value": "1237",
        "type": "xsd:string",
    },
    "Sip1_AuthPassword": {  # SIP1密码
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip1_RegistrarServer": {  # SIP1注册服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.RegistrarServer",
        "value": "10.6.0.100",
        "type": "xsd:string",
    },
    "Sip1_UseOutboundProxy": {  # 是否启用SIP1出局代理
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.UseOutboundProxy",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip1_OutboundProxy": {  # SIP1出局代理服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxy",
        "value": "10.6.0.101",
        "type": "xsd:string",
    },
    "Sip1_AutoAnswerEnable": {  # 话机自动接听设置
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.CallingFeatures.X_GRANDSTREAM_AutoAnswer",
        "value": "",
        "type": "xsd:boolean"
    },

# SIP2 参数
    "Sip2_Enable": {  # 是否启用SIP2
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.Enable",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip2_DisplayName": {  # SIP2显示名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_GRANDSTREAM_DisplayName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_Label": {  # SIP2标签
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Name",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_UserName": {  # SIP2用户名称，注册时使用的分机号
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.DirectoryNumber",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_AuthUserName": {  # SIP2注册名称
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthUserName",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_AuthPassword": {  # SIP2密码
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthPassword",
        "value": "1234",
        "type": "xsd:string",
    },
    "Sip2_RegistrarServer": {  # SIP2注册服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.RegistrarServer",
        "value": "10.6.0.100",
        "type": "xsd:string",
    },
    "Sip2_UseOutboundProxy": {  # 是否启用SIP2出局代理
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.UseOutboundProxy",
        "value": "Enabled",
        "type": "xsd:string",
    },
    "Sip2_OutboundProxy": {  # SIP2出局代理服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.OutboundProxy",
        "value": "10.6.0.101",
        "type": "xsd:string",
    },
    "Sip2_AutoAnswerEnable": {  # 话机自动接听设置
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.Line.1.CallingFeatures.X_GRANDSTREAM_AutoAnswer",
        "value": "",
        "type": "xsd:boolean"
    },

    # 其他参数
    "AdminPassword": {  # 设置管理员密码
        "parameter": "Device.UserInterface.X_GRANDSTREAM_AdminLoginPassword",
        "value": "wnwxwGJ",
        "type": "xsd:string",
    },
    "AutopServerAddress": {  # 配置文件升级地址
        "parameter": "Device.X_GRANDSTREAM_Upgrade.ConfigFile.ConfigServerPath",
        "value": "10.6.0.29/Configurations",
        "type": "xsd:string",
    },
    "UpgradeType": {  # 配置文件升级地址
        "parameter": "Device.X_GRANDSTREAM_Upgrade.UpgradeVia",
        "value": "HTTP",
        "type": "xsd:string",
    },
    "FirmwareUpgrade": {  # 固件文件升级地址
        "parameter": "Device.X_GRANDSTREAM_Upgrade.FirmwareUpgrade.FirmwareServerPath",
        "value": "10.6.0.29/Firmware",
        "type": "xsd:string",
    },
}

Error_Code = {
    0: 'Successful',
    10: '未获取到厂商品牌名称',
    20: '未有该IP信息的数据',
    21: 'IP地址不唯一',
    22: 'IP注释了',
    30: 'Parameter info Faild',
    40: '分机号已存在',
}

SIP_INFO = {
    'Yealink': Yealink_SIP_INFO,
    'Grandstream': Grandstream_SIP_INFO,
}

def code_info(error_code):
    code_info = Error_Code.get(error_code)
    return code_info


class Genieacs_api(object):
    def __init__(self):
        self.Genieacs_Server_IP = "10.6.0.149"
        self.Genieacs_Port = "7557"
        self.Genieacs_http_url = "http://%s:%s" %(self.Genieacs_Server_IP, self.Genieacs_Port)

    def query(self, query_str, projection_str):
        query_str = urllib.parse.quote(str(query_str))
        parameter_str = '%s&projection=%s' %(query_str, projection_str)
        request_api = "'%s/devices/?query=%s'" % (self.Genieacs_http_url, parameter_str)
        return request_api

    def setParameterValues(self, device_id, parameter_info):
        parameter_str = '{"name":"setParameterValues", "parameterValues":[%s]}' % parameter_info
        request_api = "'%s/devices/%s/tasks?timeout=3000&connection_request' -X POST --data '%s'" % (self.Genieacs_http_url, device_id, parameter_str)
        return request_api

    def refreshObject(self, device_id, parameter_info):
        parameter_str = '{"name":"refreshObject", "objectName":"%s"}' % parameter_info
        request_api = "'%s/devices/%s/tasks?timeout=3000&connection_request' -X POST --data '%s'" % (self.Genieacs_http_url, device_id, parameter_str)
        return request_api

    def reboot(self, device_id):
        parameter_str = '{"name":"reboot"}'
        request_api = "'%s/devices/%s/tasks?timeout=3000&connection_request' -X POST --data '%s'" % (self.Genieacs_http_url, device_id, parameter_str)
        return request_api


def request_exec_command(request_api, headerinfo="Y"):
    if headerinfo == "Y":
        request_command = "curl -i %s" % request_api
    else:
        request_command = "curl %s" % request_api
    request_obj = subprocess.Popen([request_command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    request_obj_stdout = request_obj.stdout.read().decode('utf-8')

    return request_obj_stdout


def transform_isotime(intime=1):
    intime = intime
    try:
        intime = 0 - int(intime)
    except:
        intime = -1
    now_time = datetime.datetime.utcnow()
    yes_time = now_time + datetime.timedelta(hours=intime)
    # yes_time_str = yes_time.isoformat()
    yes_time_str = yes_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return yes_time_str


# 获取excel表数据并转换成字典格式
def get_excel(excelname):
    data_dict = {}
    try:
        data = xlrd.open_workbook(excelname)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        for i in range(nrows):
            rowValues = table.row_values(i)
            if i == 0:
                nrows_name_list = rowValues
            else:
                data_dict[i] = {}
                for item in enumerate(rowValues):
                    nrows_name = str(nrows_name_list[item[0]]).strip()
                    if isinstance(item[1], float):  # 浮点数转换为整数
                        if item[1] == int(item[1]):
                            td_value = int(item[1])
                    else:
                        td_value = item[1]
                    data_dict[i][nrows_name] = str(td_value).strip()  # 转换为字符串并去除空格
    except:
        pass
    return data_dict


# 根据IP获取device_id
def get_device_info(IP):
    yes_time_str = transform_isotime()
    print(yes_time_str)
    query_str = '{"Device.LAN.IPAddress":"' + IP + '","_lastInform":{"$gt":"' + yes_time_str + '"}}'
    projection_str = 'Device.DeviceInfo.Manufacturer'
    req_url_obj = Genieacs_api() # 实例化Genieacs_api对象
    req_url = req_url_obj.query(query_str, projection_str)  # 获取请求的url
    print(req_url)
    # obj = subprocess.Popen(["curl 'http://10.6.0.149:7557/devices/?query=%7B%22Device.DeviceInfo.ManufacturerOUI%22:%22001565%22%7D&projection='"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    req_obj_stdout = request_exec_command(req_url, headerinfo="N")  # 执行请求的url，返回执行结果
    req_obj_stdout = json.loads(req_obj_stdout)  # string 转换成 dict
    device_count = len(req_obj_stdout)
    if  device_count == 1:  #
        device_id = req_obj_stdout[0]['_id']
        try:
            device_manufacturer = req_obj_stdout[0]['Device']['DeviceInfo']['Manufacturer']['_value']
            error_code = 0
        except:
            device_manufacturer = None
            error_code = 10
            print(IP + '    未获取到厂商品牌名称！！！')
    elif device_count == 0:
        print(IP + '    未有该IP信息的数据，请重新确认！！！')
        device_id = None
        device_manufacturer = None
        error_code = 20
    else:
        print(IP + '    IP地址不唯一，请重新确认！！！')
        device_id = None
        device_manufacturer = None
        error_code = 21

    device_dict = {
        'device_id': device_id,
        'device_manufacturer': device_manufacturer,
        'error_code': error_code,
    }
    return device_dict

# 转换成api参数格式
def str_format(device_parameter, device_value, string_type):
    format_value = '["%s", "%s", "%s"]' %(device_parameter, device_value, string_type)
    return str(format_value)


def sipinfo_method_dict(request_dict, sipinfo_dict, method):
    if method == "request_yaml_api":
        sip1_extension_list = ['Sip1_DisplayName', 'Sip1_Label', 'Sip1_UserName', 'Sip1_AuthUserName',
                               'Sip1_AuthPassword']
        sip2_extension_list = ['Sip2_DisplayName', 'Sip2_Label', 'Sip2_UserName', 'Sip2_AuthUserName',
                               'Sip2_AuthPassword']
        extension, platform = str(request_dict.get('分机号')).strip(), str(request_dict.get('电话平台')).strip()  # 获取分机号、电话平台
        sipinfo_dict = sipinfo_dict.get('platform').get(platform)
        if sipinfo_dict:
            for i in sip1_extension_list + sip2_extension_list:
                # for i in sip1_extension_list:
                if 'extensionself' in sipinfo_dict[i]:
                    if i == "Sip1_AuthPassword":
                        sipinfo_dict["Sip1_AuthPassword"] = sipinfo_dict[i].replace("extensionself", extension)
                    elif i == "Sip2_AuthPassword":
                        sipinfo_dict["Sip2_AuthPassword"] = sipinfo_dict[i].replace("extensionself", extension)
                    else:
                        sipinfo_dict[i] = sipinfo_dict[i].replace("extensionself", extension)
                        # print('Yaml...: ', request_data_dict)
        else:
            sipinfo_dict = None
    elif method == "request_define_api":
        sipinfo_dict = request_dict
    else:
        sipinfo_dict = None
    print(sipinfo_dict)
    return sipinfo_dict

# def sipinfo_yaml_dict(request_dict, sipinfo_dict):
#     sip1_extension_list = ['Sip1_DisplayName', 'Sip1_Label', 'Sip1_UserName', 'Sip1_AuthUserName', 'Sip1_AuthPassword']
#     sip2_extension_list = ['Sip2_DisplayName', 'Sip2_Label', 'Sip2_UserName', 'Sip2_AuthUserName', 'Sip2_AuthPassword']
#     extension, platform = str(request_dict.get('分机号')).strip(), str(request_dict.get('电话平台')).strip()  # 获取分机号、电话平台
#     sipinfo_dict = sipinfo_dict.get('platform').get(platform)
#     if sipinfo_dict:
#         for i in sip1_extension_list + sip2_extension_list:
#             # for i in sip1_extension_list:
#             if 'extensionself' in sipinfo_dict[i]:
#                 if i == "Sip1_AuthPassword":
#                     sipinfo_dict["Sip1_AuthPassword"] = sipinfo_dict[i].replace("extensionself", extension)
#                 elif i == "Sip2_AuthPassword":
#                     sipinfo_dict["Sip2_AuthPassword"] = sipinfo_dict[i].replace("extensionself", extension)
#                 else:
#                     sipinfo_dict[i] = sipinfo_dict[i].replace("extensionself", extension)
#                     # print('Yaml...: ', request_data_dict)
#
#     else:
#         sipinfo_dict = None
#     return sipinfo_dict
#
#
# def sipinfo_define_dict(sipinfo_dict):
#     sipinfo_dict = sipinfo_dict
#     # print(sipinfo_dict)
#     return sipinfo_dict


def check_extension(extension):  # 检测是否存在重复分机号,1小时内的分机号
    if extension:
        yes_time_str = transform_isotime()
        extension = str(extension)
        query_str = '{"VirtualParameters.SIP1":"' + extension + '","_lastInform":{"$gt":"' + yes_time_str + '"}}'
        projection_str = "VirtualParameters.SIP1,VirtualParameters.SIP2"
        req_url_obj = Genieacs_api()  # 实例化Genieacs_api对象
        req_url = req_url_obj.query(query_str, projection_str)  # 获取请求的url
        # print(req_url)
        req_obj_stdout = request_exec_command(req_url, headerinfo="N")  # 执行请求的url，返回执行结果
        result = json.loads(req_obj_stdout)  # string 转换成 dict
    else:
        result = ""

    return result


def get_request_url(request_data_dict, sipinfo_dict):
    parameter_info = ""
    isrepeat = False
    IP = request_data_dict.get('IP').strip()
    extension = sipinfo_dict.get('Sip1_AuthUserName').strip()
    if "#" in IP:
        request_url = None
        error_code = 22
        print("%s    注释了......." %IP)
    else:
        device_info = get_device_info(IP)
        device_id = device_info.get('device_id')  # quote()将字符串进行url编码
        device_manufacturer = device_info.get('device_manufacturer')
        error_code = device_info.get('error_code')
        if device_id and device_manufacturer:
            device_id = urllib.parse.quote(device_info.get('device_id'))  # quote()将字符串进行url编码

            print('xxxxxxxxxxxxxxxxxxxxxxxxx')
            check_extension_result = check_extension(extension)
            if len(check_extension_result) != 0:
                isrepeat = True
            for info in enumerate(sipinfo_dict):

                try:
                    if info[1] != "IP":
                        parameter_info += str_format(SIP_INFO[device_manufacturer][info[1]]['parameter'],
                                                 sipinfo_dict[info[1]],
                                                 SIP_INFO[device_manufacturer][info[1]]['type']) + ', '
                except:
                    error_code = 30
                    print("%s    Parameter_info Faild......." %IP)
            print(parameter_info)
            parameter_info = parameter_info.rsplit(', ', 1)[0]
            # print(parameter_info)
            if parameter_info:
                request_url_obj = Genieacs_api()
                request_url = request_url_obj.setParameterValues(device_id, parameter_info)
            else:
                request_url = None
                error_code = error_code
        else:
            request_url = None
            error_code = error_code
    request_url_dict = {'request_url': request_url, 'error_code': error_code, 'isrepeat': isrepeat, 'extension': extension}

    print(request_url_dict)

    return request_url_dict


def request_logcontent(reqeust_obj_stdout, IP, isrepeat, extension):
    if isrepeat == True:
        repeat_code = "该分机号重复..."
    else:
        repeat_code = ""
    if "HTTP/1.1 200 OK" in reqeust_obj_stdout:
        print("%s  %s  %s   HTTP/1.1 200 OK" % (IP, extension, repeat_code))
        logcontent = "%s  %s  %s   HTTP/1.1 200 OK" % (IP, extension, repeat_code)
    elif "HTTP/1.1 202 Task queued but not processed" in reqeust_obj_stdout:
        print("%s  %s  %s   HTTP/1.1 202 Task queued but not processed" % (IP, extension, repeat_code))
        logcontent = "%s  %s  %s   HTTP/1.1 202 Task queued but not processed" % (IP, extension, repeat_code)
    elif "HTTP/1.1 202 Device is offline" in reqeust_obj_stdout:
        print("%s  %s  %s   HTTP/1.1 202 Device is offline" % (IP, extension, repeat_code))
        logcontent = "%s  %s  %s   HTTP/1.1 202 Device is offline" % (IP, extension, repeat_code)
    elif "HTTP/1.1 202 Task faulted" in reqeust_obj_stdout:
        print("%s  %s  %s   HTTP/1.1 202 Task faulted" % (IP, extension, repeat_code))
        logcontent = "%s  %s  %s   HTTP/1.1 202 Task faulted" % (IP, extension, repeat_code)
    else:
        print("%s  配置失败啦......" % IP)
        logcontent = "%s  %s  %s    %s" %(IP, extension, repeat_code, reqeust_obj_stdout)

    return logcontent

