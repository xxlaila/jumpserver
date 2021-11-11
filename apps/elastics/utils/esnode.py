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
        for result in results:
            data = {"name": result['name'], "ip": result['ip'], "disktotal": result['disk.total'],
                    "diskused": result['disk.used'], "diskavail": result['disk.avail'], "ramcurrent": result['ram.current'],
                    "rammax": result['ram.max'], 'noderole': result['nodeRole'], 'pid': result['pid'], 'port': result['port'],
                    "http_address": result['http'], "version": result['version'], 'jdk': result['jdk'],
                    "uptime": result['uptime'], "metainfo_id": k.id}
            try:
                # obj = Node.objects.filter(date_updated__gte=datetime.datetime.now().date(), metainfo_id=k.id, ip=data['ip']).first()
                obj = EsNode.objects.filter(metainfo_id=k.id, ip=data['ip']).first()
                if obj:
                    try:
                        EsNode.objects.filter(id=obj.id).update(**data)
                    except Exception as e:
                        logger.error(f'Update data error: {e}')
                        return ({"status": "EsNode error"})
                else:
                    try:
                        EsNode.objects.create(**data)
                    except Exception as e:
                        logger.error(f'Create data error: {e}')
                        return ({"status": "EsNode error"})
                ack.append(obj.name)
                value[obj.metainfo.name] = ack
            except Exception as e:
                logger.error(f'Error getting result detail with error: {e}')
                return {'Error': 'obj Does Not Exist.'}
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
    metric = ('indices','fs','breaker','process','thread_pool')
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