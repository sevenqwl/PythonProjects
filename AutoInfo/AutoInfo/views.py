#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
            # request.session.set_expiry(86400)
            return HttpResponseRedirect(request.GET.get('next') or '/info/genieacs')
        else:
            login_err = "Wrong username or password!"
            print(login_err)
            return render(request, 'login.html', {'login_err': login_err})

    return render(request, 'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def dashboard(request):
    return HttpResponseRedirect('/info/index')

def genieacs(request):
    return HttpResponseRedirect('/info/genieacs')