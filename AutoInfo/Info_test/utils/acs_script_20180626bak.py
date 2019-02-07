#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

import os
import xlrd
import subprocess
import json
import time
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

    "AdminPassword": {  # 设置管理员密码
        "parameter": "Device.UserInterface.X_GRANDSTREAM_AdminLoginPassword",
        "value": "wnwxwGJ",
        "type": "xsd:string",
    },
    "AutopServerAddress": {  # 配置文件升级地址
        "parameter": "Device.X_GRANDSTREAM_Upgrade.ConfigFile.ConfigServerPath",
        "value": "",
        "type": "xsd:string",
    },
}

SIP_INFO = {
    'Yealink': Yealink_SIP_INFO,
    'Grandstream': Grandstream_SIP_INFO,
}

# 获取excel表数据并转换成字典格式
def get_excel(excelname):
    data_dict = {}
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
    return data_dict

# 根据IP获取device_id
def get_device_info(IP):
    req_parameter_str = '%7B"Device.LAN.IPAddress":"' + IP + '"%7D&projection=Device.DeviceInfo.Manufacturer'
    req_url = "http://%s:%s/devices/?query=%s" % (Genieacs_Server_IP, Port, req_parameter_str)
    req_command = "curl '%s'" %req_url
    req_obj = subprocess.Popen([req_command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # obj = subprocess.Popen(["curl 'http://10.6.0.149:7557/devices/?query=%7B%22Device.DeviceInfo.ManufacturerOUI%22:%22001565%22%7D&projection='"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    req_obj_stdout = req_obj.stdout.read().decode('utf-8')
    req_obj_stdout = json.loads(req_obj_stdout)  # string 转换成 dict
    if len(req_obj_stdout) == 1:
        device_id = req_obj_stdout[0]['_id']
        try:
            device_manufacturer = req_obj_stdout[0]['Device']['DeviceInfo']['Manufacturer']['_value']
        except:
            device_manufacturer = None
            print('未获取到厂商品牌名称！！！')
    else:
        print('IP地址不唯一，请重新确认！！！')
        device_id = None
        device_manufacturer = None
    device_dict = {
        'device_id': device_id,
        'device_manufacturer': device_manufacturer,
    }
    return device_dict

# 转换成api参数格式
def str_format(device_parameter, device_value, string_type):
    format_value = '["%s", "%s", "%s"]' %(device_parameter, device_value, string_type)
    return str(format_value)

# 拼接成请求的api
def request_api(set_dict):
    Parameter_info = ""
    IP = set_dict.get('IP')
    if "#" in IP:
        IP = ""
    if IP:
        device_info = get_device_info(IP)
        if device_info['device_id'] and device_info['device_manufacturer']: 
            device_id = urllib.parse.quote(device_info['device_id'])  #quote()将字符串进行url编码
            device_manufacturer = device_info['device_manufacturer']
            print(set_dict)
            for info in enumerate(set_dict):
                print(info)
                try:
                    if info[0] < (len(set_dict) - 1):
                        Parameter_info += str_format(SIP_INFO[device_manufacturer][info[1]]['parameter'], set_dict[info[1]], SIP_INFO[device_manufacturer][info[1]]['type']) + ', '
                    else:
                        Parameter_info += str_format(SIP_INFO[device_manufacturer][info[1]]['parameter'], set_dict[info[1]], SIP_INFO[device_manufacturer][info[1]]['type'])
                except:
                    pass
            # print(Parameter_info)
            Parameter_str = '{"name":"setParameterValues", "parameterValues":[%s]}' % Parameter_info
            REQUEST_SET_API = "'http://%s:%s/devices/%s/tasks?timeout=3000&connection_request' -X POST --data '%s'" % (Genieacs_Server_IP, Port, device_id, Parameter_str)
            return REQUEST_SET_API
        else:
            return None
    else:
        return None

