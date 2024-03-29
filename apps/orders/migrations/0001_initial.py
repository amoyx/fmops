# Generated by Django 2.2.5 on 2019-10-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(verbose_name='订单ID号')),
                ('stage_name', models.CharField(max_length=100, verbose_name='订单处理名称')),
                ('stage_status', models.CharField(max_length=100, verbose_name='订单处理状态')),
                ('stage_cost', models.CharField(max_length=50, null=True, verbose_name='花费时间')),
                ('stage_log', models.TextField(max_length=5000, null=True, verbose_name='订单处理内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='订单处理时间')),
            ],
            options={
                'verbose_name': '订单日志表',
                'verbose_name_plural': '订单日志表',
                'db_table': 'ops_order_log',
                'permissions': (('can_read_order_log', '读取订单日志权限'), ('can_change_order_log', '更改订单日志权限'), ('can_add_order_log', '添加订单日志权限'), ('can_delete_order_log', '删除订单日志权限')),
            },
        ),
        migrations.CreateModel(
            name='Order_System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apps_id', models.IntegerField(verbose_name='应用ID号')),
                ('order_name', models.CharField(max_length=100, verbose_name='订单名称')),
                ('order_flag', models.CharField(max_length=100, verbose_name='订单执行结果')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='订单描述性内容')),
                ('create_user', models.CharField(max_length=50, null=True, verbose_name='创建订单用户')),
                ('cost_time', models.CharField(max_length=50, null=True, verbose_name='花费时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='订单创建时间')),
            ],
            options={
                'verbose_name': '订单系统表',
                'verbose_name_plural': '订单系统表',
                'db_table': 'ops_order_system',
                'permissions': (('can_read_order_system', '读取订单系统权限'), ('can_change_order_system', '更改订单系统权限'), ('can_add_order_system', '添加订单系统权限'), ('can_delete_order_system', '删除订单系统权限')),
            },
        ),
    ]
