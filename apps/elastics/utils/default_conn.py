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

    def __init__(self, address, user, pwd):
        self.address = address
        self.user = user
        self.pwd = pwd

    def connentauth(self):
        # conn_pool = Transport(hosts=self.address, http_auth=(self.user, self.pwd),
        #                                connection_class=RequestsHttpConnection).connection_pool
        conn_pool = Elasticsearch(hosts=self.address, http_auth=(self.user, self.pwd), timeout=100000)
        return conn_pool

class EsConnectionPool:

    def __init__(self):
        pass

    def get_cluster(self):
        ELASTICSEARCH = {}
        for data in MetaInfo.objects.all():
            ELASTICSEARCH.update({
                data.name: {
                    'hosts': [
                        {
                            'host': data.address.split(':')[0],
                            'port': data.address.split(':')[-1],
                            'verify_certs': False,
                            'use_ssl': False,
                            'http_auth': (
                                data.username,
                                data.password
                            )
                        }
                    ]
                }
            })

        return ELASTICSEARCH

