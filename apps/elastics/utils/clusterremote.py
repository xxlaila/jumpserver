# -*- coding: utf-8 -*-
"""
@File    : clusterremote.py
@Time    : 2021/11/4 11:36 上午
@Author  : xxlaila
@Software: PyCharm
"""

from elasticsearch import TransportError
from ..models import BasicCluster, MetaInfo, ClusterRemote,ClusterSetting
from ..utils import default_conn
import datetime,time,json
import logging
from rest_framework.views import Response
from django.http import JsonResponse
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)

@shared_task
@register_as_period_task(interval=600)
def cluster_remote_connent(_settins=None):
    try:
        obj = []
        if _settins is None:
            _settins = MetaInfo.objects.filter(setting=True)
        for k in _settins:
            try:
                data = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.remote_info()
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.EsConnection(k.address, k.username,
                                                     k.password).connentauth().cluster.remote_info()
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            result = get_cluster_remote(data, k)
            if result:
                obj.append(result)
            else:
                obj.append("error")
        return Response({"status": obj})
    except MetaInfo.DoesNotExist:
        return False

def get_cluster_remote(results, k):
    result = {}
    if results is not None:
        for key, vaule in results.items():
            data = {"name": key, "mode": vaule["mode"], "conn": vaule["connected"],
                    "conn_timeout": vaule["initial_connect_timeout"],
                    "skip_una": vaule["skip_unavailable"], "seeds": vaule["seeds"],
                    "num_nodes": vaule["num_nodes_connected"],
                    "max_conn": vaule["max_connections_per_cluster"], "proxy_add": "", "metainfo_id": k.id}
            try:
                obj, created = ClusterRemote.objects.update_or_create(name=data['name'], metainfo_id=k.id, defaults=data)
                if obj:
                    result.update({"update ": [data['name'], k.name]})
                else:
                    result.update({"create ": [data['name'], k.name]})
            except Exception as e:
                return Response({"status": "Clusremote error", "message": 'Error: ' + str(e)})
    return result