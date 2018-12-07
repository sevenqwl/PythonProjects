from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
import json
from bbs import models
from bbs import form
from bbs import comment_handler


# 全局菜单列表
category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')

def index(request):
    category_obj = models.Category.objects.get(position_index=1)
    article_list = models.Article.objects.filter(status='published')
    return render(request,'bbs/index.html',{'category_list': category_list, 'category_obj':category_obj, 'articel_list': article_list})

# 动态url菜单
def category(request, id):
    category_obj = models.Category.objects.get(id=id)
    if category_obj.position_index == 1: # 首页
        article_list = models.Article.objects.filter(status='published')
    else:
        article_list = models.Article.objects.filter(category_id = category_obj.id, status='published')
    return render(request, 'bbs/index.html', {'category_list': category_list, 'category_obj':category_obj, 'articel_list': article_list})

def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next') or '/bbs')
        else:
            login_err = "Wrong username or password!"
            print(login_err)
            return render(request, 'login.html', {'login_err': login_err})

    return render(request, 'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/bbs')


def article_detail(request, article_id):
    article_obj = models.Article.objects.get(id=article_id)
    category_obj = models.Category.objects.get(position_index=1)
    comment_tree = comment_handler.build_tree(article_obj.comment_set.select_related())

    return render(request, 'bbs/article_detail.html',{'article_obj': article_obj, 'category_obj': category_obj, 'category_list': category_list})

def comment(request):
    print(request.POST)
    if request.method == "POST":
        # 暂未做判断article_id是否存在
        new_comment_obj = models.Comment(
            article_id = request.POST.get('article_id'),
            parent_comment_id = request.POST.get('parent_comment_id') or None,
            comment_type = request.POST.get('comment_type'),
            user_id = request.user.userprofile.id,
            comment = request.POST.get('comment'),
        )
        new_comment_obj.save()
    return HttpResponse('post-comment-success')


def get_comments(request, article_id):
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = comment_handler.build_tree(article_obj.comment_set.select_related())
    tree_html = comment_handler.render_comment_tree(comment_tree)

    return HttpResponse(tree_html)

# @login_required(login_url='/login/')
@login_required()
def new_article(request):

    if request.method == "GET":
        article_form = form.ArticleModelForm()
        return render(request, 'bbs/new_article.html', {'article_form': article_form, 'category_list': category_list})
    elif request.method == "POST":
        print(request.POST)
        article_form = form.ArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            data = article_form.cleaned_data  # cleaned_data 转换成字典格式
            data['author_id'] = request.user.userprofile.id
            article_obj = models.Article(**data)
            article_obj.save()
            article_list = models.Article.objects.filter(status='published')
            return HttpResponse('Published success....')
            # return render(request, 'bbs/index.html',{'category_list': category_list, 'articel_list': article_list})
        else:
            return render(request, 'bbs/new_article.html', {'article_form': article_form, 'category_list': category_list})

# 文件上传方法
def file_upload(request):
    print(request.FILES)
    file_obj = request.FILES.get('filename')
    with open('media/%s' % file_obj.name, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return render(request, 'bbs/new_article.html', {'category_list': category_list})


def get_latest_article_count(request):
    latest_article_id = request.GET.get('latest_id')
    print('latest_article_id', latest_article_id)

    if latest_article_id:
        new_article_count = models.Article.objects.filter(id__gt=latest_article_id).count()

        print("new article count:", new_article_count)
    else:
        new_article_count = 0
    return HttpResponse(json.dumps({'new_article_count': new_article_count}))

