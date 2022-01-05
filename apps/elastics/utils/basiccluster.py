# -*- coding: utf-8 -*-
"""
@File    : basiccluster.py
@Time    : 2021/10/29 2:16 下午
@Author  : xxlaila
@Software: PyCharm
"""

from elasticsearch import TransportError
from rest_framework.views import Response
from ..models import BasicCluster, MetaInfo, ClusterRemote,ClusterSetting,BreakerConfigNum,\
    BreakerConfig,RoutingConfigNum,RoutingConfig
from ..utils import default_conn
import datetime,time,json
import logging
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)
from jsonsearch import JsonSearch

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
        return Response({"status": obj}, status=200)
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
                'pt': results['nodes']['packaging_types'][0]['type'], "metainfo_id": k.id}
        try:
            obj = BasicCluster.objects.filter(
                date_updated__gte=datetime.datetime.now().date(), metainfo_id=k.id).first()
            if obj:
                BasicCluster.objects.filter(id=obj.id).update(**data)
                ack.update({"update ": obj.name})
            else:
                BasicCluster.objects.create(**data)
                ack.update({"create  ": results['cluster_name']})
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
            get_indices_breaker(data, k)
            get_routing(data, k)
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
              "def_xpack": results["defaults"]["indices"],
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

def get_indices_breaker(results, k):
    data = {}
    jsondata = JsonSearch(object=results, mode='j')
    data.update({"inflight_req_limit":
                     list(filter(None, [i.get('limit') for i in jsondata.search_all_value(key='inflight_requests')]))[
                         0],
                 "inflight_req": list(
                     filter(None, [i.get('overhead') for i in jsondata.search_all_value(key='inflight_requests')]))[0],
                 "fielddata_over":
                     list(filter(None, [i.get('overhead') for i in jsondata.search_all_value(key='fielddata')]))[0],
                 "fielddata_limit":
                     list(filter(None, [i.get('limit') for i in jsondata.search_all_value(key='fielddata')]))[0],
                 "request_over":
                     list(filter(None, [i.get('overhead') for i in jsondata.search_all_value(key='request')]))[0],
                 "request_limit":
                     list(filter(None, [i.get('limit') for i in jsondata.search_all_value(key='request')]))[0],
                 "total_limit": list(filter(None, [i.get('limit') for i in jsondata.search_all_value(key='total')]))[0],
                 "metainfo_id": k.id
                 })
    if not BreakerConfigNum.objects.filter(status=True, metainfo_id=k.id):
        obj = BreakerConfig.objects.create(**data)
        BreakerConfigNum.objects.create(status=True, metainfo_id=k.id, breakerconfig_id=obj.id)
    return "ok"

def get_routing(results, k):
    jsondata = JsonSearch(object=results, mode='j')
    # "allocation_enable": list(filter(None, [i.get('enable') for i in jsondata.search_all_value(key='allocation')]))[0],
    data = {"node_concurrent_recoveries": jsondata.search_all_value(key='node_concurrent_recoveries')[0],
            "cluster_concurrent_rebalance": jsondata.search_all_value(key='cluster_concurrent_rebalance')[0],
            "node_initial_primaries_recoveries": jsondata.search_all_value(key='node_initial_primaries_recoveries')[0],
            "node_concurrent_outgoing_recoveries": jsondata.search_all_value(key='node_concurrent_outgoing_recoveries')[0],
            "disk_watermark_flood_stage": jsondata.search_all_value(key='flood_stage')[0],
            "disk_watermark_low": jsondata.search_all_value(key='low')[0],
            "disk_watermark_high": jsondata.search_all_value(key='high')[0],
            "allow_rebalance": jsondata.search_all_value(key='allow_rebalance')[0],
            "allocation_enable": 'all',
            "rebalance_enable": jsondata.search_all_value(key='rebalance')[0]['enable'],
            "awareness_attributes": jsondata.search_all_value(key='attributes')[0],
            "balance_index": jsondata.search_all_value(key='balance')[0]['index'],
            "balance_threshold": jsondata.search_all_value(key='balance')[0]['threshold'],
            "balance_shard": jsondata.search_all_value(key='balance')[0]['shard'],
            "metainfo_id": k.id
            }
    if not RoutingConfigNum.objects.filter(status=True, metainfo_id=k.id):
        obj = RoutingConfig.objects.create(**data)
        RoutingConfigNum.objects.create(status=True, metainfo_id=k.id, routingConfig_id=obj.id)
    return "ok"

def put_settings_cluster(data, body):
    """
    edit cluster settings
    :param datas:
    :param body:
    :return:
    """
    try:
        default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                           data.metainfo.password).connentauth().cluster.put_settings(
            body=body)
    except TransportError as e:
        if e.status_code in [503, 502, 500]:
            default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().cluster.put_settings(
                body=body)
        elif e.status_code in [401]:
            raise ValueError("Incorrect account password")
        else:
            raise ValueError("connent timeout")
        
    return True
