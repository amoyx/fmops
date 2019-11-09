#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from django.db import models
# Create your models here.
import sys


class Project_Assets(models.Model):
    '''产品线资产表'''
    apps_id = models.IntegerField(null=False,unique=True,verbose_name='应用ID号')
    business_name = models.CharField(max_length=50, verbose_name='业务线名称')
    project_name = models.CharField(max_length=50, verbose_name='应用名称')
    project_envprofile = models.CharField(max_length=20,null=True,verbose_name='项目运行环境' )
    project_repo_address = models.CharField(max_length=255, null=True, blank=True,verbose_name='git仓库地址')
    project_kube_service = models.CharField(max_length=150, null=True,verbose_name='应用kubernetes服务名称')
    project_kube_namespace = models.CharField(max_length=50, null=True, verbose_name='应用所属kubernetes命名空间')
    project_start_cmdline = models.CharField(max_length=255, null=True, verbose_name='应用启动指令')
    description = models.CharField(max_length=255,null=True,verbose_name='其他说明内容')
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='创建时间')
    class Meta:
        # unique_together=('business_name','project_name','project_envprofile')
        db_table = 'ops_project_assets'
        permissions = (
            ("can_read_project_assets", "读取产品线权限"),
            ("can_change_project_assets", "更改产品线权限"),
            ("can_add_project_assets", "添加产品线权限"),
            ("can_delete_project_assets", "删除产品线权限"),
        )
        verbose_name = '项目资产表'
        verbose_name_plural = '项目资产表'


class Server_Assets(models.Model):
    ip_address = models.CharField(max_length=100,unique=True,blank=False,null=False,verbose_name='主机IP地址')
    hostname = models.CharField(max_length=100,blank=True,null=True,verbose_name='主机名称')
    username = models.CharField(max_length=100,blank=True,null=True,verbose_name='系统用户名')
    passwd = models.CharField(max_length=100,blank=True,null=True,verbose_name='用户密码')
    keyfile =  models.SmallIntegerField(blank=True,null=True)#FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    ssh_port = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True,verbose_name='SSH通信端口')
    cpu = models.CharField(max_length=100,blank=True,null=True)
    cpu_number = models.SmallIntegerField(blank=True,null=True)
    disk_total = models.CharField(max_length=100,blank=True,null=True)
    ram_total= models.IntegerField(blank=True,null=True)
    kernel = models.CharField(max_length=100,blank=True,null=True)
    swap = models.CharField(max_length=100,blank=True,null=True)
    system = models.CharField(max_length=100,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    '''自定义添加只读权限-系统自带了add change delete三种权限'''
    class Meta:
        db_table = 'ops_server_assets'
        permissions = (
            ("can_read_server_assets", "读取服务器资产权限"),
            ("can_change_server_assets", "更改服务器资产权限"),
            ("can_add_server_assets", "添加服务器资产权限"),
            ("can_delete_server_assets", "删除服务器资产权限"),
        )
        verbose_name = '服务器资产表'
        verbose_name_plural = '服务器资产表'
