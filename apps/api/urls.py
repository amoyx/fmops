from django.conf.urls import url

from .views import assets_api, deploy_api, users_api, koderover_api, order_api, tencentcloud_api
from django.urls import path, re_path
from rest_framework.authtoken import views


urlpatterns = [
    path('project/', assets_api.project_list),
    re_path('project/(?P<id>[0-9]+)/', assets_api.project_detail),
    path('koderover/', koderover_api.koderover_list),
    re_path('koderover/(?P<id>[0-9]+)/', koderover_api.koderover_detail),
    path('koderover/deploy/', koderover_api.koderover_deploy),
    path('deploy/run/', deploy_api.deploy_run),
    path('deploy/rollback/', deploy_api.deploy_rollback),
    path('deploy/job/status/<str:action>/<int:task_id>/', deploy_api.get_job_full_status),
    path('deploy/stage/status/<str:action>/<int:task_id>/<int:stage_id>/',deploy_api.get_job_stage_status),
    path('user/group/', users_api.group_list),
    path('user/register/', users_api.register),
    path('user/<int:id>/',users_api.user_detail),
    path('server/', assets_api.server_list),
    path('server/<int:id>/', assets_api.server_detail),
    path(r'token/', views.obtain_auth_token),
    re_path('order/search/(?P<id>[0-9]+)/', order_api.orders_search),
    path('tencentcloud/os/image/region/<str:region>/platform/<str:platform>/',tencentcloud_api.os_image_search),
    path('tencentcloud/security/group/region/<str:region>/',tencentcloud_api.search_security_groups),
    path('tencentcloud/security/policies/region/<str:region>/secid/<str:secid>/',tencentcloud_api.search_security_policies),
    path('tencentcloud/network/vpc/region/<str:region>/',tencentcloud_api.search_vpc_network),
    path('tencentcloud/subnet/region/<str:region>/vpcid/<str:vpcid>/zone/<str:zone>/',tencentcloud_api.search_vpc_subnet),
    path('tencentcloud/zone/region/<str:region>/',tencentcloud_api.search_zone_available),
    path('tencentcloud/cvm/instances/run/',tencentcloud_api.cvm_instances_run),
]
