# -*- coding: utf-8 -*-
"""
@File    : asset_expansion.py
@Time    : 2021/12/13 2:51 下午
@Author  : xxlaila
@Software: PyCharm
"""

from elastics.models.cloudinfor import CloudInfor
from elastics.models.esnode import EsNode
from ..models import AssetExpansion
from .aliyun_rsync import list_instances
from django.http import HttpResponse

def get_es_nodes():
    result = {}
    aliyun = []
    tengxunyun = []

    for k in EsNode.objects.all():
        if k.metainfo.cloud.value == 'aliyun':
            aliyun.append(k.ip)
        else:
            tengxunyun.append(k.ip)
        result['aliyun'] = aliyun
        result['tengxunyun'] = tengxunyun
    return result

def fenzu(lists, res):
    n = 8
    data = []
    for b in [lists[i:i + n] for i in range(0, len(lists), n)]:
        data.append(list_instances(b, res))
    return HttpResponse(data)

def cloud_asset_rsync(request):
    for k, v in get_es_nodes().items():
        if k == 'aliyun':
            res = CloudInfor.objects.get(value=k)
            fenzu(v, res)
        else:
            pass



