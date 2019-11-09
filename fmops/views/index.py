#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.contrib import auth
from django.shortcuts import render


@login_required(login_url='/login')
def index(request):
    return HttpResponseRedirect('/project_list')


def login(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/index', {"user": request.user})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request,user)
            request.session['username'] = username
            return HttpResponseRedirect('/index', {"user": request.user})
        else:
            if request.method == "POST":
                return render(request, 'login.html',{"login_error_info": "用户名不存在，或者密码错误！", "username": username},)
            else:
                return render(request, 'login.html')


# @login_required(login_url='/login')
# def index(request):
#     api = "http://172.16.13.208:8080/api/v1/namespace"
#     try:
#         list_data = requests.get(api).json()
#     except Exception as ex:
#         list_data = False
#         return render(request, 'error/500.html', {"error_info": " 请求超时，请检查URL是否有问题 %s " % str(ex)})
#     return render(request, 'kubernetes/namespace_list.html', {"user": request.user, "listData": list_data})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')


def display_error_500(request):
    return render(request, 'error/500.html', {"error_info": "服务器错误，请检查后端服务器是否异常！"})

