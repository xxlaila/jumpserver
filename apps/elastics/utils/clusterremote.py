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
from django.http import JsonResponse
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)

@shared_task
@register_as_period_task(interval=600)
def get_cluster_remote():
    try:
        basics = MetaInfo.objects.filter(setting=True)
        obj = []
        for k in basics:
            try:
                data = default_conn.ElasticsAuth(k.name, k.labels).connentauth().cluster.remote_info()
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.ElasticsAuth(k.name, k.labels).connentauth().cluster.remote_info()
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            result = write_cluster_remote(data, k)
            if result:
                obj.append(result)
            else:
                obj.append("error")
        return JsonResponse({"status": obj})
    except MetaInfo.DoesNotExist:
        return False

def write_cluster_remote(results, k):
    if results is not None:
        value = {}
        ack = []
        for key, vaule in results.items():
            data = {"name": key, "mode": vaule["mode"], "conn": vaule["connected"],
                    "conn_timeout": vaule["initial_connect_timeout"],
                    "skip_una": vaule["skip_unavailable"], "seeds": vaule["seeds"],
                    "num_nodes": vaule["num_nodes_connected"],
                    "max_conn": vaule["max_connections_per_cluster"], "proxy_add": "", "metainfo_id": k.id}
            try:
                obj, created = ClusterRemote.objects.update_or_create(name=data['name'], metainfo_id=k.id,
                                                                     defaults=data)
                if obj:
                    ack.append(obj.name)
                value[obj.metainfo.name] = ack
            except Exception as e:
                return ({"status": "Clusremote error", "message": 'Error: ' + str(e)})
        return value
    return False