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
def check_setting_connent(request,_settins=None):
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
            # get_indices_breaker(data, k)
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
    bre = jsondata.search_all_value(key='indices')
    nets = jsondata.search_all_value(key='network')
    data.update({"inflight_req_limit": nets[0]['breaker']['inflight_requests']['limit'],
                 "inflight_req": nets[0]['breaker']['inflight_requests']['overhead']})
    data.update({"fielddata_over": bre[4]['breaker']['fielddata']['overhead'],
                 "fielddata_limit": bre[4]['breaker']['fielddata']['limit'],
                 "request_over": bre[0]['breaker']['request']['overhead'],
                 "total_limit": bre[4]['breaker']['total']['limit'],
                 "request_limit": bre[4]['breaker']['request']['limit'], "metainfo_id": k.id})
    if not BreakerConfigNum.objects.filter(status=True, metainfo_id=k.id):
        obj = BreakerConfig.objects.create(**data)
        BreakerConfigNum.objects.create(status=True, metainfo_id=k.id, breakerconfig_id=obj.id)
    return "ok"

def get_routing(results, k):
    jsondata = JsonSearch(object=results, mode='j')
    rout = jsondata.search_all_value(key='routing')
    data = {"node_concurrent_recoveries": rout[0]['allocation']['node_concurrent_recoveries'],
            "cluster_concurrent_rebalance": rout[0]['allocation']['cluster_concurrent_rebalance'],
            "node_initial_primaries_recoveries": rout[0]['allocation']['node_initial_primaries_recoveries'],
            "node_concurrent_outgoing_recoveries": rout[2]['allocation']['node_concurrent_outgoing_recoveries'],
            "disk_watermark_flood_stage": rout[0]['allocation']['disk']['watermark']['flood_stage'],
            "disk_watermark_low": rout[0]['allocation']['disk']['watermark']['low'],
            "disk_watermark_high": rout[0]['allocation']['disk']['watermark']['high'],
            "allow_rebalance": rout[2]['allocation']['allow_rebalance'],
            "allocation_enable": rout[0]['allocation']['enable'],
            "rebalance_enable": rout[2]['rebalance']['enable'],
            "awareness_attributes": rout[2]['allocation']['awareness']['attributes'],
            "balance_index": rout[2]['allocation']['balance']['index'],
            "balance_threshold": rout[2]['allocation']['balance']['threshold'],
            "balance_shard": rout[2]['allocation']['balance']['shard'],
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
