from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.koderover.models import Koderover_Product
from fmops import settings
from django.http import HttpResponse
# Create your views here.


@login_required(login_url='/login')
def koderover_list(request):
    koderoverList = Koderover_Product.objects.all()
    return render(request, 'koderover/koderover_list.html',
                  {"user": request.user, "koderoverList": koderoverList, "jenkins_host": settings.JENKINS_HOST})


@login_required(login_url='/login')
def koderover_detail(request, id, action):
    if request.method == 'GET':
        koderover = Koderover_Product.objects.get(id=id)
        return render(request, 'koderover/koderover_detail.html', {"user": request.user, "koderover": koderover, "action": action})


@login_required(login_url='/login')
def koderover_add(request):
    return render(request, 'koderover/koderover_add.html', {"user": request.user})

