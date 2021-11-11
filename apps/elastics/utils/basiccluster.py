# -*- coding: utf-8 -*-
"""
@File    : basiccluster.py
@Time    : 2021/10/29 2:16 下午
@Author  : xxlaila
@Software: PyCharm
"""

from elasticsearch import TransportError
from rest_framework.views import Response
from ..models import BasicCluster, MetaInfo, ClusterRemote,ClusterSetting
from ..utils import default_conn
import datetime,time,json
import logging
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)

@shared_task
@register_as_period_task(interval=600)
def get_default_setting(basics=None):
    try:
        obj = []
        if basics is None:
            basics = MetaInfo.objects.filter(setting=True)
        for k in basics:
            try:
                data = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.stats()
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.stats()
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            result = write_default_setting(data, k)
            if result:
                obj.append(result)
            else:
                obj.append("error")
        return Response({"status": obj})
    except MetaInfo.DoesNotExist:
        return False

def write_default_setting(results, k):
    if results is not None:
        ack = {}
        node = results["nodes"]["count"]
        mem = results["nodes"]["os"]["mem"]
        indi = results["indices"]
        data = {"name": results['cluster_name'], "status": results['status'], "st": indi['shards']['total'],
                "sp": indi['shards']['primaries'], "incount": indi['count'], "indocs": indi['docs']['count'],
                "instore": indi['store']['size_in_bytes'], "nt": node['total'], 'nc': node['coordinating_only'],
                'nd': node['data'], 'ni': node['ingest'], "nm": node['master'], "nr": node['remote_cluster_client'],
                'mt': mem['total_in_bytes'], "mf": mem['free_in_bytes'], 'mu': mem['used_in_bytes'],
                'pt': results['nodes']['packaging_types'], "metainfo_id": k.id}
        try:
            obj = BasicCluster.objects.filter(date_updated__gte=datetime.datetime.now().date(),
                                              metainfo_id=k.id).first()
            if obj:
                BasicCluster.objects.filter(id=obj.id).update(**data)
                ack.update({"update ": obj.name})
            else:
                BasicCluster.objects.create(**data)
                ack.update({"create  ": obj.name})
        except Exception as e:
            logging.error("Clubrief error")
            raise ValueError(e)
        return ack
    return False

@shared_task
@register_as_period_task(interval=600)
def check_setting_connent(_settins=None):
    try:
        obj = []
        if _settins is None:
            _settins = MetaInfo.objects.filter(setting=True)
        for k in _settins:
            try:
                data = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.get_settings(
                    include_defaults='true')
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.EsConnection(
                        k.address, k.username, k.password).connentauth().cluster.get_settings(include_defaults='true')
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            result = get_check_setting_data(data, k)
            if result:
                obj.append(result)
            else:
                obj.append("error")
        return Response({"status": obj})
    except MetaInfo.DoesNotExist:
        return False

def get_check_setting_data(results, k):
    f_data = {"persis": results["persistent"], "tran": results["transient"],
              "def_clus": results["defaults"]["cluster"],
              "def_xpack": results["defaults"]["xpack"]["flattened"],
              "metainfo_id": k.id}
    try:
        data = ClusterSetting.objects.filter(metainfo_id=k.id).first()
        if data:
            ClusterSetting.objects.filter(id=data.id).update(**f_data)
        else:
            ClusterSetting.objects.create(**f_data)
        return Response({"status": "%s update success" % k.name})
    except Exception as e:
        logging.error("Settinginfo error")
        raise ValueError(e)

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
                    return Response({"status": "%s update success: %s" % (data['name'], obj)})
            except Exception as e:
                return Response({"status": "Clusremote error", "message": 'Error: ' + str(e)})
    return False
