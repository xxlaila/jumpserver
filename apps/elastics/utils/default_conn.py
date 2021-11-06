# -*- coding: utf-8 -*-
"""
@File    : default_conn.py
@Time    : 2021/10/22 2:19 下午
@Author  : xxlaila
@Software: PyCharm
"""


from elasticsearch import Elasticsearch,RequestsHttpConnection
from elasticsearch.transport import Transport
import datetime
import base64, random
from ..models import MetaInfo
from elasticsearch import TransportError


class EsConnection:

    def __init__(self, names, labels):
        cl_inf = self.GetDataAuth(names, labels)
        self.conn_pool = Transport(hosts=cl_inf["address"],  http_auth=(cl_inf['username'], base64.b64decode(cl_inf['password']).decode()), connection_class=RequestsHttpConnection).connection_pool

    def GetDataAuth(self, names, labels):
        data = {}
        try:
            e_infos = MetaInfo.objects.filter(name=names, label=labels).values()
        except MetaInfo.DoesNotExist:
            return False
        for e_info in e_infos:
            data['name'] = e_info['name']
            data['env'] = e_info['env']
            data['address'] = e_info['address']
            data['username'] = e_info['username']
            data['password'] = e_info['password']
            data['labels'] = e_info['labels']
            data['kibana'] = e_info['kibana']
        return data

    def get_conn(self):
        conn = self.conn_pool.get_connection()
        return conn

class ElasticsAuth:

    def __init__(self, names, labels):
        self.names = names
        self.labels = labels

    def GetDataAuth(self):
        data = {}
        try:
            e_infos = MetaInfo.objects.filter(name=self.names, labels=self.labels).values()
            for e_info in e_infos:
                data['name'] = e_info['name']
                data['env'] = e_info['env']
                data['address'] = e_info['address']
                data['username'] = e_info['username']
                data['password'] = e_info['password']
                data['labels'] = e_info['labels']
                data['kibana'] = e_info['kibana']
            return data
        except MetaInfo.DoesNotExist:
            raise ValueError("The cluster does not exist, or the query is wrong")

    def connentauth(self):
        cl_inf = self.GetDataAuth()
        if cl_inf:
            dolphins = Elasticsearch(cl_inf["address"], http_auth=(cl_inf['username'], cl_inf['password']),
                              timeout=10000)
            return dolphins

    def GetIndexsAll(self):
        yesterday = (datetime.date.today()).strftime("%Y.%m.%d")
        inds = self.connentauth().cat.indices(index="*" + '-' + yesterday)
        return inds