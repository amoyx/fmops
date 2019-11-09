#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from rest_framework.decorators import api_view
from apps.api import serializers
from apps.assets.models import *
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
from fmops import settings
from django.contrib.auth.decorators import permission_required
import json


@api_view(['GET', 'POST' ])
def project_list(request,format=None):
    if request.method == 'GET':
        snippets = Project_Assets.objects.all()
        serializer = serializers.ProjectSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            apps_id = json.loads(request.body).get('apps_id')
        except Exception as ex:
            apps_id = request.POST.get('apps_id', None)
        try:
            snippet = Project_Assets.objects.get(apps_id=apps_id)
            if snippet:
                serializer = serializers.ProjectSerializer(snippet)
                return Response(serializer.data)
        except Exception as ex:
            pass
            print(str(ex))
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def project_detail(request, id, format=None):
    try:
        snippet = Project_Assets.objects.get(id=id)
    except Project_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ProjectSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.ProjectSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                if serializer.data.get('project_kube_namespace',None) and serializer.data.get('project_kube_service',None):
                    api = '%s/api/v1/publish/fmServices/notify/%s' % (settings.DEPLOY_PLATFORM_HOST,serializer.data.get('apps_id'))
                    print(requests.get(api).content)
            except Exception as e:
                print(str(e))
                pass
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            data=json.loads(request.body)
        except Exception as ex:
            data=request.POST
        try:
            serializer = serializers.ProjectSerializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"code": 500, "data": str(e), "msg": "项目更新失败"})

    elif request.method == 'DELETE':
        if not request.user.has_perm('fmops.can_delete_project_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST' ])
def server_list(request,format=None):
    if request.method == 'GET':
        snippets = Server_Assets.objects.all()
        serializer = serializers.ServerSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST','DELETE'])
@permission_required('fmops.can_change_server_assets',raise_exception=True)
def server_detail(request, id):
    try:
        snippet = Server_Assets.objects.get(id=id)
    except Server_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ServerSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.ServerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('fmops.can_delete_server_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
