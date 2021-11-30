# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/10/29 2:17 下午
@Author  : xxlaila
@Software: PyCharm
"""
from elasticsearch import TransportError
from ..models import EsNode, MetaInfo, IndiceNode, IndiceShard, NodeFs, Index
from ..utils import default_conn
import datetime,time
from common.utils import get_logger
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)
from rest_framework.views import Response

logger = get_logger(__name__)

@shared_task
@register_as_period_task(interval=600)
def get_nodes_connenct(basics=None):
    display = ('id', 'ip', 'name','disk.total', 'disk.used', 'disk.avail', 'ram.current', 'ram.percent', 'ram.max',
               'cpu', 'hp', 'fm', 'sm', 'sc', 'qcm', 'sqti', 'uptime', 'pid', 'nodeRole', 'jdk', 'port', 'http',
               'version'
               )
    params = {'format': 'json', 'full_id': 'true', 'master_timeout': '180s', 'bytes': 'gb'}
    try:
        obj = []
        if basics is None:
            basics = MetaInfo.objects.filter(node=True)
        for k in basics:
            try:
                data = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cat.nodes(
                    h=display, params=params)
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cat.nodes(
                        h=display, params=params)
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            obj.append(write_node_params(data, k))
        return Response({"status": obj}, status=200)
    except MetaInfo.DoesNotExist:
        return False

def write_node_params(results, k):
    if results is not None:
        value = {}
        ack = []
        old_ip = []
        old_result = EsNode.objects.filter(metainfo_id=k.id).values('ip')
        for old in old_result:
            old_ip.append(old['ip'])
        for result in results:
            data = {"name": result['name'], "uuid": result["id"], "ip": result['ip'], "disktotal": result['disk.total'],
                    "diskused": result['disk.used'], "diskavail": result['disk.avail'], "ramcurrent": result['ram.current'],
                    "rammax": result['ram.max'], 'noderole': result['nodeRole'], 'pid': result['pid'], 'port': result['port'],
                    "http_address": result['http'], "version": result['version'], 'jdk': result['jdk'],
                    "uptime": result['uptime'], "status": True, "metainfo_id": k.id}
            if data['ip'] in old_ip:
                old_ip.remove(data['ip'])
            try:
                obj, create = EsNode.objects.update_or_create(metainfo_id=k.id, defaults=data, ip=data['ip'])
                if obj:
                    ack.append(obj.name)
                    value[obj.metainfo.name] = ack
            except Exception as e:
                logger.error(f'error: {e}')
                raise ValueError("EsNode error: %s" % data['ip'])
        if old_ip:
            for ele in old_ip:
                EsNode.objects.filter(metainfo_id=k.id, ip=ele).update(status=False)
        return value
    return False

def get_node_stats(datas):
    """
    Node stats
    :param datas:
    :return:
    """
    metric = ('fs', 'indices')
    index_metric = ('docs', 'store', 'recovery', 'refresh', 'flush')
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().nodes.stats(
                    node_id=data.name, metric=metric, index_metric=index_metric, level='indices')
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().nodes.stats(
                    node_id=data.name, metric=metric, index_metric=index_metric, level='indices')
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            elif e.status_code in [404]:
                return ("%s Index does not exist!" % data.name)
            else:
                raise ValueError("connent timeout")
        if result:
            for i in result['nodes']:
                for k, v in result['nodes'][i]['indices']['indices'].items():
                    if datetime.datetime.now().strftime('%Y.%m.%d') in k:
                        try:
                            inds = Index.objects.get(name=k, metainfo_id=data.metainfo.id)
                            if inds:
                                ojb = {"esnode_id": data.id, "index_id": inds.id, "refresh": v['refresh']['total'],
                                   "flush": v['flush']['total'], "recovery": v['recovery']['current_as_source']}
                                obj, create = IndiceNode.objects.update_or_create(
                                    esnode_id=data.id, index_id=inds.id, defaults=ojb)
                        except Exception as e:
                            print(e)
        else:
            return str(result)

def exclude_body(data):
    result = {
        "transient": {
            "cluster.routing.allocation.exclude._ip": "%s" % data
        }
    }
    return result

def find_json_key(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_json_key(key, v):
                yield result

def exclude_node(data):
    result = ''
    _ip = ''
    old_result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                           data.metainfo.password).connentauth().cluster.get_settings()
    # _ip = old_result['transient']['cluster']['routing']['allocation']['exclude']['_ip']
    if 'transient' in old_result.keys():
        for my_element in find_json_key('_ip', old_result['transient']):
            if data.ip == my_element:
                _ip = ''
            elif data.ip in my_element:
                _ip = _ip.pattern(data.ip)
            else:
                _ip = data.ip
    else:
        _ip = data.ip
    try:
        result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                           data.metainfo.password).connentauth().cluster.put_settings(
            body=exclude_body(_ip))
    except TransportError as e:
        if e.status_code in [503, 502, 500]:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().cluster.put_settings(
                body=exclude_body(_ip))
    if 'acknowledged' in result:
        return True, None
    else:
        return False, str(result)