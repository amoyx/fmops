#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import urllib3
urllib3.disable_warnings()
import time
import getopt, sys, os
from fmops import settings


class KubernetesCluster(object):

    TOKEN = settings.K8S_TOKEN
    HOST = settings.K8S_HOST
    # TOKEN=$(kubectl get secret ${SECRET} -n kube-system -o json | jq -Mr '.data.token' | base64 -d)
    # CERT=kubectl get secret ${SECRET} -o json  -n kube-system | jq -Mr '.data["ca.crt"]' | base64 -d > ca.crt
    # 注： 可基于verify秘钥模式，也可以基于Token模式访问，本示例中基于TOKEN访问

    def __init__(self, host=HOST, token=TOKEN, namespace='default'):
        self.host = host
        self.namespace = namespace
        self.token = token
        # if not self._has_namespace(namespace):
        #     print("Error: 找不到 %s 该命名空间! " % str(namespace))
        #     exit()

    @property
    def host_address(self):
        return self.host

    @property
    def server_token(self):
        return self.token

    @property
    def request_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.server_token,
        }
        return headers

    def send_request(self, api, method='GET', data=None, content_type='JSON'):
        url = self.host_address + api
        headers = self.request_headers
        if content_type == 'YAML':
            headers['Content-Type'] = 'application/yaml'
        if method == 'GET':
            res = requests.get(url, verify=False, headers=headers)
        elif method == 'DELETE':
            res = requests.delete(url, verify=False, headers=headers)
        elif method == 'PUT':
            res =requests.put(url, verify=False, data=data, headers=headers)
        elif method == 'POST':
            res = requests.post(url, verify=False, data=json.dumps(data), headers=headers)
        return res.content.decode("utf-8")

    def _has_namespace(self, name):
        return True if name in self.list_namespace() else False

    def get_namespace(self, name=None):
        n = name if name else self.namespace
        api = '/api/v1/namespaces/%s' % n
        return self.send_request(api=api, method='GET')

    def get_namespace_status(self):
        api = '/api/v1/namespaces/%s/status' % self.namespace
        return json.loads(self.send_request(api=api, method='GET'))['status']['phase']

    def list_namespace(self):
        names = []
        data = json.loads(self.send_request(api='/api/v1/namespaces', method='GET'))
        if 'items' in data.keys():
            for c in data['items']: names.append(c["metadata"]["name"])
        return names

    def _has_deployment(self, dep_name):
        '''
        判断是否存在deployment
        :param dep_name: deployment名称
        :return:
        '''
        return True if dep_name in self.list_deployment() else False

    def get_deployment(self, dep_name):
        '''
        获取deployment信息
        :param dep_name: deployment名称
        :return:
        '''
        if not self._has_deployment(dep_name):
            return False
        api = '/apis/apps/v1/namespaces/{namespace}/deployments/{name}'.format(
                                                                namespace=self.namespace,
                                                                name=dep_name)
        return self.send_request(api=api, method='GET')

    def create_deployment(self, name, replicas=1, port=8080, package='/app/release.jar', env='prod'):
        api = '/apis/apps/v1/namespaces/%s/deployments' % self.namespace
        data = '''
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    qcloud-app: {name}
  name: {name}
spec:
  replicas: {replicas}
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      qcloud-app: {name}
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        qcloud-app: {name}
    spec:
      containers:
      - args:
        - -jar
        - -XX:+UnlockExperimentalVMOptions
        - -XX:+UseCGroupMemoryLimitForHeap
        - -XX:MaxRAMFraction=2
        - -Xss512k
        - -XX:MaxGCPauseMillis=200
        - -XX:ParallelGCThreads=10
        - -XX:+UseG1GC
        - -XX:CompileThreshold=100
        - -server
        - -Duser.timezone=GMT+08
        - -Dspring.profiles.active={env}
        - {package}
        command:
        - java
        image: {image}
        imagePullPolicy: Always
        name: {name}
        readinessProbe:
          failureThreshold: 3
          initialDelaySeconds: 30
          periodSeconds: 20
          successThreshold: 1
          tcpSocket:
            port: {port}
          timeoutSeconds: 2
        resources:
          limits:
            cpu: "2"
            memory: 1Gi
          requests:
            cpu: 10m
            memory: 512Mi
        securityContext:
          privileged: false
        terminationMessagePath: /dev/termination-log
      dnsPolicy: ClusterFirst
      imagePullSecrets:
      - name: qcloudregistrykey
      - name: tencenthubkey
      restartPolicy: Always
      serviceAccountName: ""
      terminationGracePeriodSeconds: 30
      volumes: null
        '''.format(name=name,
                   replicas=replicas,
                   image=self.get_product_latest_image(),
                   port=port,
                   package=package,
                   env=env)
        return self.send_request(api=api, method='POST', data=data, content_type='YAML')

    def list_deployment(self):
        '''
        列出指定命名空间所有deployment
        :param namespace: 命名空间
        :return:
        '''
        api = '/apis/apps/v1/namespaces/%s/deployments' % self.namespace
        deps = []
        data = json.loads(self.send_request(api=api, method='GET'))
        if 'items' in data.keys():
            for c in data['items']: deps.append(c["metadata"]["name"])
        return deps

    def update_deployment(self, name, latest_img):
        '''
        发起deployment更新操作

        :param name:  deployment名称
        :param k_product_name: koderover产品名称
        :param k_svc_name: koderover产品服务名称
        :return:
        '''
        api = '/apis/apps/v1/namespaces/{namespace}/deployments/{name}'.format(
                                                            namespace=self.namespace,
                                                            name=name)
        data = self.modify_deployment_template_data(name, latest_img)
        return self.send_request(api=api, data=data, method='PUT')

    def modify_deployment_template_data(self, name, new_image):
        '''
        修改原来deployment模板镜像
        :param name: deployment名称
        :param new_image: 新的docker镜像
        :return:
        '''
        template = self.get_deployment(name)
        running_image = json.loads(template)["spec"]["template"]["spec"]["containers"][0]["image"]
        template = template.replace(running_image, new_image, 1)
        return template

    def get_deployment_status(self, name):
        api = '/apis/apps/v1/namespaces/%s/deployments/%s/status' % (self.namespace, name)
        return json.loads(self.send_request(api=api, method='GET'))

    def list_services(self):
        api = '/api/v1/namespaces/%s/endpoints' % self.namespace
        services = []
        data = json.loads(self.send_request(api=api, method='GET'))
        if 'items' in data.keys():
            for c in data['items']: services.append(c["metadata"]["name"])
        return services

    def get_service(self, svc_name):
        api = '/api/v1/namespaces/%s/endpoints/%s' % (self.namespace, svc_name)
        return self.send_request(api=api, method='GET')

    def has_service(self, svc_name):
        return True if svc_name in self.list_services() else False

    def get_service_status(self, name):
        api = '/api/v1/namespaces/%s/services/%s/status' % (self.namespace, name)
        return self.send_request(api=api, method='GET')

    def _create_service(self, name, port):
        api = '/api/v1/namespaces/%s/services' % self.namespace
        data = '''
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.kubernetes.io/qcloud-loadbalancer-clusterid: cls-gt195ckd
  creationTimestamp: null
  labels:
    qcloud-app: {name}
  name: {name}
spec:
  ports:
  - name: tcp-{port}-{port}
    port: {port}
    protocol: TCP
    targetPort: {port}
  selector:
    qcloud-app: {name}
  sessionAffinity: None
  type: NodePort
        '''.format(name=name,port=port)
        return self.send_request(api=api, data=data, method='POST', content_type='YAML')

    def update_service(self, name, port):
        api = '/api/v1/namespaces/%s/services/%s' % (self.namespace, name)
        data='''
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.kubernetes.io/qcloud-loadbalancer-clusterid: cls-gt195ckd
  creationTimestamp: null
  labels:
    qcloud-app: {name}
  name: {name}
spec:
  ports:
  - name: tcp-{port}-{port}
    port: {port}
    protocol: TCP
    targetPort: {port}
  selector:
    qcloud-app: {name}
  sessionAffinity: None
  type: NodePort        
        '''.format(name=name,port=port)
        return self.send_request(api=api, data=data, method='PUT', content_type='YAML')

    def get_endpoints_subsets(self, svc_name):
        data = json.loads(self.get_service(svc_name))
        for subsets in data["subsets"]:
            for addr in subsets['addresses']:
                del addr['targetRef']
            del subsets["ports"]
        return data["subsets"]

    def get_endpoints_ports(self, svc_name):
        data = json.loads(self.get_service(svc_name))
        for subsets in data["subsets"]:
            del subsets["addresses"]
        return data["subsets"]

    def get_replicaset(self):
        api = '/apis/apps/v1/namespaces/{namespace}/replicasets/{name}'

    def list_replicasets(self):
        api = '/apis/apps/v1/namespaces/%s/replicasets' % self.namespace
        return self.send_request(api=api, method='GET')

    def get_product_latest_image(self, product_name, service_name):
        k = KodeRoverObject(product_name=product_name)
        return k.is_publish_image_by_day(service_name)

    def __create_configmaps(self, name):
        api = '/api/v1/namespaces/%s/configmaps' % self.namespace
        data = '''
        '''
        return self.send_request(api=api, data=data, method='POST', content_type='YAML')

    def list_configmaps(self):
        api = ' /api/v1/namespaces/%s/configmaps' % self.namespace
        return self.send_request(api=api, method='GET')

    def get_configmap(self, name):
        api='/api/v1/namespaces/%s/configmaps/%s' % (self.namespace, name)
        return self.send_request(api=api, method='GET')

    def list_all_configmaps(self):
        api = '/api/v1/configmaps'
        return self.send_request(api=api, method='GET')

    def __delete_configmap(self, name):
        api = '/api/v1/namespaces/%s/configmaps/%s' % (self.namespace, name)
        return self.send_request(api=api, method='DELETE')

    def list_secrets(self):
        api = '/api/v1/namespaces/%s/secrets' % self.namespace
        data = json.loads(self.send_request(api=api, method='GET'))
        secrets = []
        for dt in data['items']:
            secrets.append(dt['metadata']['name'])
        return secrets

    def list_all_secrets(self):
        api = '/api/v1/secrets'
        return self.send_request(api=api, method='GET')

    def get_secrets(self, name):
        api = '/api/v1/namespaces/%s/secrets/%s' % (self.namespace, name)
        return self.send_request(api=api, method='GET')


class KodeRoverObject(KubernetesCluster):

    HOST = settings.KODEROVER_HOST
    TOKEN = settings.KODEROVER_TOKEN

    def __init__(self, product_name='default'):
        # super().__init__(host='https://cls-gt195ckd-kubelb.sh.1251026273.clb.myqcloud.com')
        self.product_name = product_name

    @property
    def host_address(self):
        return self.HOST

    @property
    def server_token(self):
        return self.TOKEN

    @property
    def request_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'X-API-KEY ' + self.server_token,
        }
        return headers

    def get_deliver_data(self):
        api = '/api/directory/dc/releases?productName=%s' % self.product_name
        return self.send_request(api=api, method='GET')

    def query_workflow_name(self):
        data = json.loads(self.get_deliver_data())
        workflow = []
        for wf in data:
            workflow.append(wf['versionInfo']['workflowName'])
        return list(set(workflow))

    def list_images_by_product(self):
        '''
        按照工程名称 列出所有交付的镜像
        :return:
        '''
        data = json.loads(self.get_deliver_data())
        img_list = []
        for d in data:
            img_list.append({
                'serviceName': d['buildInfo'][0]['serviceName'],
                'imageName': d['buildInfo'][0]['imageName']
            })
        return img_list

    def query_images_by_service(self, name):
        '''
        查询指定服务名称的 已交付镜像, 按最新时间进行排序
        :param name:  服务名称
        :return:
        '''
        data = self.list_images_by_product()
        images = []
        for d in data:
            if d['serviceName'] == name:
                images.append(d["imageName"])

        for i in range(0, len(images)-1):
            min = i
            for j in range(i+1, len(images)):
                t1 = int(str(images[j]).split(":")[-1].split('-')[0])
                t2 = int(str(images[min]).split(":")[-1].split('-')[0])
                if t1 > t2:
                    min = j
            images[i], images[min] = images[min], images[i]
        return images

    def is_publish_image_by_day(self, name):
        '''
        确定当天是否有已交付 可发布镜像
        :param name:
        :return:
        '''
        data = self.query_images_by_service(name)
        day = time.strftime('%Y%m%d', time.localtime())
        if len(data) >= 1:
            version = str(data[0]).split(":")[-1].split('-')[0]
            if str(day) in version:
                return data[0]
            else:
                return False
        else:
            return False



