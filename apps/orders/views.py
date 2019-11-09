from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.koderover.models import Koderover_Product
from apps.orders.models import Order_System, Order_Log
from django.http import JsonResponse


@login_required(login_url='/login')
def order_list(request, id):
    orders = Order_System.objects.filter(apps_id=id).order_by("-create_time")
    return render(request,
                  'orders/order_list.html',
                  {"user": request.user, "orders": orders, "id": id})


@login_required(login_url='/login')
def order_detail(request):
    return render(request,
                  'orders/order_detail.html',
                  {"user": request.user})


@login_required(login_url='/login')
def order_stage(request, id, sid):
    try:
        id = int(id)
        sid = int(sid)
        order = Order_Log.objects.filter(order_id=id).order_by('id')
    except Exception as e:
        return JsonResponse({'code': 400, 'status': 'FAIL', 'msg': str(e)})
    if order.count() > sid:
        task = order[sid:sid+1]
        return JsonResponse({'code': 200, 'status': task[0].stage_status, 'msg': task[0].stage_log})
    else:
        return JsonResponse({'code': 202, 'status': 'PENDING', 'msg': ''})
