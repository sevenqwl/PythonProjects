from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.core.cache import cache
from django.forms.models import model_to_dict


from Info import models
import xlwt
from io import StringIO, BytesIO
import datetime
from math import floor, ceil
import json
import pymongo
import re
import os, queue, subprocess, time, random
from Info.utils import acs_script, get_excel, mongodb_conn
from Info.utils import area
from Info.templatetags import custom
import pytz
import yaml


Mongodb_IP = "10.6.0.144"
Port = 27017

list_pagenum = [1, 2, 3, 4, 5]


# Create your views here.
def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect(request.GET.get('next') or '/info/genieacs')
        else:
            login_err = "Wrong username or password!"
            print(login_err)
            return render(request, 'login.html', {'login_err': login_err})

    return render(request, 'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


# 获取用户IP地址
def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip

# @login_required()
def index(request):
    return render(request, 'NeuBoard/index.html')


def ui_buttons(request):
    return render(request, 'NeuBoard/ui-buttons.html')

def ui_icons(request):
    return render(request, 'NeuBoard/ui-icons.html')


# @login_required()
def extensions(request):
    # obj = models.Hardwareinfo.objects.filter(mac1='D8:CB:8A:5C:99:AF').values('switchinfo__ip')
    # print(obj)

    regip = get_client_ip(request)  # 获取用户IP地址
    list_pagenum = [0, 1, 2, 3, 4, 5]
    print(list_pagenum)
    # 每页显示多少条记录
    pagenumper = request.GET.get('pagenumper')
    try:
        pagenumper = int(pagenumper)
        if pagenumper == 0:
            pagenumper = 100
    except:
        pagenumper = 100
    extensions_obj = models.Phoneinfo.objects.all().order_by('id')  # 获取所有话机信息对象
    paginator = Paginator(extensions_obj, pagenumper)  # Default Show 100 per page
    total_count = paginator.count  # 总数据量
    num_pages = paginator.num_pages  # 总页面量

    page = request.GET.get('page')
    try:
        extensions_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        extensions_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        extensions_list = paginator.page(paginator.num_pages)

    online_num = models.Phoneinfo.objects.filter(ping_status='online').count()
    offline_num = total_count - online_num
    print(online_num)

    if request.is_ajax():
        data = serializers.serialize("json", extensions_list)
        return HttpResponse(data, content_type="application/json")

    # return render(request, 'NeuBoard/extensions.html', locals())  # locals() 表示
    return render(request, 'NeuBoard/extensions.html', {'extensions_list': extensions_list,
                                                            'list_pagenum': list_pagenum,
                                                            'total_count': total_count,
                                                            'num_pages': num_pages,
                                                            'online_num': online_num,
                                                            'offline_num': offline_num,
                                                        })

# @login_required()
def genieacs(request):
    # 获取用户IP地址
    regip = get_client_ip(request)  # 获取用户IP地址
    print(regip)
    # 获取区域信息
    area_code = request.COOKIES.get('area')
    area_dict = area.area_dict
    area_info = area.area_info(area_dict, area_code)  # 获取对应区域节点的信息
    rearea = area_info.get('pattern')  # 获取区域的正则表达式
    # 每页显示的数量
    pagenumper = request.COOKIES.get('pagenumper')
    try:
        pagenumper = int(pagenumper)
        if pagenumper <= 0:
            pagenumper = 100
    except:
        pagenumper = 100
    # 页面数
    page = request.GET.get('page')
    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1
    skip_num = (page-1) * pagenumper
    # print(skip_num)

    # 连接mongodb
    client = pymongo.MongoClient(Mongodb_IP, 27017)
    db = client.genieacs
    collection = db.devices
    task_collection = db.tasks
    task_count = task_collection.find().count()

    # search_conditions = {}
    search_conditions = {'Device.LAN.IPAddress._value': re.compile(rearea, re.I)}
    sortstr = [("Device.LAN.IPAddress._value", 1)]
    # sortstr = [("_lastInform", -1)]
    # sortstr = [("Device.DeviceInfo.UpTime._value", -1)]
    # sortstr = request.GET.get('sortstr')
    # sortvalue = request.GET.get('sortvalue')
    # try:
    #     page = int(page)
    #     if page < 1:
    #         page = 1
    # except:
    #     sortvalue = 1
    repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value', 'count': {'$sum': 1}, 'date': { '$addToSet': "$_lastInform"}}},
                                        {'$match': {'count': {'$gt': 1}}},
                                        {'$sort': {'_id': 1}}
                                        ])
    repeat_list_count = 0
    now_utctime = datetime.datetime.utcnow()
    compare_utctime = now_utctime + datetime.timedelta(hours=-0.25)
    for j in repeat_list:
        if j.get('_id'):
            date_arr = j.get('date')
            flag = 0
            for x in date_arr:
                if x < compare_utctime:
                    flag = 1
            if flag == 0:  # flag=0表示重复分机号lastInform时间<15分钟
                repeat_list_count += 1

    if request.method == "GET":
        conditions_list = []
        multilist = request.GET.get('multishow')
        if multilist:
            multilist = multilist.split("\r\n")
            # print(multilist)
            parameters_list = ["Device.LAN.IPAddress", "VirtualParameters.SIP1", "VirtualParameters.SIP2"]

            for i in parameters_list:
                for j in multilist:
                    if j:
                        parameters_value_str = {i + "._value": j.strip()}
                        conditions_list.append(parameters_value_str)
            # search_conditions = {"$or": conditions_list}
            search_conditions = {
                "$and": [
                    {"$or": conditions_list},
                    {'Device.LAN.IPAddress._value': re.compile(rearea, re.I)}
                    ]
                }
        else:
            searchtype = request.GET.get('searchtype')
            if searchtype=="search":
                search_keywords = request.GET.get('search_keywords')
                if search_keywords is not None:
                    parameters_list = ["_lastInform", "Device.LAN.IPAddress","Device.LAN.MACAddress",
                                       "Device.DeviceInfo.ProductClass", "VirtualParameters.SIP1",
                                       "VirtualParameters.SIP1 Status", "VirtualParameters.SIP1 RegistrarServer",
                                       "VirtualParameters.SIP2", "VirtualParameters.SIP1 Status",
                                       "VirtualParameters.SIP2 RegistrarServer", "VirtualParameters.AutoUpdate Url"]
                    for i in parameters_list:
                        parameters_value_str = {i + "._value": re.compile(search_keywords.strip(), re.I)}
                        conditions_list.append(parameters_value_str)
                    # search_conditions = {"$or": conditions_list}
                    search_conditions = {
                        "$and": [
                            {"$or": conditions_list},
                            {'Device.LAN.IPAddress._value': re.compile(rearea, re.I)}
                        ]
                    }
            elif searchtype=="repeat_list":
                intime = request.GET.get('intime')
                try:
                    inhours = 0-float(intime)
                except:
                    inhours = 0
                print(inhours)
                yes_time = now_utctime + datetime.timedelta(hours=inhours)
                repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value',
                                                                'count': {'$sum': 1},
                                                                'date': {'$addToSet': "$_lastInform"}}},
                                                    {'$match': {'count': {'$gt': 1}}},
                                                    {'$sort': {'_id': 1}}
                                                    ])
                # repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value', 'count': {'$sum': 1}}},
                #                                      {'$match': {"$and":[{'count': {'$gt': 1}}, {"_lastInform":{"$gte": yes_time_utc}}]}},
                #                                      {'$sort': {'_id': 1}}
                #                                      ])
                # print(repeat_list)
                # sortvalue = "VirtualParameters.SIP1._value"
                sortstr = [("VirtualParameters.SIP1._value",1), ("Device.LAN.IPAddress._value", 1)]
                parameters_list = ["VirtualParameters.SIP1",]


                for i in parameters_list:
                    for j in repeat_list:
                        if j.get('_id'):
                            if inhours != 0:
                                temp_date = j.get('date')
                                flag = 0
                                for x in temp_date:
                                    if x < yes_time:
                                        flag = 1
                                if flag == 0:  # flag=0表示重复分机号lastInform时间<15分钟
                                    parameters_value_str = {i + "._value": j.get('_id').strip()}
                                    conditions_list.append(parameters_value_str)
                            else:
                                parameters_value_str = {i + "._value": j.get('_id').strip()}
                                conditions_list.append(parameters_value_str)
                print(conditions_list)
                if len(conditions_list) != 0:
                    if intime:
                        search_conditions = {"$and":[{"$or": conditions_list}, {"_lastInform":{"$gt": yes_time}}]}
                        search_conditions = {
                            "$and": [
                                {"$or": conditions_list},
                                # {'Device.LAN.IPAddress._value': re.compile(rearea, re.I)},
                                {"_lastInform": {"$gt": yes_time}}
                            ]
                        }
                    else:
                        search_conditions = {
                            "$and": [
                                {"$or": conditions_list},
                                {'Device.LAN.IPAddress._value': re.compile(rearea, re.I)}
                            ]
                        }
                    print(conditions_list)
                else:
                    return HttpResponse('没有重复数据')

    # print(search_conditions)
    repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value', 'count': {'$sum': 1}}},
                                        {'$match': {'count': {'$gt': 1}}},
                                        {'$sort': {'_id': 1}}
                                        ])


    # genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "Device.DeviceInfo.ProductClass":1, "VirtualParameters": 1, "_lastInform": 1}).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
    genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1,
                                                        "Device.DeviceInfo.ProductClass":1, "Device.DeviceInfo.SoftwareVersion":1,
                                                        "VirtualParameters": 1, "_lastInform": 1, "_lastBootstrap": 1, "_lastBoot": 1,
                                                        "Device.DeviceInfo.UpTime": 1}).sort(sortstr).skip(skip_num).limit(pagenumper)
    # print(genieacs_list)
    total_count = genieacs_list.count()
    num_pages = ceil(total_count / pagenumper)
    # print('genieacs_list end')

    # 获取PositionsRelation
    positions_obj = models.PositionsRelation.objects.all().values()
    positions_data = {}
    for i in positions_obj:
        positions_data[i['ip']] = i['position']

    return render(request, 'NeuBoard/genieacs.html', {'genieacs_list':genieacs_list,
                                                        'page': page,
                                                        'total_count': total_count,
                                                        'num_pages': num_pages,
                                                        'list_pagenum': list_pagenum,
                                                        'id_num': skip_num,
                                                        'positions_data': positions_data,
                                                        'repeat_list': repeat_list,
                                                        'repeat_list_count': repeat_list_count,
                                                        'task_count': task_count,
                                                        'area_info': area_info,
                                                        })


# @login_required()
def genieacs_tasks(request):
    regip = get_client_ip(request)  # 获取用户IP地址

    pagenumper = request.COOKIES.get('pagenumper')
    try:
        pagenumper = int(pagenumper)
        if pagenumper <= 0:
            pagenumper = 100
    except:
        pagenumper = 100

    page = request.GET.get('page')
    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1
    skip_num = (page-1) * pagenumper
    # print(skip_num)

    # 连接mongodb
    client = pymongo.MongoClient(Mongodb_IP, 27017)
    db = client.genieacs
    collection = db.tasks

    search_conditions = {}
    sortstr = [("device", 1)]
    # sortstr = [("_lastInform", -1)]
    # sortstr = [("Device.DeviceInfo.UpTime._value", -1)]
    # sortstr = request.GET.get('sortstr')
    # sortvalue = request.GET.get('sortvalue')
    # try:
    #     page = int(page)
    #     if page < 1:
    #         page = 1
    # except:
    #     sortvalue = 1

    if request.method == "GET":
        conditions_list = []
        multilist = request.GET.get('multishow')


    # print(search_conditions)

    genieacs_list = collection.find(search_conditions).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
    # genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "Device.DeviceInfo.ProductClass":1, "VirtualParameters": 1, "_lastInform": 1}).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
    # genieacs_list = collection.find(search_conditions).sort(sortstr).skip(skip_num).limit(pagenumper)
    # print(genieacs_list)
    total_count = genieacs_list.count()
    num_pages = ceil(total_count / pagenumper)
    # print('genieacs_list end')

    # 获取PositionsRelation
    positions_obj = models.PositionsRelation.objects.all().values()
    positions_data = {}
    for i in positions_obj:
        positions_data[i['ip']] = i['position']

    return render(request, 'NeuBoard/genieacs-tasks.html', {'genieacs_list':genieacs_list,
                                                        'page': page,
                                                        'total_count': total_count,
                                                        'num_pages': num_pages,
                                                        'list_pagenum': list_pagenum,
                                                        'id_num': skip_num,
                                                        'positions_data': positions_data,
                                                        })


def genieacs_log(request):
    log_dir = os.path.dirname(os.path.dirname(__file__)) + '/media'
    print(os.path.dirname(os.path.dirname(__file__)) + '/media')
    list = os.listdir(log_dir)
    log_list = []
    for i in range(len(list)):
        path = list[i]
        if '.log' in path:
            print(path)
            log_list.append(path)
    log_list.sort(reverse=True)

    return render(request, 'NeuBoard/genieacs-log.html', {'log_list': log_list,})


def genieacs_yaml(request):
    yaml_file = os.path.dirname(__file__) + '/utils/config_file.yaml'
    print(yaml_file)
    if os.path.exists(yaml_file):
        with open(yaml_file, 'rb') as f:
            yaml_content = f.read().decode('utf-8')
    else:
        yaml_content = None


    return render(request, 'NeuBoard/genieacs-yaml.html', {'yaml_content': yaml_content,})

# def genieacs(request):
#     regip = get_client_ip(request)  # 获取用户IP地址
#
#     pagenumper = request.GET.get('pagenumper')
#     try:
#         pagenumper = int(pagenumper)
#         if pagenumper <= 0:
#             pagenumper = 100
#     except:
#         pagenumper = 100
#
#     page = request.GET.get('page')
#     try:
#         page = int(page)
#         if page < 1:
#             page = 1
#     except:
#         page = 1
#     skip_num = (page-1) * pagenumper
#
#     client = pymongo.MongoClient(Mongodb_IP, 27017)
#     db = client.genieacs
#     collection = db.devices
#     genieacs_list = collection.find({},{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "VirtualParameters": 1, "_lastInform": 1}).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
#     total_count = collection.count()
#     num_pages = ceil(total_count / pagenumper)
#
#     return render(request, 'NeuBoard/genieacs.html', {'genieacs_list':genieacs_list,
#                                                         'page': page,
#                                                         'total_count': total_count,
#                                                         'num_pages': num_pages,
#                                                         'list_pagenum': list_pagenum,
#                                                         'id_num': skip_num,
#                                                         })
#


def file_upload(request):
    # file_obj = request.FILES
    file_data = request.FILES.get('file_data')
    msg_data = request.POST.get('msg_data')  #当前获取到的type为string
    msg_data = json.loads(msg_data)  # 转换成字典格式
    media_home_dir = "media"
    print(media_home_dir)
    if not os.path.isdir(media_home_dir):
        os.mkdir(media_home_dir)
    timestamp = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
    randomstamp = random.randint(1000,9999)
    new_file_name = "%s/%s__%s__%s" % (media_home_dir, timestamp, randomstamp, file_data.name )
    msg_data['msg_content'] = new_file_name  # 拼接文件路径和名称

    print(new_file_name)

    recv_size = 0
    # 写入文件保存到user_home_dir目录
    with open(new_file_name,'wb+') as new_file_item:
        for chunk in file_data.chunks():
            new_file_item.write(chunk)
            recv_size += len(chunk)
            cache.set(file_data.name, recv_size)

    return HttpResponse(json.dumps({'filename': new_file_name}))

def get_file_upload_progress(request):
    filename = request.GET.get('filename')
    progress = cache.get(filename)
    print("file[%s] uploading progress [%s]" %(filename, progress))
    return HttpResponse(json.dumps({'recv_size': progress}))


def delete_cache_key(request):
    cache_key = request.GET.get('cache_key')
    cache.delete(cache_key)
    return HttpResponse('---- cache_key deleted success ----')

def config_phone(request):
    print("Starting config phone...")
    request_method_api = request.POST.get('request_method_api')  # 请求的method api
    logfile = '%s.log' %(request.POST.get('filename'))
    config_yaml_file = os.path.dirname(os.path.realpath(__file__)) + '/utils/config_file.yaml'
    if request_method_api:  #
        request_data_dict = acs_script.get_excel('%s' % (request.POST.get('filename')))  # 获取excel数据转换成字典
        with open(logfile, 'w+') as file:
            for j in request_data_dict:
                try:
                    request_data_dict_row = request_data_dict.get(j)  # 每一行的excel中数据
                    IP = request_data_dict_row.get('IP')
                    if IP:
                        print(IP)
                        with open(config_yaml_file, encoding='utf-8') as f:
                            yaml_dict = yaml.load(f)  # config_file.yaml所有的信息
                        # print(yaml_dict)
                        sipinfo_dict = acs_script.sipinfo_method_dict(request_data_dict_row, yaml_dict, request_method_api)
                        # print(sipinfo_dict)
                        request_url_dict = acs_script.get_request_url(request_data_dict_row, sipinfo_dict)  # 获取请求的api
                        request_url, error_code = request_url_dict.get('request_url'), request_url_dict.get('error_code')
                        isrepeat, extension = request_url_dict.get('isrepeat'), request_url_dict.get('extension')
                        # print(request_url)
                        if request_url:
                            reqeust_obj_stdout = acs_script.request_exec_command(request_url)  # 执行 request_exec_command
                            logcontent = acs_script.request_logcontent(reqeust_obj_stdout, IP, isrepeat, extension)  # 返回执行结果匹配
                        else:
                            code_info = acs_script.code_info(error_code)
                            logcontent = "%s  Error Code:  %s,  %s" % (IP, error_code, code_info)
                except:
                    logcontent = "配置异常，请反馈系统管理员..."
                finally:
                    file.write(logcontent + '\n')
        with open(logfile, 'r+') as f:
            log_all_content = f.read()
        return HttpResponse(log_all_content)
    return HttpResponse("未检测到正确的请求类型.......")

def logfile(request, logfile):
    logfile = "media/%s" %(logfile)
    # print(logfile)
    if os.path.exists(logfile):
        with open(logfile, 'r+') as f:
            logallcontent = f.read()
    else:
        logallcontent = "未查询到该日志..."
    # return render(request, 'NeuBoard/test.html', {'logallcontent': logallcontent,
    #
    #                                                   })
    return render(request, 'NeuBoard/genieacs-log.html', {'logallcontent': logallcontent,})



def excel_export(request):
    print('excel export started ...')
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H%M%S')
    search_conditions = {}
    sortstr = [("Device.LAN.IPAddress._value", 1)]
    # 连接mongodb
    client = pymongo.MongoClient(Mongodb_IP, 27017)
    db = client.genieacs
    collection = db.devices
    genieacs_list = collection.find(search_conditions, {"Device.LAN.IPAddress": 1, "Device.LAN.MACAddress": 1,
                                                        "Device.DeviceInfo.ProductClass": 1, "Device.DeviceInfo.SoftwareVersion":1, "VirtualParameters": 1,
                                                        "_lastInform": 1, "_lastBootstrap": 1, "_lastBoot": 1,
                                                        "Device.DeviceInfo.UpTime": 1}).sort(sortstr)
    total_count = genieacs_list.count()

    # 获取PositionsRelation
    positions_obj = models.PositionsRelation.objects.all().values()
    positions_data = {}
    for i in positions_obj:
        if i['ip']:
            positions_data[i['ip']] = i['position']

    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
                         num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    style_heading = xlwt.easyxf("""
                font:
                    name Arial,
                    colour_index white,
                    bold on,
                    height 0xA0;
                align:
                    wrap off,
                    vert center,
                    horiz center;
                pattern:
                    pattern solid,
                    fore-colour 0x19;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)

    wb = xlwt.Workbook()
    ws = wb.add_sheet('分机信息')

    title_list = ["ID", "日期", "运行时长(天)", "型号", "固件版本", "IP地址", "MAC地址", "SIP1分机号", "SIP1状态", "SIP1注册地址", "SIP1出局",
                  "SIP2分机号", "SIP2状态", "SIP2注册地址", "SIP2出局", "工位"]
    device_parameters_list = ["_id", "_lastInform", "Device.DeviceInfo.UpTime", "Device.DeviceInfo.ProductClass",
                              "Device.DeviceInfo.SoftwareVersion", "Device.LAN.IPAddress", "Device.LAN.MACAddress"]
    sip1_parameters_list = ["VirtualParameters.SIP1", "VirtualParameters.SIP1 Status",
                            "VirtualParameters.SIP1 RegistrarServer",  "VirtualParameters.SIP1 OutboundProxy"]
    sip2_parameters_list = ["VirtualParameters.SIP2", "VirtualParameters.SIP2 Status",
                            "VirtualParameters.SIP2 RegistrarServer",  "VirtualParameters.SIP2 OutboundProxy" ]
    parameters_list = device_parameters_list + sip1_parameters_list + sip2_parameters_list
    for x in range(len(title_list)):
        ws.write(0, x, title_list[x], style_heading)
        ws.col(0).width = 256 * 35
    for item in enumerate(genieacs_list):
        for i in enumerate(parameters_list):
            # print(i[1])
            col = item[0]+1
            row = i[0]
            value = get_excel.get_excel_value(i[1], item[1])
            if i[1] == "_lastInform":
                value = custom.nowtime(value, 'datetime')
            if i[1] == "Device.DeviceInfo.UpTime":
                runtime = custom.sec2time(value, 'day')
                value = runtime
            if i[1] == "Device.LAN.IPAddress":
                ip = value
                position = positions_data.get(ip)
            if i[1] == "Device.LAN.MACAddress":
                value = custom.parsemac(value)
            ws.write(col, row, value)
            ws.col(row).width = 256 * 18
        ws.write(col+1, row+1, position)
        ws.col(row+1).width = 256 * 18

    filename = '%s_genieacs.xls' %now_time
    wb.save(filename)
    sio = BytesIO()
    wb.save(sio)
    sio.seek(0)
    return HttpResponse(filename)
    # response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename=%s_genieacs.xls' %now_time
    # response.write(sio.getvalue())
    # return response

def download_excel(request, filename):
    from django.http import StreamingHttpResponse
    def file_iterator(file_name, chunk_size=512):  # 用于形成二进制数据
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = filename
    print(the_file_name)
    print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/' + the_file_name)
    response = StreamingHttpResponse(file_iterator(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/' + the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response

def check_ping(request):

    IP = request.POST.get('IP')
    print('%s Ping Started...' %IP)
    ping_command = "ping -w 1 -i 0.2 -c 3 %s" % IP

    ping_obj = subprocess.Popen([ping_command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    try:
        ping_obj.wait(3)
        ping_obj_stdout = ping_obj.stdout.read().decode('utf-8')
        # print('ping result', ping_obj_stdout)
    except:
        print('except')
        ping_obj_stdout = "%s    Network Faild" %IP
    # ping_result = "<p>正在检测 %s 网络...</p>" %IP
    return HttpResponse(ping_obj_stdout)

def multishow(request):
    multilist = ""
    if request.method == "POST":
        multilist = request.POST.get('multishow')
    response = HttpResponse(multilist)
    return response

def pagenumper(request):
    pagenumper = 100
    if request.method == "POST":
        pagenumper = request.POST.get('pagenumper')
    response = HttpResponse()
    response.set_cookie('pagenumper', pagenumper)
    return response

def check_area(request):

    if request.method == "POST":
        area = request.POST.get('area')
        response = HttpResponse()
        response.set_cookie('area', area)
    else:
        response = HttpResponse('')
    return response

def wakeup(request):
    from Info.utils import redishelper
    redishelper = redishelper.RedisHelper()
    iplist = ""
    if request.method == "POST":
        print(request.POST.get('wakeup'))
        iplist = request.POST.get('wakeup').split('\n')
        print(iplist)
        redishelper.publish(iplist)
    return HttpResponse(iplist)

def reboot_phone(request):
    device_id = request.POST.get('device_id')
    device_ip = request.POST.get('device_ip')
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
    return HttpResponse(logcontent)


def delete(request):
    # from bson import json_util as jsonb
    if request.method == "POST":
        device_id = request.POST.get('device_id')
        device_ip = request.POST.get('device_ip')
        if device_id:
            print(device_id)
            try:
                client = pymongo.MongoClient(Mongodb_IP, Port)
                db = client.genieacs
                collection = db.devices
                # result = collection.find({'_id': "000B82-GXP1625-000b82d465d5"})

                # result = collection.delete_one({"_id": "000B82-GXP1625-000b82d465d5"} )
                result = collection.delete_one({"_id": "%s" %device_id} )
                print(result)
                # print(jsonb.dumps(result))
                result = "%s  %s Delete  Successful..." %(device_ip, device_id)
            except Exception as e:
                print(e)
                result = "%s  %s  Delete  Faild..." %(device_ip, device_id)

        else:
            device_id =None

        return HttpResponse(result)
    else:
        return HttpResponse('Invaild Operation...')


def test(request):
    from Info import tasks
    res = tasks.add.delay(100,100)
    device_id = "000B82-GXP1625-000b827fd280"
    device_ip = "10.6.39.241"
    # res = tasks.reboot_phone.delay(device_id, device_ip)
    task_id = res.task_id
    print('res: ', res)
    return HttpResponse(task_id)
