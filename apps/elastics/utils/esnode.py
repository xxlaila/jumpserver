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
import logging
from celery import shared_task
from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start, after_app_shutdown_clean_periodic
)

display = ('id', 'ip', 'name', 'disk.total', 'disk.used', 'disk.avail', 'ram.current', 'ram.percent', 'ram.max',
           'cpu', 'hp', 'fm', 'sm', 'sc', 'qcm', 'sqti', 'uptime', 'pid', 'nodeRole', 'jdk', 'port', 'http',
           'version'
          )
params = {'format': 'json', 'full_id': 'true', 'master_timeout': '180s', 'bytes': 'gb'}

@shared_task
@register_as_period_task(interval=600)
def get_nodes_connenct(request):
    try:
        basics = MetaInfo.objects.filter(node=True)
        for k in basics:
            try:
                data = default_conn.ElasticsAuth(k.name, k.labels).connentauth().cat.nodes(
                    h=display, params=params)
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.ElasticsAuth(k.name, k.labels).connentauth().cat.nodes(
                        ph=display, params=params)
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            write_node_params(data, k)
            # return data, k
    except MetaInfo.DoesNotExist:
        return False

def write_node_params(results, k):
    if results is not None:
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
                    EsNode.objects.filter(id=obj.id).update(**data)
                else:
                    EsNode.objects.create(**data)
            except Exception as e:
                logging.error("Node error")
                raise ValueError(e)
    return False