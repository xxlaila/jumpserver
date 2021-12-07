# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/9 5:37 下午
@Author  : xxlaila
@Software: PyCharm
"""

from elasticsearch import TransportError, RequestError, ConnectionTimeout
import elasticsearch
from ..models import MetaInfo
from ..utils import default_conn, EsConnection
from common.utils import get_logger
import datetime
from ..models import Index, IndiceShard, EsNode
from django.http import JsonResponse

logger = get_logger(__name__)

params = {'bytes': 'gb', 'format': 'json', 'include_unloaded_segments': 'true', 'local': 'false'}

def get_indexs_connent(basics=None):
    """
    :param request:
    :param basics:
    :return:
    """
    try:
        obj = {}
        if basics is None:
            basics = MetaInfo.objects.filter(indexes=True)
        for k in basics:
            try:
                data = default_conn.EsConnection(k.address, k.username,
                                                   k.password).connentauth().cat.indices(
                    index='*-%s' % datetime.datetime.now().strftime('%Y.%m.%d'), params=params)
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    data = default_conn.EsConnection(k.address, k.username,
                                                   k.password).connentauth().cat.nodes(
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
    """
    :param results:
    :param k:
    :return:
    """
    if results is not None:
        for result in results:
            data = {"name": result['index'], "uuid": result['uuid'], "pri": result['pri'], "rep": result['rep'],
                    "dc": result['docs.count'], "ssize": result['store.size'], "pss": result['pri.store.size'],
                    'health': result['health'], 'status': result['status'], "metainfo_id": k.id}
            try:
                obj, create = Index.objects.update_or_create(name=data['name'], metainfo_id=k.id, defaults=data)
            except Exception as e:
                logger.error(f'error: {e}')
                raise ValueError("Index error: %s" % result['index'])
        return "seccess"
    return False

def index_shards_num(data):
    params = {'bytes': 'gb', 'format': 'json'}
    display = ('id', 's', 'i', 'p', 'st', 'dc', 'sto', 'ip', 'node', 'ur', 'ud')
    try:
        shards = default_conn.EsConnection(
            data.metainfo.address, data.metainfo.username, data.metainfo.password).connentauth().cat.shards(
            index=data.name, h=display, params=params, ignore=['404'])
    except TransportError as e:
        if e.status_code in [503, 502, 500]:
            shards = default_conn.EsConnection(
                data.metainfo.address, data.metainfo.username, data.metainfo.password).connentauth().cat.shards(
                index=data.name, h=display, params=params, ignore=['404'])
        elif e.status_code in [401]:
            raise ValueError("Incorrect account password")
        elif e.status_code in [404]:
            return ("%s Index does not exist!" % data.name)
        else:
            raise ValueError("connent timeout")
    return shards


def delete_index(datas):
    """
    delete index
    :param datas:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                      data.metainfo.password).connentauth().indices.delete(index=data.name)
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

def create_index(data, index_name, body=None):
    """
    :param data:
    :param index_name:
    :param body:
    :return:
    """
    print(data, index_name)
    try:
        default_conn.EsConnection(data.address, data.username, data.password).connentauth().indices.create(
            index=index_name, body=body, ignore=[400])
    except RequestError as e:
        if e.status_code in [503, 502, 500]:
            default_conn.EsConnection(data.address, data.username, data.password).connentauth().indices.create(
                index=index_name, body=body, ignore=[400])
    except ConnectionTimeout:
        raise ValueError("connent timeout")
    except elasticsearch.AuthenticationException:
        raise ValueError("Incorrect account password")
    else:
        return ("%s already exists" % index_name)

def close_index(datas):
    """
    close index
    :param datas:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.close(index=data.name, ignore=[400, 404])
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().indices.close(index=data.name, ignore=[400, 404])
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def open_index(datas):
    """
    open index
    :param datas:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.open(index=data.name)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().indices.open(index=data.name)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def freeze_index(datas):
    """
    Freeze index
    :param datas:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.freeze(index=data.name)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().indices.freeze(index=data.name)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def unfreeze_index(datas):
    """
    UnFreeze index
    :param datas:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.unfreeze(index=data.name)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().index.unfreeze(index=data.name)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def put_settings_index(datas, body):
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.put_settings(
                index=data.name, body=body)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().indices.put_settings(
                    index=data.name, body=body)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            elif e.status_code in [404]:
                return ("%s Index does not exist!" % data.name)
            else:
                raise ValueError("connent timeout")
        if result:
            pass

def create_templates(datas, template_name, params):
    """
    create templates
    :param datas:
    :param template_name:
    :param params:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.put_template(
                name=template_name, params=params)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().indices.put_template(
                    name=template_name, params=params)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            else:
                raise ValueError("connent timeout")
        if result:
            pass


def delete_templates(datas, template_name):
    """
    delete template
    :param datas:
    :param template_name:
    :return:
    """
    for data in datas:
        try:
            result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                               data.metainfo.password).connentauth().indices.delete_template(
                name=template_name)
        except TransportError as e:
            if e.status_code in [503, 502, 500]:
                result = default_conn.EsConnection(data.metainfo.address, data.metainfo.username,
                                                   data.metainfo.password).connentauth().indices.delete_template(
                    name=template_name)
            elif e.status_code in [401]:
                raise ValueError("Incorrect account password")
            else:
                raise ValueError("connent timeout")
        if result:
            pass

