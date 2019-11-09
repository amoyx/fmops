#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models
from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models
from fmops import settings


class Tencent_Cloud_Object(object):

    SecretId = settings.TENCENT_SECRET_ID
    SecretKey = settings.TENCENT_SECRET_KEY

    def __init__(self):
        self._cred = credential.Credential(self.SecretId, self.SecretKey)

    @property
    def credential(self):
        return self._cred

    @staticmethod
    def profile(service="cvm"):
        httpProfile = HttpProfile()
        httpProfile.endpoint = service + ".tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        return clientProfile


class Tencent_Cloud_NetWork(Tencent_Cloud_Object):
    SERVICE_NAME = "vpc"

    def describe_vpc_request(self, region):
        client = vpc_client.VpcClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = vpc_models.DescribeVpcsRequest()
        req.from_json_string('{}')
        return json.loads(client.DescribeVpcs(req).to_json_string())

    def describe_subnet_request(self, region, vpc_id, zone='ap-shanghai-2'):
        client = vpc_client.VpcClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = vpc_models.DescribeSubnetsRequest()
        params = '{"Filters":[{"Name":"vpc-id","Values":["%s"]},{"Name":"zone","Values":["%s"]}]}' % (vpc_id, zone) if vpc_id else '{}'
        req.from_json_string(params)
        return json.loads(client.DescribeSubnets(req).to_json_string())['SubnetSet']

    def describe_subnet_zone_request(self, region, vpc_id, zone):
        subnets = self.describe_subnet_request(region, vpc_id)
        subnet_list = []
        for subnet in subnets:
            if subnet['Zone'] == zone:
                subnet_list.append(subnet)
        return subnet_list

    def describe_security_groups(self, region):
        client = vpc_client.VpcClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = vpc_models.DescribeSecurityGroupsRequest()
        req.from_json_string('{}')
        return json.loads(client.DescribeSecurityGroups(req).to_json_string())['SecurityGroupSet']

    def describe_security_group_policies(self, region, security_id):
        client = vpc_client.VpcClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = vpc_models.DescribeSecurityGroupPoliciesRequest()
        params = '{"SecurityGroupId":"%s"}' % security_id
        req.from_json_string(params)
        resp = client.DescribeSecurityGroupPolicies(req)
        return json.loads(resp.to_json_string())['SecurityGroupPolicySet']


class Tencent_Cloud_CVM(Tencent_Cloud_Object):
    SERVICE_NAME = "cvm"

    def describe_region_request(self):
        client = cvm_client.CvmClient(self.credential, "ap-shanghai", self.profile(self.SERVICE_NAME))
        req = models.DescribeRegionsRequest()
        params = '{}'
        req.from_json_string(params)
        resp = client.DescribeRegions(req)
        return resp.to_json_string()

    def describe_zone_request(self, region):
        zone_list = []
        client = cvm_client.CvmClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = models.DescribeZonesRequest()
        req.from_json_string('{}')
        resp = json.loads(client.DescribeZones(req).to_json_string())
        for zone in resp['ZoneSet']:
            if zone['ZoneState'] == "AVAILABLE":
                zone_list.append(zone)
        return zone_list

    def describe_images_request(self, region):
        client = cvm_client.CvmClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = models.DescribeImagesRequest()
        req.from_json_string('{}')
        resp = client.DescribeImages(req)
        return resp.to_json_string()

    def get_os_image_list(self, region, platform='Centos'):
        os_list = []
        images = json.loads(self.describe_images_request(region))
        for image in images['ImageSet']:
            if str(image['Platform']).upper() == platform.upper():
                os_list.append(image)
        return os_list

    def describe_instance_config_request(self, region):
        client = cvm_client.CvmClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = models.DescribeZoneInstanceConfigInfosRequest()
        req.from_json_string('{}')
        return json.loads(client.DescribeZoneInstanceConfigInfos(req).to_json_string())

    def describe_instance_status_request(self, region):
        client = cvm_client.CvmClient(self.credential, region, self.profile(self.SERVICE_NAME))
        req = models.DescribeInstancesStatusRequest()
        req.from_json_string('{}')
        return json.loads(client.DescribeInstancesStatus(req).to_json_string())

    def run_instances_request(self, args):
        client = cvm_client.CvmClient(self.credential, args['region'], self.profile(self.SERVICE_NAME))
        req = models.RunInstancesRequest()
        params ={"InstanceChargeType": "PREPAID",
                 "InstanceChargePrepaid": {
                     "Period": int(args['Period']),
                     "RenewFlag": "NOTIFY_AND_MANUAL_RENEW"
                 },
                 "Placement": {
                     "Zone": args['zone']
                 },
                 "InstanceType": args['InstanceType'],
                 "ImageId": args['ImageId'],
                 "InstanceCount": 1,
                 "SystemDisk": {
                     "DiskType": args['DiskType'],
                     "DiskSize": int(args['DiskSize'])
                 },
                 "HostName": args['HostName'],
                 "VirtualPrivateCloud": {
                     "VpcId": args['vpc'],
                     "SubnetId": args['subnet']
                 },
                 "InternetAccessible": {
                     "InternetChargeType": args['InternetChargeType'],
                     "InternetMaxBandwidthOut": int(args['InternetMaxBandwidthOut']),
                     "PublicIpAssigned": args['PublicIpAssigned']
                 },
                 "LoginSettings": {
                     "Password": args['Password']
                 },
                 "SecurityGroupIds": [args['SecurityGroupIds']]
             }
        req.from_json_string(json.dumps(params))
        resp = client.RunInstances(req)
        return json.loads(resp.to_json_string())

