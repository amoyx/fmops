#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from rest_framework.decorators import api_view
from utils.tencentcloud import Tencent_Cloud_NetWork, Tencent_Cloud_CVM
from django.http import JsonResponse
import json


@api_view(['GET', 'POST'])
def os_image_search(request, region, platform):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':
        try:
            cvm = Tencent_Cloud_CVM()
            data = cvm.get_os_image_list(region, platform)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': data})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": "query data error"+str(e), 'data': []})


@api_view(['GET', 'POST'])
def search_security_groups(request, region):
    if request.method == 'GET':
        try:
            net = Tencent_Cloud_NetWork()
            data = net.describe_security_groups(region)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': data})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": "query data error"+str(e), 'data': []})


@api_view(['GET','POST'])
def search_security_policies(request, region, secid):
    if request.method == 'GET':
        try:
            net = Tencent_Cloud_NetWork()
            data = net.describe_security_group_policies(region, secid)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': data})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": "query data error"+str(e), 'data': []})


@api_view(['GET', 'POST'])
def search_vpc_network(request, region):
    if request.method == 'GET':
        try:
            net = Tencent_Cloud_NetWork()
            data = net.describe_vpc_request(region)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': data['VpcSet']})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": "query data error"+str(e), 'data': []})


@api_view(['GET', 'POST'])
def search_vpc_subnet(request, region, vpcid, zone):
    if request.method == 'GET':
        try:
            net = Tencent_Cloud_NetWork()
            data = net.describe_subnet_request(region, vpcid, zone)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': data})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": "query data error"+str(e), 'data': []})


@api_view(['GET', 'POST'])
def search_zone_available(request, region):
    if request.method == 'GET':
        try:
            net = Tencent_Cloud_CVM()
            data = net.describe_zone_request(region)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': data})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": "query data error"+str(e), 'data': []})


@api_view(['GET', 'POST'])
def cvm_instances_run(request):
    if request.method == 'POST':
        try:

            data = request.data.copy()
            if int(data['InternetMaxBandwidthOut']) < 1: data['InternetMaxBandwidthOut'] = 1
            data['PublicIpAssigned'] = True if data['PublicIpAssigned'] == 'true' else False
            cvm = Tencent_Cloud_CVM()
            result = cvm.run_instances_request(data)
            return JsonResponse({"code": 200, "status": "SUCCESS", "messages": "query data success", 'data': result})
        except Exception as e:
            return JsonResponse({"code": 500, "status": "FAIL", "messages": str(e), 'data': []})
