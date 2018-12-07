from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

# Create your views here.
from webchat import models
import queue,json,time,os,time,random,threading

GLOBAL_MSG_QUEUES ={}
threads = []

@login_required
def dashboard(request):

    return render(request, 'webchat/dashboard.html')

def get_ping_result(request):
    with open('media/test.log', 'r') as fdout:
        ping_result = json.dumps(fdout.readlines())
    print(type(ping_result))
    print(ping_result)
    return HttpResponse(ping_result)

@login_required
def send_msg(request):
    print(request.POST.get("data"))
    #if request.POST.get()
    msg_data = request.POST.get('data')
    msg_data = json.loads(msg_data)  # 转换成字典格式
    # if msg_data:
    #     msg_data = json.loads(msg_data)
    #     msg_data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     if msg_data['contact_type'] == 'single':
    #         if not GLOBAL_MSG_QUEUES.get(int(msg_data['to']) ):
    #             GLOBAL_MSG_QUEUES[int(msg_data["to"])] = queue.Queue()
    #         GLOBAL_MSG_QUEUES[int(msg_data["to"])].put(msg_data)
    #     else: # group
    #         group_obj = models.WebGroup.objects.get(id=msg_data['to'])
    #         for member in group_obj.members.select_related():
    #             if not GLOBAL_MSG_QUEUES.get(member.id):  # 如果字典里不存在这个用户的queue则创建一个
    #                 GLOBAL_MSG_QUEUES[member.id] = queue.Queue()
    #             if member.id != request.user.userprofile.id:
    #                 GLOBAL_MSG_QUEUES[member.id].put(msg_data)
    # 发送消息添加到队列
    msg_add_queue(msg_data)

    return HttpResponse('---msg recevied---')

# 发送消息添加到队列
def msg_add_queue(msg_data):
    if msg_data:
        # msg_data = json.loads(msg_data)
        msg_data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        received_user_id = msg_data['to_user_id']  # 接收好友或群组id
        send_user_id = msg_data['from_user_id']  # 发送者的id
        msg_type = msg_data['msg_type']
        print(msg_data)

        if msg_data['contact_type'] == "single":
            if not GLOBAL_MSG_QUEUES.get(int(received_user_id)):
                GLOBAL_MSG_QUEUES[int(received_user_id)] = queue.Queue()
            GLOBAL_MSG_QUEUES[int(received_user_id)].put(msg_data)
            to_name = models.UserProfile.objects.get(id=received_user_id).name  # 接收者的name
        else:
            group_obj = models.WebGroup.objects.get(id=received_user_id)  # 通过id获取群组对象
            if group_obj:
                for member in group_obj.members.select_related():
                    if not GLOBAL_MSG_QUEUES.get(member.id):  # 不存在该用户的queue则创建
                        GLOBAL_MSG_QUEUES[member.id] =queue.Queue()
                    if member.id != int(send_user_id):  # member.id 不等于发送者的id则添加消息到队列
                        GLOBAL_MSG_QUEUES[member.id].put(msg_data)
            to_name = group_obj.name  # 接收者的name

        msg_data['to_name'] = to_name
        # 聊天信息写入数据库
        models.WebRecord.objects.create(**msg_data)




def get_new_msgs(request):
    random_num = random.random()
    # threads.append(random_num)
    # print(threads)
    # if len(threads) != 0:  # 存在连接
    #     t = threading.Thread(target=new_msgs, args=(request,random_num))
    #     t.start()
    #     return HttpResponse("OK")
    # else:
    #     return new_msgs(request, random_num)
    return new_msgs(request, random_num)



def new_msgs(request,random_num):
    print('new_msgs')
    userid = request.user.userprofile.id
    if userid not in GLOBAL_MSG_QUEUES:  # 如不存在该用户对应的queue则创建
        print("no queue for user [%s]" %userid,request.user)
        GLOBAL_MSG_QUEUES[userid] = queue.Queue()
    msg_count = GLOBAL_MSG_QUEUES[userid].qsize()  # 该queue中的消息数量
    q_obj = GLOBAL_MSG_QUEUES[userid]  # 该queue对象
    msg_list = []
    random_num = random_num
    print(random_num)
    if msg_count >0 and random_num:

        for msg in range(msg_count):
            msg_list.append(q_obj.get())

        print("new msgs:",msg_list)
    else:  # 没消息,要挂起
        # print("no new msg for ",request.user,request.user.userprofile.id)
        # print(GLOBAL_MSG_QUEUES)
        try:
            msg_list.append(q_obj.get(timeout=60))
        except queue.Empty:
            print("\033[41;1mno msg for [%s][%s] ,timeout\033[0m" %(userid,request.user))


    return HttpResponse(json.dumps(msg_list))


def file_upload(request):
    # file_obj = request.FILES
    file_data = request.FILES.get('file_data')
    msg_data = request.POST.get('msg_data')  #当前获取到的type为string
    msg_data = json.loads(msg_data)  # 转换成字典格式
    msg_data['msg_content'] = file_data.name
    user_home_dir = "media/images/uploads/%s" % request.user.userprofile.id
    if not os.path.isdir(user_home_dir):
        os.mkdir(user_home_dir)
    new_file_name = "%s/%s" % (user_home_dir, file_data.name)
    msg_data['msg_content'] = new_file_name  # 拼接文件路径和名称

    recv_size = 0
    # 写入文件保存到user_home_dir目录
    with open(new_file_name,'wb+') as new_file_item:
        for chunk in file_data.chunks():
            new_file_item.write(chunk)
            recv_size += len(chunk)
            cache.set(file_data.name, recv_size)

    if file_data.size == recv_size:  # 当文件size和写入文件recv_size相等时
        # 发送消息添加到队列
        msg_add_queue(msg_data)

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