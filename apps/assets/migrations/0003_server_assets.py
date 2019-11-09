# Generated by Django 2.2.5 on 2019-09-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20190918_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server_Assets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100, unique=True, verbose_name='主机IP地址')),
                ('hostname', models.CharField(blank=True, max_length=100, null=True, verbose_name='主机名称')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='系统用户名')),
                ('passwd', models.CharField(blank=True, max_length=100, null=True, verbose_name='用户密码')),
                ('keyfile', models.SmallIntegerField(blank=True, null=True)),
                ('ssh_port', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True, verbose_name='SSH通信端口')),
                ('cpu', models.CharField(blank=True, max_length=100, null=True)),
                ('cpu_number', models.SmallIntegerField(blank=True, null=True)),
                ('disk_total', models.CharField(blank=True, max_length=100, null=True)),
                ('ram_total', models.IntegerField(blank=True, null=True)),
                ('kernel', models.CharField(blank=True, max_length=100, null=True)),
                ('swap', models.CharField(blank=True, max_length=100, null=True)),
                ('system', models.CharField(blank=True, max_length=100, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '服务器资产表',
                'verbose_name_plural': '服务器资产表',
                'db_table': 'ops_server_assets',
                'permissions': (('can_read_server_assets', '读取服务器资产权限'), ('can_change_server_assets', '更改服务器资产权限'), ('can_add_server_assets', '添加服务器资产权限'), ('can_delete_server_assets', '删除服务器资产权限')),
            },
        ),
    ]