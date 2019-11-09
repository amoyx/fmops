"""fmops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from fmops.views import index, kubernetes, users
from apps.assets import views
from apps.koderover import views as koder
from django.conf.urls import include
from apps.orders import views as order


urlpatterns = [
    path('', index.index, name='index'),
    path('index/', views.project_list),
    path('admin/', admin.site.urls),
    path(r'login/', index.login, name='login'),
    path(r'logout/', index.logout, name='logout'),
    path(r'kubernetes/namespaces/', kubernetes.namespace_list),
    path(r'api/v1/', include('apps.api.urls')),
    re_path(r'kubernetes/namespaces/(?P<namespace>[0-9a-zA-Z-_]+)/deployments/', kubernetes.deployment_list),
    re_path(r'kubernetes/namespaces/(?P<namespace>[0-9a-zA-Z-_]+)/deployment/(?P<deployment>\S+)/pods/', kubernetes.pod_list),
    path(r'kubernetes/namespaces/deployment/detail/', kubernetes.deployment_detail),
    path(r'error/500/', index.display_error_500, name='error_500'),
    path(r'project_list/', views.project_list, name='project_list'),
    re_path(r'project_modify/(?P<id>[0-9]+)/', views.project_modf, name='project_modf'),
    re_path(r'project_detail/(?P<id>[0-9]+)/', views.project_detail, name='project_detail'),
    path(r'server/add/', views.server_add, name='server_add'),
    path(r'server/list/', views.server_list, name='server_list'),
    path(r'server/modify/<int:id>/', views.server_modf, name='server_modf'),
    path(r'users/manage/', users.user_manage, name='user_manage'),
    path(r'users/center/<int:uid>/', users.user_center),
    path(r'users/info/<int:uid>/', users.user_info),
    path('koderover/list/', koder.koderover_list),
    re_path(r'koderover/detail/(?P<id>[0-9]+)/(?P<action>\w+)/', koder.koderover_detail, name='koderover_detail'),
    path('koderover/add/', koder.koderover_add, name='koderover_add'),
    re_path(r'order/list/(?P<id>[0-9]+)/', order.order_list),
    path('order/detail/', order.order_detail),
    re_path(r'order/(?P<id>[0-9]+)/stage/(?P<sid>[0-9]+)/', order.order_stage),
]
