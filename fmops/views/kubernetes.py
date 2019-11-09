#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from fmops import settings
from apps.api.views.kubernetes_api import kubeAPI


@login_required(login_url='/login')
def namespace_list(request):
    api = '%s/api/v1/namespace' % settings.KUBERNETES_API
    try:
        list_data = requests.get(api).json()
    except Exception as ex:
        list_data = False
        return render(request, 'error/500.html', {"error_info": " 请求超时，请检查URL是否有问题 %s " % str(ex)})
    return render(request, 'kubernetes/namespace_list.html', {"user": request.user, "listData": list_data})


@login_required(login_url='/login')
def deployment_list(request, namespace):
    api = '%s/api/v1/deployment/%s/' % (settings.KUBERNETES_API, namespace)
    try:
        list_data = requests.get(api).json()
    except Exception as ex:
        list_data = {}
        return render(request, 'error/500.html', {"error_info": " 请求超时，请检查URL是否有问题 %s " % str(ex)})
    return render(request, 'kubernetes/deployment_list.html', {"user": request.user,
                                                               "namespace": namespace,
                                                               "listData": list_data})


@login_required(login_url='/login')
def pod_list(request, namespace, deployment):
    k = kubeAPI()
    data = {
            'pod_list': k.kube_pod_list(namespace, deployment),
            'history_data': k.kube_history(namespace, deployment),
            'event_data': k.kube_event(namespace, deployment),
            'detail_data': k.kube_detail(namespace, deployment)
        }
    return render(request, 'kubernetes/deployment_detail.html', {"user": request.user,
                                                        "namespace": namespace,
                                                        "deployment": deployment,
                                                        "listData": data})


@login_required(login_url='/login')
def deployment_detail(request):
    api = 'http://172.16.13.208:8080'
    return render(request, 'kubernetes/deployment_detail.html', {"user": request.user})

