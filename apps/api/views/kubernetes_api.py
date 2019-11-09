#!/usr/bin/env python
# _#_ coding:utf-8 _*_

from fmops import settings
import requests


class kubeAPI(object):

    @staticmethod
    def kube_history(namespace, deployment):
        api = '%s/api/v1/deployment/%s/%s/oldreplicaset' % (settings.KUBERNETES_API,namespace,deployment)
        try:
            return requests.get(api).json()
        except Exception as ex:
            return {}

    @staticmethod
    def kube_event(namespace, deployment):
        api = '%s/api/v1/deployment/%s/%s/event' % (settings.KUBERNETES_API,namespace,deployment)
        try:
            return requests.get(api).json()
        except Exception as ex:
            return {}

    @staticmethod
    def kube_detail(namespace, deployment):
        api = "%s/api/v1/deployment/%s/%s" % (settings.KUBERNETES_API,namespace,deployment)
        try:
            return requests.get(api).json()
        except Exception as ex:
            return {}

    @staticmethod
    def kube_replicaset(namespace, deployment):
        api = '%s/api/v1/deployment/%s/%s/newreplicaset' % (settings.KUBERNETES_API, namespace, deployment)
        try:
            return requests.get(api).json()
        except Exception as ex:
            return {}

    def kube_pod_list(self,namespace, deployment):
        try:
            replicaset=self.kube_replicaset(namespace, deployment)
            api = '{host}/api/v1/replicaset/{namespace}/{replicaset}/pod'.format(
                                                             host=settings.KUBERNETES_API,
                                                             namespace=namespace,
                                                             replicaset=replicaset['objectMeta']['name'])
            return requests.get(api).json()
        except Exception as ex:
            return {}
