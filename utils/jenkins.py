#!/usr/bin/python
# -*- coding=utf-8 -*-

import jenkins
import requests
from requests.auth import HTTPBasicAuth
from enum import Enum
from utils import base
from fmops import settings
import json


class JenkinsAPI(object):

    def __init__(self):
        self.host = settings.JENKINS_HOST
        self.username = settings.JENKINS_USER
        self.passwd = settings.JENKINS_TOKEN
        self.login = self.connect

    @property
    def connect(self):
        try:
            return jenkins.Jenkins(self.host, self.username, self.passwd)
        except jenkins.JenkinsException as ex:
            print("Error, 连接失败",str(ex))
            raise ("jenkins connection fail")

    def _has_job(self, name):
        return self.connect.job_exists(name)

    def get_version(self):
        return (self.username, self.connect.get_version())

    def get_job_list(self):
        return self.connect.get_jobs()

    def _get_queue_info(self, number):
        return self.connect.get_queue_item(number)

    def __get_job_info(self,job_name):
        return self.connect.get_job_info(job_name)

    def build_job(self, job_name="execute-pipeline", **kwargs):
        if 'special_cmdline' in kwargs.keys() and kwargs.get('special_cmdline', None) is None:
            del kwargs['special_cmdline']
        if False in base.is_exist(list(kwargs.values())):
            return {"status": 'FAILED', "task_id": None, "info": "Parameters cannot be null!"}
        if not self._has_job(job_name):
            return {"status": 'FAILED', "task_id": None, "info": "jenknis job is not exits!"}
        build_id = self._get_next_build_number(job_name)
        try:
            self.connect.build_job(job_name,parameters=kwargs)
            return {"status": 'SUCCESS', "task_id": build_id, "info": "SUCCESS"}
        except jenkins.JenkinsException as ex:
            return {"status": 'FAILED', "task_id": None, "info": str(ex)}

    def _get_next_build_number(self, job_name):
        ''' get jenkins job next build number
        :param job_name:
        :return: get jenkins job next build number
        '''
        return self.connect.get_job_info(job_name)['nextBuildNumber']

    def get_last_build_numer(self, job_name):
        ''' get jenkins last build number
        :param job_name:
        :return: get jenkins last build number
        '''
        return self.connect.get_job_info(job_name)['lastBuild']['number']

    def get_build_result(self, job_name, build_id):
        return self.connect.get_build_info(job_name, build_id)['result']

    def _get_build_output(self, job_name, build_id):
        return self.connect.get_build_console_output(job_name, build_id)

    def _send_request(self,api,method='GET'):
        if not api: return "Error: api cann't is empty"
        return requests.get(api,auth=HTTPBasicAuth(self.username,self.passwd))

    def get_job_stage_log(self,job_name,build_id,node_id):
        api = self.host+"/job/{jobName}/{buildID}/execution/node/{nodeID}/wfapi/log".format(
                                                                                    nodeID=node_id,
                                                                                    jobName=job_name,
                                                                                    buildID=build_id)
        return dict(self._send_request(api)).get('text','服务正在处理中......')

    def get_job_stage_status(self, job_name, build_id, stage_id):
        api = self.host + "/job/%s/%s/execution/node/%s/wfapi/describe" % (job_name, build_id, stage_id)
        log_paths = []
        log_content = ''
        try:
            stage_content = json.loads(self._send_request(api).text)
            if isinstance(stage_content, dict) and 'stageFlowNodes' in stage_content.keys() and isinstance(stage_content['stageFlowNodes'], list):
                for stage in stage_content['stageFlowNodes']:
                    log_paths.append(stage['_links']['log']['href'])
            if len(log_paths) >= 1:
                for href in log_paths:
                    temp_log = json.loads(self._send_request(self.host + href).text).get('text', '服务正在处理中......')
                    log_content += temp_log
            if not log_content: log_content = "未找到日志内容"
            return {'status': 'SUCCESS', 'info': log_content}
        except Exception as e:
            return {'status': 'FAILED', 'info': str(e)}

    def get_job_result_describe(self, job_name, build_id, action):
        api = self.host + "/job/%s/%s/wfapi/describe" % (job_name, build_id)
        job_output = self._send_request(api).json()
        if isinstance(job_output, dict) and 'stages' in job_output.keys():
            stages_content = job_output.get('stages')
            for stage in stages_content:
                del stage['_links']
                stage['href'] = '/api/v1/deploy/stage/status/%s/%s/%s/' % (action, build_id, stage['id'])
        return job_output

    def is_building(self, job_name):
        return False if self.get_build_result(job_name,self.get_last_build_numer(job_name)) else True


class statusCode(Enum):
    ERROR = 400
    SUCCESS = 200
    NOTFOUND = 404
    WAITING = 202
