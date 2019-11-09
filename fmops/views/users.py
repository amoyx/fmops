#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect


@login_required(login_url='/login')
def user_manage(request):
    if request.method == "GET":
        userList = User.objects.raw(''' SELECT a.*, b.key FROM auth_user as a INNER JOIN authtoken_token as b ON a.id = b.user_id ''')
        groupList = Group.objects.all()
        return render(request,'users/user_manage.html', {"user": request.user,
                                                         "userList": userList,
                                                         "groupList": groupList})


@login_required(login_url='/login')
def user_center(request, uid):
    if request.method == "GET":
        try:
            user = User.objects.get(id=uid)
        except Exception as e:
            return render(request,'users/user_center.html',{"user":request.user,
                                                             "errorInfo":"用户不存在，可能已经被删除."})
        #获取用户权限列表
        userGroupList = []
        permList = Permission.objects.filter(codename__startswith="can_")
        userPermList = [u.get('id') for u in user.user_permissions.values()]
        for ds in permList:
            if ds.id in userPermList:ds.status = 1
            else:ds.status = 0
        #获取用户组列表
        groupList = Group.objects.all()
        userGroupList = [g.get('id') for g in user.groups.values()]
        for gs  in groupList:
            if gs.id in userGroupList:gs.status = 1
            else:gs.status = 0
        return render(request,'users/user_center.html', {"user":request.user,"user_info": user,
                                                        "permList": permList, "groupList": groupList})
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.get(username=request.POST.get('username'))
                user.set_password(request.POST.get('password'))
                user.save()
                return JsonResponse({"code": 200, "data": None, "msg": "密码修改成功"})
            except Exception as e:
                return JsonResponse({"code": 500, "data": None, "msg": "密码修改失败：%s" % str(e)})
        else:
            return JsonResponse({"code": 500, "data": None, "msg": "密码不一致，密码修改失败。"})


@login_required(login_url='/login')
def user_info(request, uid):
    if request.method == "POST":
        try:
            user = User.objects.get(id=uid)
            User.objects.filter(id=uid).update(
                                            is_active=request.POST.get('is_active'),
                                            is_superuser=int(request.POST.get('is_superuser')),
                                            email=request.POST.get('email'),
                                            first_name=request.POST.get('first_name'),
                                            username=request.POST.get('username')
                                            )
            #如果权限key不存在就单做清除权限
            if request.POST.getlist('perms') is None:
                user.user_permissions.clear()
            else:
                userPermList = []
                for perm in user.user_permissions.values():
                    userPermList.append(perm.get('id'))
                permList = [int(i) for i in request.POST.getlist('perms')]
                addPermList = list(set(permList).difference(set(userPermList)))
                delPermList = list(set(userPermList).difference(set(permList)))
                #添加新增的权限
                for permId in addPermList:
                    perm = Permission.objects.get(id=permId)
                    User.objects.get(id=uid).user_permissions.add(perm)
                #删除去掉的权限
                for permId in delPermList:
                    perm = Permission.objects.get(id=permId)
                    User.objects.get(id=uid).user_permissions.remove(perm)
            #如果用户组key不存在就单做清除用户组
            if request.POST.getlist('groups') is None:
                user.groups.clear()
            else:
                userGroupList = []
                for group in user.groups.values():
                    userGroupList.append(group.get('id'))
                groupList = [ int(i) for i in request.POST.getlist('groups')]
                addGroupList = list(set(groupList).difference(set(userGroupList)))
                delGroupList = list(set(userGroupList).difference(set(groupList)))
                #添加新增的用户组
                for groupId in addGroupList:
                    group = Group.objects.get(id=groupId)
                    user.groups.add(group)
                #删除去掉的用户组
                for groupId in delGroupList:
                    group = Group.objects.get(id=groupId)
                    user.groups.remove(group)
            return HttpResponseRedirect('/users/center/{uid}/'.format(uid=uid))
        except Exception as e:
            return render(request, 'users/user_center.html', {"user": request.user, "errorInfo": "用户资料修改错误：%s" % str(e)})
