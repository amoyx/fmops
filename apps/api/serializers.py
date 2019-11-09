#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from rest_framework import serializers
from apps.assets.models import *
from apps.koderover.models import *
from django.contrib.auth.models import Group,User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username',
                  'first_name','last_name','email','is_staff',
                  'is_active','date_joined')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Assets
        fields = ('id','apps_id','business_name','project_name','project_envprofile',
                  'project_repo_address','project_kube_service','project_kube_namespace',
                  'project_start_cmdline','description','create_time')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server_Assets
        fields = ('id','ip_address','hostname','username','passwd',
                  'keyfile','ssh_port','cpu','cpu_number','disk_total',
                  'ram_total','kernel','swap','system','create_time')


class KoderOverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Koderover_Product
        fields = ('id','product_name','service_name','kube_namespace',
                  'kube_deployment','description','create_time')
