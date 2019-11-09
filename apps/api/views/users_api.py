#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from rest_framework import status
from django.http import Http404
from django.contrib.auth.models import Group,User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from apps.api import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


@api_view(['GET', 'POST'])
def user_list(request,):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':
        snippets = User.objects.all()
        serializer = serializers.UserSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def group_list(request):
    """
    List all order, or create a server assets order.
    """
    # if not request.user.has_perm('Opsmanage.read_group'):
    #     return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        snippets = Group.objects.all()
        serializer = serializers.GroupSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # if not  request.user.has_perm('Opsmanage.change_group'):
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.filter(username=request.POST.get('username'))
                if len(user)>0:return JsonResponse({"code": 500, "data":None, "msg": "注册失败，用户已经存在。"})
                else:
                    user = User()
                    user.username = request.POST.get('username')
                    user.email = request.POST.get('email')
                    user.first_name = request.POST.get('first_name')
                    user.is_staff = 0
                    user.is_active = 0
                    user.is_superuser = 0
                    user.set_password(request.POST.get('password'))
                    user.save()
                    token = Token.objects.create(user=user)
                    return JsonResponse({"code":200,"data": token.key, "msg": "用户注册成功"})
            except Exception as e:
                return JsonResponse({"code":500, "data": None,"msg":"用户注册失败, "+str(e)})
        else:return JsonResponse({"code":500, "data": None, "msg": "密码不一致，用户注册失败。"})


@api_view(['GET', 'POST', 'DELETE'])
def user_detail(request, id):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.UserSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.delete_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def user_update_password(request):
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.get(username=request.user)
                user.set_password(request.POST.get('password'))
                user.save()
                return JsonResponse({"code": 200, "data": None, "msg":"密码修改成功"})
            except Exception as e:
                return JsonResponse({"code": 500, "data": None, "msg":"密码修改失败：%s" % str(e)})
        else:
            return JsonResponse({"code": 500, "data": None, "msg": "密码不一致，密码修改失败。"})
