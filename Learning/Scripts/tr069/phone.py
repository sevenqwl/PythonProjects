
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

import os


# curl -i 'http://10.6.0.149:7557/devices/001565-SIP%252DT22P-0015652e0372/tasks?timeout=3000&connection_request' -X POST
# --data '{"name":"setParameterValues", "parameterValues":[["", "8002", "xsd:string"],["", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.X_001565_UserName", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword", "jd8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.1.SIP.RegistrarServer", "10.6.0.250", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxy", "10.6.0.250", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable", "Enabled", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_DisplayName", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_Label", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.X_001565_UserName", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthUserName", "8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.Line.1.SIP.AuthPassword", "jd8002", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.SIP.RegistrarServer", "10.6.0.251", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.SIP.OutboundProxy", "10.6.0.251", "xsd:string"],["Device.Services.VoiceService.1.VoiceProfile.2.Line.1.Enable", "Enabled", "xsd:string"]]}'

def str_format(device_parameter, device_value, string_type):
    a = '["%s", "%s", "%s"]' %(device_parameter, device_value, string_type)
    return str(a)


SIP_INFO = {
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
    "Sip1_UserName": {  # SIP1用户名称
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
    "Sip2_OutboundProxy": {  # SIP2出局代理服务器地址
        "parameter": "Device.Services.VoiceService.1.VoiceProfile.2.SIP.OutboundProxy",
        "value": "10.6.0.101",
        "type": "xsd:string",
    },
}
Genieacs_Server_IP = "10.6.0.149"
Port = 7557
device_id = "001565-SIP%252DT22P-0015652e0372"

x=""
for info in enumerate(SIP_INFO):
    print(info)
    if info[0] < (len(SIP_INFO) -1):
        x += str_format(SIP_INFO[info[1]]['parameter'], SIP_INFO[info[1]]['value'], SIP_INFO[info[1]]['type']) + ', '
    else:
        x += str_format(SIP_INFO[info[1]]['parameter'], SIP_INFO[info[1]]['value'], SIP_INFO[info[1]]['type'])
print(x)

Parameter =  '{"name":"setParameterValues", "parameterValues":[%s]}' %x
REQUEST_SET_API = "'http://%s:%s/devices/%s/tasks?timeout=3000&connection_request' -X POST --data '%s'" %(Genieacs_Server_IP, Port, device_id, Parameter)


REQUEST_COMMAND = 'curl -i %s' %REQUEST_SET_API
os.system(REQUEST_COMMAND)
