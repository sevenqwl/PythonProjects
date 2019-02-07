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
from Info.utils import acs_script, get_excel
import pytz
import yaml


MONGODB_IP = "10.6.0.149"
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
    client = pymongo.MongoClient(MONGODB_IP, 27017)
    db = client.genieacs
    collection = db.devices

    search_conditions = {}
    sortstr = [("Device.LAN.IPAddress._value", 1)]
    repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value', 'count': {'$sum': 1}}},
                                        {'$match': {'count': {'$gt': 1}}},
                                        {'$sort': {'_id': 1}}
                                        ])
    repeat_list_count = 0
    for j in repeat_list:
        if j.get('_id'):
            # print(j)
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
            search_conditions = {"$or": conditions_list}
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
                    search_conditions = {"$or": conditions_list}
            elif searchtype=="repeat_list":
                # now_time = datetime.datetime.now()
                # yes_time = now_time + datetime.timedelta(days=-1)
                # print(yes_time)
                # utc_tz = pytz.timezone('UTC')
                # yes_time_utc = yes_time.now(tz=utc_tz)
                # print(yes_time_utc)
                intime = request.GET.get('intime')
                try:
                    inhours = 0-int(intime)
                except:
                    inhours = 0
                now_time = datetime.datetime.utcnow()
                yes_time = now_time + datetime.timedelta(hours=inhours)
                repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value', 'count': {'$sum': 1}}},
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
                pagenumper = 5000




                for i in parameters_list:
                    for j in repeat_list:
                        if j.get('_id'):
                            # print(j)
                            # repeat_list_count += 1
                            parameters_value_str = {i + "._value": j.get('_id').strip()}
                            conditions_list.append(parameters_value_str)
                if request.GET.get('intime'):
                    # print(yes_time)
                    search_conditions = {"$and":[{"$or": conditions_list}, {"_lastInform":{"$gt": yes_time}}]}
                else:
                    search_conditions = {"$or": conditions_list}
                # print(conditions_list)

    # print(search_conditions)
    # print(repeat_list)
    # print('genieacs_list start')
    # print(search_conditions)
    repeat_list = collection.aggregate([{'$group': {'_id': '$VirtualParameters.SIP1._value', 'count': {'$sum': 1}}},
                                        {'$match': {'count': {'$gt': 1}}},
                                        {'$sort': {'_id': 1}}
                                        ])
    # genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "Device.DeviceInfo.ProductClass":1, "VirtualParameters": 1, "_lastInform": 1}).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
    genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "Device.DeviceInfo.ProductClass":1, "Device.DeviceInfo.SoftwareVersion":1, "VirtualParameters": 1, "_lastInform": 1}).sort(sortstr).skip(skip_num).limit(pagenumper)
    # print(genieacs_list)
    total_count = genieacs_list.count()
    num_pages = ceil(total_count / pagenumper)
    # print('genieacs_list end')

    # 获取PositionsRelation
    positions_obj = models.PositionsRelation.objects.all().values()
    # positions_data = serializers.serialize("json", positions_obj)
    # positions_data = model_to_dict(positions_obj)
    positions_data = {}
    #

    for i in positions_obj:
        positions_data[i['ip']] = i['position']
    # print(positions_data)
    return render(request, 'NeuBoard/genieacs.html', {'genieacs_list':genieacs_list,
                                                        'page': page,
                                                        'total_count': total_count,
                                                        'num_pages': num_pages,
                                                        'list_pagenum': list_pagenum,
                                                        'id_num': skip_num,
                                                        'positions_data': positions_data,
                                                        'repeat_list': repeat_list,
                                                        'repeat_list_count': repeat_list_count,
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
#     client = pymongo.MongoClient(MONGODB_IP, 27017)
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
                        sipinfo_dict = acs_script.sipinfo_method_dict(request_data_dict_row, yaml_dict, request_method_api)
                        request_url_dict = acs_script.get_request_url(request_data_dict_row, sipinfo_dict)  # 获取请求的api
                        request_url, error_code = request_url_dict.get('request_url'), request_url_dict.get('error_code')
                        isrepeat, extension = request_url_dict.get('isrepeat'), request_url_dict.get('extension')
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
    print(logfile)
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
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H%M%S')
    search_conditions = {}
    sortstr = [("Device.LAN.IPAddress._value", 1)]
    # 连接mongodb
    client = pymongo.MongoClient(MONGODB_IP, 27017)
    db = client.genieacs
    collection = db.devices
    genieacs_list = collection.find(search_conditions, {"Device.LAN.IPAddress": 1, "Device.LAN.MACAddress": 1,
                                                        "Device.DeviceInfo.ProductClass": 1, "Device.DeviceInfo.SoftwareVersion":1, "VirtualParameters": 1,
                                                        "_lastInform": 1}).sort(sortstr)
    total_count = genieacs_list.count()

    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
                         num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('分机信息')

    title_list = ["ID", "型号", "固件版本", "IP地址", "MAC地址", "SIP1分机号", "SIP1状态", "SIP1注册地址", "SIP1出局",  "SIP2分机号", "SIP2状态", "SIP2注册地址", "SIP2出局"]
    device_parameters_list = ["Device.DeviceInfo.ProductClass", "Device.DeviceInfo.SoftwareVersion", "Device.LAN.IPAddress", "Device.LAN.MACAddress"]
    sip1_parameters_list = ["VirtualParameters.SIP1", "VirtualParameters.SIP1 Status",  "VirtualParameters.SIP1 RegistrarServer",  "VirtualParameters.SIP1 OutboundProxy"]
    sip2_parameters_list = ["VirtualParameters.SIP2", "VirtualParameters.SIP2 Status",  "VirtualParameters.SIP2 RegistrarServer",  "VirtualParameters.SIP2 OutboundProxy" ]
    parameters_list = device_parameters_list + sip1_parameters_list + sip2_parameters_list
    for x in range(len(title_list)):
        ws.write(0, x,title_list[x])
        ws.col(0).width = 256 * 35
    for item in enumerate(genieacs_list):
        # print(item[0], item[1])
        ws.write(item[0]+1, 0, item[1].get('_id'))
        # ws.write(item[0]+1, 1, item[1].get('_lastInform'))
        for i in enumerate(parameters_list):
            ws.write(item[0]+1, i[0]+1, get_excel.get_excel_value(i[1], item[1]))
            # print(item[0]+1, i[0]+1, get_excel.get_excel_value(i[1], item[1]))
            ws.col(i[0]+1).width = 256 * 18

    # wb.save('example.xlsx')
    sio = BytesIO()
    wb.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s_genieacs.xls' %now_time
    response.write(sio.getvalue())
    return response

def check_ping(request):
    print('Ping Started...')
    IP = request.POST.get('IP')
    ping_command = "ping -w 1 -i 0.2 -c 3 %s" % IP

    print(ping_command)
    ping_obj = subprocess.Popen([ping_command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    try:
        print('try')
        ping_obj.wait(3)
        ping_obj_stdout = ping_obj.stdout.read().decode('utf-8')
        print('ping result', ping_obj_stdout)
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