# Generated by Django 2.2.5 on 2019-10-18 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Koderover_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='Koderover 产品线名称')),
                ('service_name', models.CharField(max_length=100, verbose_name='Koderover 组件服务名称')),
                ('kube_namespace', models.CharField(max_length=100, verbose_name='kubernetes  namespace名称')),
                ('kube_deployment', models.CharField(max_length=150, verbose_name='kubernetes deployment名称')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='其他说明内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'Koderover产品表',
                'verbose_name_plural': 'Koderover产品表',
                'db_table': 'ops_koderover_product',
                'permissions': (('can_read_koderover_product', '读取Koderover产品权限'), ('can_change_koderover_product', '更改Koderover产品权限'), ('can_add_koderover_product', '添加Koderover产品权限'), ('can_delete_koderover_product', '删除Koderover产品权限')),
                'unique_together': {('product_name', 'service_name'), ('kube_namespace', 'kube_deployment')},
            },
        ),
    ]
