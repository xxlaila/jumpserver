# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/10/29 2:17 下午
@Author  : xxlaila
@Software: PyCharm
"""
from elasticsearch import TransportError
from ..models import EsNode, MetaInfo
from ..utils import default_conn
import datetime,time
from django.http import JsonResponse
from common.utils import get_logger
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)

logger = get_logger(__name__)



@shared_task
@register_as_period_task(interval=600)
def get_nodes_connenct(basics=None):
    display = ('id', 'ip', 'name', 'disk.total', 'disk.used', 'disk.avail', 'ram.current', 'ram.percent', 'ram.max',
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
        return ({"status": obj})
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
            data = {"name": result['name'], "ip": result['ip'], "disktotal": result['disk.total'],
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

def get_node_info(datas):
    """
    Node info
    :param datas:
    :return:
    """
    metric = ('process', 'thread_pool', 'os', 'indices', 'settings')
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().nodes.info(
                node_id=data.name, metric=metric)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().nodes.info(
                    node_id=data.name, metric=metric)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            elif e.status_code in [404]:
                return ("%s Index does not exist!" % data.name)
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def get_node_stats(datas):
    """
    Node stats
    :param datas:
    :return:
    """
    metric = ('indices', 'fs', 'breaker', 'process', 'thread_pool')
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().nodes.stats(
                node_id=data.name, metric=metric)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().nodes.stats(
                    node_id=data.name, metric=metric)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            elif e.status_code in [404]:
                return ("%s Index does not exist!" % data.name)
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def exclude_body(data):
    data = {
        "transient": {
            "cluster.routing.allocation.exclude._name": "%s" % data
        }
    }
    return data

def exclude_node(datas, k_head):
    result = ''
    for data in datas:
        old_result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                           data.metainfo.password).connentauth().cluster.get_settings()
        # _name = result['transient']['cluster']['routing']['allocation']['exclude']['_name']
        _ip = old_result['transient']['cluster']['routing']['allocation']['exclude']['ip']
        if k_head == 'online':
            if data.ip in _ip.split(','):
                _ip = _ip.replace(data.ip)
        else:
            _ip = _ip + ''.join(data.ip)
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
        return "seccess"
    else:
        logger.error(result)
        raise ValueError("eroor")