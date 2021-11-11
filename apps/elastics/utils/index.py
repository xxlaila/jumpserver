# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/9 5:37 下午
@Author  : xxlaila
@Software: PyCharm
"""

from elasticsearch import TransportError
from ..models import MetaInfo
from ..utils import default_conn, EsConnection
from common.utils import get_logger
import datetime
from ..models import Index
from django.http import JsonResponse

logger = get_logger(__name__)

params = {'bytes': 'gb', 'format': 'json', 'include_unloaded_segments': 'true', 'local': 'false'}

def get_indexs_connent(request, basics=None):
    try:
        obj = {}
        if basics is None:
            basics = MetaInfo.objects.filter(indexes=True)
        for k in basics:
            try:
                data = default_conn.ElasticsAuth(k.name, k.labels).connentauth().cat.indices(
                    index='*-%s' % datetime.datetime.now().strftime('%Y.%m.%d'), params=params)
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.ElasticsAuth(k.name, k.labels).connentauth().cat.nodes(
                        index='*-%s' % datetime.datetime.now().strftime('%Y.%m.%d'), params=params)
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            result = write_indexs_data(data, k)
            if result:
                obj[k.name] = result
        return JsonResponse(obj)
    except Exception as e:
        return False

def write_indexs_data(results, k):
    if results is not None:
        for result in results:
            data = {"name": result['index'], "uuid": result['uuid'], "pri": result['pri'], "rep": result['rep'],
                    "dc": result['docs.count'], "ssize": result['store.size'], "pss": result['pri.store.size'],
                    'health': result['health'], 'status': result['status'], "metainfo_id": k.id}
            try:
                Index.objects.update_or_create(name=data['name'], metainfo_id=k.id, defaults=data)
            except Exception as e:
                logger.error(f'error: {e}')
                raise ValueError("Index error: %s" % result['index'])
        return "seccess"
    return False


def delete_index(datas):
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                      data.metainfo.password).connentauth().indices.delete(index=data.name)
            # default_conn.ElasticsAuth(data.metainfo.name, data.metainfo.labels).connentauth().indices.delete(
            #     index=data.name)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                          data.metainfo.password).connentauth().indices.delete(index=data.name)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            elif e.status_code in [404]:
                return ("%s Index does not exist!" % data.name)
            else:
                raise ValueError("connent timeout")
        if 'acknowledged' in result:
            return "seccess"



