# -*- coding: utf-8 -*-
"""
@File    : aliyun_rsync.py
@Time    : 2021/12/13 5:51 下午
@Author  : xxlaila
@Software: PyCharm
"""

import json, logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeDisksRequest import DescribeDisksRequest
from ..models import AssetExpansion
from ..models import DiskInfo
from django.http import JsonResponse
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')

def list_instances(dicts, cld):
    client = AcsClient(cld.key, cld.secret, 'cn-shenzhen')
    data_list = []
    for ip_dict in dicts:
        old_data = AssetExpansion.objects.filter(primaryip=ip_dict)
        if old_data:
            data_list.append(old_data)
    try:
        request = DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_PrivateIpAddresses(dicts)
        response = client.do_action_with_exception(request)
    except Exception as e:
        return json.dumps(e)
    data = {}
    if response is not None:
        instance_list = str(response, encoding='utf-8')
        results = json.loads(instance_list)["Instances"]["Instance"]
        disk_data_name = []
        disk_data_size = []
        disk_data_type = []
        for result in results:
            diskrequest = DescribeDisksRequest()
            diskrequest.set_accept_format('json')
            diskrequest.set_InstanceId("{}".format(result["InstanceId"]))
            diskrequest.set_PageSize(20)
            diskresponse = client.do_action_with_exception(diskrequest)
            disk_list = str(diskresponse, encoding='utf-8')
            diskresult = json.loads(disk_list)["Disks"]["Disk"]
            operuser = ''
            devuser = ''
            dept = ''
            disk_data = {}
            new_format = "%Y-%m-%d %H:%M:%S"
            if result["PublicIpAddress"]["IpAddress"]:
                publicip = result["PublicIpAddress"]["IpAddress"][0]
            else:
                publicip = ''
            if result["EipAddress"]["IpAddress"]:
                eip = result["EipAddress"]["IpAddress"]
                ebandwidth = result["EipAddress"]["Bandwidth"]
                paybywidth = result["EipAddress"]["InternetChargeType"]
            else:
                eip = ''
                ebandwidth = int()
                paybywidth = ''
            if 'CentOS  6' or 'CentOS 7.5' in result["OSNameEn"]:
                core_thread = int()
                cpu_vcpus = result["Cpu"]
                cpu_cores = int()
            else:
                core_thread = result["CpuOptions"]["ThreadsPerCore"]
                cpu_vcpus = result["Cpu"]
                cpu_cores = result["CpuOptions"]["CoreCount"]
            if 'Tags' in result:
                for i in result["Tags"]["Tag"]:
                    if 'oper_user' in i.values():
                        operuser = i["TagValue"]
                    if 'dev_user' in i.values():
                        devuser = i["TagValue"]
                    if 'department' in i.values():
                        dept = i["TagValue"]
            else:
                operuser = ''
                devuser = ''
                dept = ''
            if "LocalStorageAmount" in result.keys():
                localstoranum = result["LocalStorageAmount"]
            else:
                localstoranum = int()
            if "LocalStorageCapacity" in result.keys():
                localstorasize = result["LocalStorageCapacity"]
            else:
                localstorasize = int()
            create_d1 = datetime.datetime.strptime(result["CreationTime"], "%Y-%m-%dT%H:%SZ")
            start_d1 = datetime.datetime.strptime(result["StartTime"], "%Y-%m-%dT%H:%SZ")
            expired_d1 = datetime.datetime.strptime(result["ExpiredTime"], "%Y-%m-%dT%H:%SZ")
            data = {"hostname": result["HostName"], "instance": result["InstanceId"], "memory": result["Memory"],
                    "core_thread": core_thread, "cpu_vcpus": cpu_vcpus, "cpu_cores": cpu_cores,
                    "localstoranum": localstoranum, "localstorasize": localstorasize,
                    "os_version": result["OSNameEn"], "os_arch": result["OSType"], "images": result["ImageId"],
                    "vpc": result["VpcAttributes"]["VpcId"], "security": result["SecurityGroupIds"]["SecurityGroupId"],
                    "vswaitch": result["VpcAttributes"]["VSwitchId"], "instancetype": result["InstanceType"],
                    "eip": eip, "ebandwidth": ebandwidth, "paybywidth": paybywidth, "publicip": publicip,
                    "primaryip": result["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"],
                    "primarynetwork": result["NetworkInterfaces"]["NetworkInterface"][0]["NetworkInterfaceId"],
                    "primarymac": result["NetworkInterfaces"]["NetworkInterface"][0]["MacAddress"],
                    "regionid": result["RegionId"], "zoneid": result["ZoneId"], "chargetype": result["InstanceChargeType"],
                    "operuser": operuser, "devuser": devuser, "dept": dept, "status": result["Status"],
                    "create_time": (create_d1 + datetime.timedelta(hours=8)).strftime(new_format),
                    "cloudinfor_id": cld.id,
                    "start_time": (start_d1 + datetime.timedelta(hours=8)).strftime(new_format),
                    "expired_time": expired_d1.strftime(new_format),
                    }
            try:
                obj, create = AssetExpansion.objects.update_or_create(primaryip=data["primaryip"], defaults=data)
            except Exception as e:
                return {"message": 'Error: ' + str(e)}
            asset_id = AssetExpansion.objects.filter(instance=result["InstanceId"]).first()
            for i in diskresult:
                disk_data['diskid'] = i["DiskId"]
                disk_data['device'] = i["Device"]
                disk_data['category'] = i["Category"]
                disk_data['disk_size'] = i["Size"]
                disk_data['chargetype'] = i["DiskChargeType"]
                disk_data['zoneid'] = i["ZoneId"]
                disk_data['delwith'] = i["DeleteWithInstance"]
                disk_data['snapshot'] = i["EnableAutomatedSnapshotPolicy"]
                disk_data['autoanspshot'] = i["EnableAutoSnapshot"]
                disk_data['regionid'] = i["RegionId"]
                disk_data['disk_type'] = i["Type"]
                disk_data['encrypted'] = i["Encrypted"]
                disk_data['status'] = i["Status"]
                disk_data['assetexpansion_id'] = asset_id.id
                expired_time = datetime.datetime.strptime(i["ExpiredTime"], "%Y-%m-%dT%H:%MZ")
                create_time = datetime.datetime.strptime(i["CreationTime"], "%Y-%m-%dT%H:%M:%SZ")
                disk_data['expired_time'] = expired_time.strftime(new_format)
                disk_data['create_time'] = create_time.strftime(new_format)
                try:
                    obj, create = DiskInfo.objects.update_or_create(diskid=disk_data['diskid'], defaults=disk_data)
                except Exception as e:
                    print(str(e))
                    return ({"status": "error", "message": 'Error: ' + str(e)})