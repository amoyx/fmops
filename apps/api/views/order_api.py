#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from rest_framework.decorators import api_view
import json
from apps.orders.models import Order_System
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def orders_search(request, id, format=None):
    try:
        if request.method == 'POST':
            date_start = request.POST.get('date_start')
            date_end = request.POST.get('date_end')
            order_status = request.POST.get('status', None)
        else:
            date_start = request.GET.get('date_start', None)
            date_end = request.GET.get('date_end', None)
            order_status = request.GET.get('status', None)
        sql = "SELECT id,apps_id,order_name,order_flag,create_user,cost_time,create_time FROM ops_order_system WHERE apps_id=" + id
        if date_start:
            sql += " AND create_time >= '" + date_start + " 00:00:00'"
        if date_end:
            sql += " AND create_time <= '" + date_end + " 24:00:00'"
        if order_status:
            sql += " AND order_flag ='" + str(order_status).strip() + "'"

        dataList = Order_System.objects.raw(sql)
        html_content = "<thead><tr><th>任务ID</th><th data-hide=\"phone\">任务名称</th>" \
                       "<th data-hide=\"phone\">执行用户</th>" \
                       "<th data-hide=\"phone\">创建时间</th>" \
                       "<th data-hide=\"phone,tablet\" >花费时间</th> " \
                        "<th data-hide=\"phone\">执行结果</th>" \
                        "<th class=\"text-right\"></th></tr></thead><tbody>"
        for data in dataList:
            html_content += "<tr><td>{id}</td><td>{name}</td><td>{user}</td><td>{time}</td><td>{cost}</td><td>".format(
                                                                                    id=str(data.id),
                                                                                    name=data.order_name,
                                                                                    user=data.create_user,
                                                                                    time=data.create_time,
                                                                                    cost=data.cost_time)
            if data.order_flag == "SUCCESS":
                html_content += "<td><span class='label label-success'>SUCCESS</span></td>"
            elif data.order_flag == "FAIL":
                html_content += "<td><span class='label label-danger'>FAIL</span></td>"
            else:
                html_content += "<td><span class='label label-warning'>Pending</span></td>"
            html_content += "<td class='text-right'><div class='btn-group'><button class='btn-success btn btn-xs' " \
                            "onclick=\"showOrderLogInfo('{id}')\" data-api=\"/order/detail/\" " \
                            "style=\"padding: 0px 15px;font-weight: bold\">日志</button></div></td></tr>".format(id=data.id)
        html_content += "</tbody><tfoot><tr><td colspan=\"7\">" \
                        "<ul class=\"pagination pull-right\"></ul></td></tr></tfoot>"
        return Response(html_content)
    except Exception as e:
        return Response(str(e))

