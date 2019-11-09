from django.db import models

# Create your models here.


class Koderover_Product(models.Model):
    '''Koderover产品表'''
    product_name = models.CharField(max_length=100, null=False, verbose_name='Koderover 产品线名称')
    service_name = models.CharField(max_length=100, null=False, verbose_name='Koderover 组件服务名称')
    kube_namespace = models.CharField(max_length=100, null=False, verbose_name='kubernetes  namespace名称')
    kube_deployment = models.CharField(max_length=150, null=False,verbose_name='kubernetes deployment名称')
    description = models.CharField(max_length=255, null=True, verbose_name='其他说明内容')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    class Meta:
        unique_together = [['product_name', 'service_name'], ['kube_namespace', 'kube_deployment']]
        db_table = 'ops_koderover_product'
        permissions = (
            ("can_read_koderover_product", "读取Koderover产品权限"),
            ("can_change_koderover_product", "更改Koderover产品权限"),
            ("can_add_koderover_product", "添加Koderover产品权限"),
            ("can_delete_koderover_product", "删除Koderover产品权限"),
        )
        verbose_name = 'Koderover产品表'
        verbose_name_plural = 'Koderover产品表'

