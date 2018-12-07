from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from Info import models

# Create your views here.

def index(request):
    return render(request, 'NeuBoard/index.html')


def ui_buttons(request):
    return render(request, 'NeuBoard/ui-buttons.html')

def elements(request):
    return render(request, 'TID/elements.html')

def extensions(request):
    page = request.GET.get('page')
    print(page)
    page_list = range(20)
    extensions_obj = models.Phoneinfo.objects.all()[:100]
    return render(request, 'NeuBoard/extensions.html', {'extensions_list': extensions_obj, 'page_list': page_list})