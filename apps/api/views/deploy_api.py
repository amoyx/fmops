#!/usr/bin/python
# -*- coding=utf-8 -*-
from django.http import JsonResponse, HttpResponse
import json
from utils.jenkins import JenkinsAPI
from fmops import settings
from apps.assets.models import Project_Assets
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@api_view(['POST'])
def deploy_run(request):
    """
    应用发布
    """
    if request.method == 'POST':
        try:
            id = json.loads(request.body).get('id')
            project_name = json.loads(request.body).get('project_name')
            codebranch = json.loads(request.body).get('codebranch')
        except Exception as ex:
            id = request.POST.get('id', None)
            project_name = request.POST.get('project_name',None)
            codebranch = request.POST.get('codebranch',None)

        try:
            project = Project_Assets.objects.get(Q(id=id),
                                                 Q(project_name=project_name))
            jenkins = JenkinsAPI()
            return JsonResponse(jenkins.build_job(job_name='execute-pipeline',
                                project=project.project_name,
                                envprofile=project.project_envprofile,
                                git_address='/'.join([settings.GITLAB_PATH,
                                                      project.project_repo_address]),
                                codebranch=codebranch,
                                namespace=project.project_kube_namespace,
                                servicename=project.project_kube_service,
                                special_cmdline=project.project_start_cmdline
                                ))
        except Exception as ex:
            return JsonResponse({
                'status': 'FAILED', "task_id": None, "messages": str(ex)
            })


@api_view(['GET'])
def get_job_full_status(request, action, task_id):
    """
    部署任务结果查询
    """
    try:
        job_name = 'rollback-pipeline' if action == 'rollback' else 'execute-pipeline'
        jenkins = JenkinsAPI()
        return JsonResponse(jenkins.get_job_result_describe(job_name, int(task_id), action))
    except Exception as e:
        return JsonResponse({'status': "FAILED", "info": str(e)})


@api_view(['GET'])
def get_job_stage_status(request, action, task_id, stage_id):
    try:
        job_name = 'rollback-pipeline' if action == 'rollback' else 'execute-pipeline'
        jenkins = JenkinsAPI()
        return JsonResponse(jenkins.get_job_stage_status(job_name, int(task_id), int(stage_id)))
    except Exception as e:
        return JsonResponse({"status": "FAILED", "info": str(e)})


@api_view(['POST'])
def deploy_rollback(request):
    """
    应用回滚
    """
    try:
        id = json.loads(request.body).get('id')
        project_name = json.loads(request.body).get('project_name')
        rollback_version = json.loads(request.body).get('rollback_version')
    except Exception as ex:
        id = request.POST.get('id', None)
        project_name = request.POST.get('project_name', None)
        rollback_version = request.POST.get('rollback_version', None)

    if request.method == 'POST':
        try:
            project = Project_Assets.objects.get(Q(id=id),
                                                 Q(project_name=project_name))
            jenkins = JenkinsAPI()
            return JsonResponse(jenkins.build_job(job_name='rollback-pipeline',
                                                  project=project.project_name,
                                                  rollback_version=rollback_version,
                                                  namespace=project.project_kube_namespace)
                                )
        except Exception as ex:
            return JsonResponse({
                'status': 'FAILED', "build_id": None, "info": str(ex)
            })
