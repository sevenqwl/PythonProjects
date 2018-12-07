from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from Info import models
import xlwt
from io import StringIO, BytesIO
from datetime import datetime
import json

# Create your views here.
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

    return render(request, 'NeuBoard/extensions.html', locals())  # locals() 表示
    # return render(request, 'NeuBoard/extensions.html', {'extensions_list': extensions_list,
    #                                                         'list_pagenum': list_pagenum,
    #                                                         'total_count': total_count,
    #                                                         'num_pages': num_pages,
    #                                                         'online_num': online_num,
    #                                                         'offline_num': offline_num,
    #                                                     })


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