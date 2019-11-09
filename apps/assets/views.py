from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
from apps.assets.models import Project_Assets, Server_Assets
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def project_list(request):
    projectList = Project_Assets.objects.all()
    return render(request, 'project/project_list.html',
                  {"user": request.user, "projectList": projectList})


@login_required(login_url='/login')
@csrf_exempt
def project_modf(request,id):
    if request.method == 'GET':
        project = Project_Assets.objects.get(id=id)
        return render(request,'project/project_modf.html',{"user": request.user, "project":project})


@login_required(login_url='/login')
def project_detail(request,id):
    if request.method == 'GET':
        project = Project_Assets.objects.get(id=id)
        return render(request,'project/project_detail.html',{"user": request.user, "project":project})


@login_required(login_url='/login')
def server_add(request):
    return render(request, 'server/host_add.html', {"user": request.user})


@login_required(login_url='/login')
def server_list(request):
    serverList = Server_Assets.objects.all()
    return render(request, 'server/host_list.html', {"user": request.user, "serverList": serverList})

@login_required(login_url='/login')
def server_detail(request,id):
    if request.method == 'GET':
        server = Server_Assets.objects.get(id=id)
        return render(request,'project/project_detail.html',{"user": request.user, "project":server})


@login_required(login_url='/login')
def server_modf(request,id):
    server = Server_Assets.objects.get(id=id)
    return render(request, 'server/host_modf.html', {"user": request.user,"server": server})
