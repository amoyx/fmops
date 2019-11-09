#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from rest_framework.decorators import api_view
from apps.api.serializers import KoderOverSerializer
from apps.koderover.models import *
from apps.orders.models import Order_System
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from utils.jenkins import JenkinsAPI
from apps.koderover.task import recordKodeRover
from django.forms.models import model_to_dict


@api_view(['GET', 'POST' ])
def koderover_list(request,format=None):
    if request.method == 'GET':
        snippets = Koderover_Product.objects.all()
        serializer = KoderOverSerializer(snippets, many=True)
        # return JsonResponse({"code": 500, "data": None, "msg": "Hello world"})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = KoderOverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def koderover_detail(request, id, format=None):
    try:
        snippet = Koderover_Product.objects.get(id=id)
    except Koderover_Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KoderOverSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = KoderOverSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('fmops.can_delete_project_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def koderover_deploy(request):
    """
    koderover 应用发布
    """
    if request.method == 'POST':
        data = request.data
        try:
            koder = Koderover_Product.objects.get(Q(id=data['id']) & Q(service_name=data['service_name']))
            order = Order_System.objects.create(apps_id=koder.id,
                                                order_name='%s-%s 项目服务部署' % (koder.product_name,koder.service_name),
                                                order_flag='PENDING',
                                                create_user=request.user)
            recordKodeRover.delay(order.id,
                                  koder.product_name,
                                  koder.service_name,
                                  koder.kube_namespace,
                                  koder.kube_deployment)
            return JsonResponse({"code": 200, 'msg': 'SUCCESS'})
        except Exception as ex:
            return JsonResponse({'code': 404, 'msg': str(ex)})


