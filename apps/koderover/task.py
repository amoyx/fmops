#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from django.conf import settings
import time, datetime
from .container import KodeRoverObject, KubernetesCluster
from apps.orders.models import Order_Log, Order_System


app = settings.CELERY
# python manage.py celery worker -c 4 --loglevel=info


@app.task
def recordKodeRover(order_id, product_name, service_name, namespace, deployment):
    kode = KodeRoverObject(product_name)
    latest_image = kode.is_publish_image_by_day(service_name)
    first_time = datetime.datetime.now()
    if not latest_image:
        stage_status = 'FAIL'
        stage_log = 'Error: 未找到该 %s 服务的发布镜像' % service_name
    else:
        stage_status = 'SUCCESS'
        stage_log = latest_image
    Order_Log.objects.create(order_id=order_id,
                             stage_name='查找服务发布的最新镜像',
                             stage_status=stage_status,
                             stage_log=stage_log,
                             stage_cost=get_cost_time(first_time))
    if not latest_image:
        Order_System.objects.filter(id=order_id).update(order_flag=stage_status, cost_time=get_cost_time(first_time))
        print("Error: 未找到要发布的镜像 " + get_cost_time(first_time))
        return stage_status

    st = datetime.datetime.now()
    kube = KubernetesCluster(namespace=namespace)
    dep = kube.get_deployment(deployment)
    if not dep:
        stage_status = 'FAIL'
        stage_log = 'Error: 未找到 %s 该服务的deployment信息' % deployment
    else:
        stage_status = 'SUCCESS'
        stage_log = dep

    Order_Log.objects.create(order_id=order_id,
                             stage_name='查找服务kubernetes的deployment信息',
                             stage_status=stage_status,
                             stage_log=stage_log,
                             stage_cost=get_cost_time(st))
    st = datetime.datetime.now()
    if not dep:
        Order_System.objects.filter(id=order_id).update(order_flag=stage_status, cost_time=get_cost_time(st))
        print("Error: 未找到要发布的镜像")
        return stage_status

    try:
        stage_status = 'SUCCESS'
        kube.update_deployment(deployment, latest_image)
        stage_log = ' %s 服务正在更新中，请稍等。。。' % deployment
    except Exception as e:
        stage_status = 'FAIL'
        stage_log = 'Error: 更新 %s 服务错误，%s ' % (deployment, str(e))
    Order_Log.objects.create(order_id=order_id,
                            stage_name='更新kubernetes的deployment',
                            stage_status=stage_status,
                            stage_log=stage_log,
                            stage_cost=get_cost_time(st))
    st = datetime.datetime.now()
    if stage_status == 'FAIL':
        Order_System.objects.filter(id=order_id).update(order_flag=stage_status, cost_time=get_cost_time(st))
        print("Error: 更新deployment失败")
        return stage_status

    wait_time = 120
    while wait_time > 0:
        result = kube.get_deployment_status(deployment)
        time.sleep(2)
        if isinstance(result['status'], dict):
            print('%s 应用服务正在启动中，请稍等 %s ......' % (deployment, str(wait_time)))
            if result['status']['replicas'] == result['status']["readyReplicas"]:
                stage_log = "successfully：%s 服务启动完成" % deployment
                stage_status = 'OK'
                break
        else:
            stage_status = 'FAIL'
            stage_log = "Error：%s 服务启动超时" % deployment
            break
        wait_time -= 1
    Order_Log.objects.create(order_id=order_id,
                            stage_name='检测kubernetes - deployment启动情况',
                            stage_status=stage_status,
                            stage_log=stage_log,
                            stage_cost=get_cost_time(st))
    order_flag = 'FAIL' if stage_status == 'FAIL' else 'SUCCESS'
    Order_System.objects.filter(id=order_id).update(order_flag=order_flag, cost_time=get_cost_time(first_time))
    return order_flag


def get_cost_time(start_time):
    curr_time = datetime.datetime.now()
    return str(curr_time - start_time)
