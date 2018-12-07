from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.core.cache import cache


from Info import models
import xlwt
from io import StringIO, BytesIO
from datetime import datetime
from math import floor, ceil
import json
import pymongo
import re
import os, queue, subprocess, time, random
from Info.utils import acs_script

MONGODB_IP = "10.6.0.149"
list_pagenum = [1, 2, 3, 4, 5]

# Create your views here.
def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        user = "seven"
        # user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print(user)
        print('xxxxx')
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or 'NeuBoard/genieacs.html')
        else:
            login_err = "Wrong username or password!"
            print(login_err)
            return render(request, 'login.html', {'login_err': login_err})

    return render(request, 'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('NeuBoard/index.html')


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


def index(request):
    return render(request, 'NeuBoard/index.html')


def ui_buttons(request):
    return render(request, 'NeuBoard/ui-buttons.html')

def ui_icons(request):
    return render(request, 'NeuBoard/ui-icons.html')

def extensions(request):
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


def genieacs(request):
    regip = get_client_ip(request)  # 获取用户IP地址

    pagenumper = request.GET.get('pagenumper')
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
    print(skip_num)

    search_keywords = request.GET.get('search_keywords')
    if search_keywords is None:
        search_conditions = {}
    else:
        parameters_list = ["_lastInform", "Device.LAN.IPAddress","Device.LAN.MACAddress", "VirtualParameters.SIP1", "VirtualParameters.SIP1 Status", "VirtualParameters.SIP1 RegistrarServer", "VirtualParameters.SIP2", "VirtualParameters.SIP1 Status", "VirtualParameters.SIP2 RegistrarServer"]
        conditions_list = []
        for i in parameters_list:
            parameters_value_str = {i + "._value": re.compile(search_keywords.strip(), re.I)}
            conditions_list.append(parameters_value_str)
        search_conditions = {"$or": conditions_list}
    print(search_conditions)

    client = pymongo.MongoClient(MONGODB_IP, 27017)
    db = client.genieacs
    collection = db.devices
    genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "VirtualParameters": 1, "_lastInform": 1}).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
    total_count = genieacs_list.count()
    num_pages = ceil(total_count / pagenumper)
    return render(request, 'NeuBoard/genieacs.html', {'genieacs_list':genieacs_list,
                                                        'page': page,
                                                        'total_count': total_count,
                                                        'num_pages': num_pages,
                                                        'list_pagenum': list_pagenum,
                                                        'id_num': skip_num,
                                                        })


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
# def genieacs_search(request):
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
#     print(skip_num)
#
#     search_keywords = request.GET.get('search_keywords')
#     if search_keywords is None:
#         search_conditions = {}
#     else:
#         parameters_list = ["_lastInform", "Device.LAN.IPAddress","Device.LAN.MACAddress", "VirtualParameters.SIP1", "VirtualParameters.SIP1 Status", "VirtualParameters.SIP1 RegistrarServer", "VirtualParameters.SIP2", "VirtualParameters.SIP1 Status", "VirtualParameters.SIP2 RegistrarServer"]
#         conditions_list = []
#         for i in parameters_list:
#             parameters_value_str = {i + "._value": re.compile(search_keywords.strip(), re.I)}
#             conditions_list.append(parameters_value_str)
#         search_conditions = {"$or": conditions_list}
#     print(search_conditions)
#
#     client = pymongo.MongoClient(MONGODB_IP, 27017)
#     db = client.genieacs
#     collection = db.devices
#     genieacs_list = collection.find(search_conditions ,{"Device.LAN.IPAddress":1, "Device.LAN.MACAddress":1, "VirtualParameters": 1, "_lastInform": 1}).sort([("Device.LAN.IPAddress._value", 1)]).skip(skip_num).limit(pagenumper)
#     total_count = genieacs_list.count()
#     num_pages = ceil(total_count / pagenumper)
#     return render(request, 'NeuBoard/genieacs.html', {'genieacs_list':genieacs_list,
#                                                         'page': page,
#                                                         'total_count': total_count,
#                                                         'num_pages': num_pages,
#                                                         'list_pagenum': list_pagenum,
#                                                         'id_num': skip_num,
#                                                         })


def file_upload(request):
    # file_obj = request.FILES
    file_data = request.FILES.get('file_data')
    msg_data = request.POST.get('msg_data')  #当前获取到的type为string
    msg_data = json.loads(msg_data)  # 转换成字典格式
    media_home_dir = "media"
    print(media_home_dir)
    if not os.path.isdir(media_home_dir):
        os.mkdir(media_home_dir)
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
    randomstamp = random.randint(1000,9999)
    new_file_name = "%s/%s_%s_%s" % (media_home_dir, timestamp, randomstamp, file_data.name )
    msg_data['msg_content'] = new_file_name  # 拼接文件路径和名称

    print(new_file_name)

    recv_size = 0
    # 写入文件保存到user_home_dir目录
    with open(new_file_name,'wb+') as new_file_item:
        for chunk in file_data.chunks():
            new_file_item.write(chunk)
            recv_size += len(chunk)
            cache.set(file_data.name, recv_size)

    return HttpResponse(json.dumps({'filename': file_data.name}))

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
    request_data_dict = acs_script.get_excel('%s' %(request.POST.get('filename')))
    print(request.POST.get('filename'))

    for j in request_data_dict:
        print(request_data_dict[j])
        REQUEST_SET_API = acs_script.request_api(request_data_dict[j])
        print(REQUEST_SET_API)
        if REQUEST_SET_API:
            REQUEST_COMMAND = 'curl -i %s' % REQUEST_SET_API
            REQUEST_OBJ = subprocess.Popen([REQUEST_COMMAND], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            REQUEST_OBJ_STDOUT = REQUEST_OBJ.stdout.read().decode('utf-8')
            if "HTTP/1.1 200 OK" in REQUEST_OBJ_STDOUT:
                print("%s   HTTP/1.1 200 OK" % request_data_dict[j]['IP'])
            elif "HTTP/1.1 202 Task queued but not processed" in REQUEST_OBJ_STDOUT:
                print("%s   HTTP/1.1 202 Task queued but not processed" % request_data_dict[j]['IP'])
            else:
                print(REQUEST_OBJ_STDOUT)
        else:
            print("%s   REQUEST_SET_API is None" % request_data_dict[j]['IP'])
    else:
        print("Excel data is None!!!")

    return HttpResponse(1)

def excel_export(request):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
                         num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')

    ws.write(0, 0, 1234.56, style0)
    ws.write(1, 0, datetime.now(), style1)
    ws.write(2, 0, 1)
    ws.write(2, 1, 1)
    ws.write(2, 2, xlwt.Formula("A3+B3"))

    wb.save('example.xls')
    sio = BytesIO()
    wb.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xls'
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
        ping_obj_stdout = "Failed"
    # ping_result = "<p>正在检测 %s 网络...</p>" %IP
    return HttpResponse(ping_obj_stdout)