# -*- coding: utf-8 -*-
"""
@File    : rsync_slb.py
@Time    : 2021/12/18 10:11 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.http import HttpResponse,JsonResponse
from ..models import Balanced
import datetime,json
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest

def listslb(slb, cld):
    client = AcsClient(cld.key, cld.secret, 'cn-shenzhen')
    data = {}
    try:
        request = DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        request.set_Address(slb)
        response = client.do_action_with_exception(request)
    except Exception as e:
        return json.dumps(e)
    slb_result = str(response, encoding='utf-8')
    results = json.loads(slb_result)["LoadBalancers"]["LoadBalancer"]
    if results is not None:
        for result in results:
            try:
                descrequest = DescribeLoadBalancerAttributeRequest()
                descrequest.set_accept_format('json')
                descrequest.set_LoadBalancerId(result["LoadBalancerId"])
                descresponse = client.do_action_with_exception(descrequest)
            except Exception as e:
                return json.dumps(e)
            data = {"loadid": result["LoadBalancerId"], "ip": result["Address"], "loadname": result["LoadBalancerName"],
                    "vswitchId": result["VSwitchId"], "resgroup": result["ResourceGroupId"], "paytype": result["PayType"],
                    "masterzoneid": result["MasterZoneId"], "slavezoneid": result["SlaveZoneId"], "addresstype": result["AddressType"],
                    "loadbalancerspec": result["LoadBalancerSpec"], "vpcid": result["VpcId"], "regionid": result["RegionId"],
                    "status": result["LoadBalancerStatus"], "describeinfo": json.loads(str(descresponse, 'utf-8')),
                    "label": cld.id,
                    "create_time": datetime.datetime.strptime(result["CreateTime"], "%Y-%m-%dT%H:%MZ")}
            try:
                obj, create = Balanced.objects.update_or_create(ip=data["ip"], defaults=data)
                if create:
                    return JsonResponse({"status": "create", "message": "创建成功"})
                else:
                    return JsonResponse({"status:": "update", "message": "更新成功"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": 'Error: ' + str(e)})
