# -*- coding: utf-8 -*-
"""
@File    : health.py
@Time    : 2021/10/29 2:17 下午
@Author  : xxlaila
@Software: PyCharm
"""
import re,json
from ..models import MetaInfo
from elasticsearch import TransportError
from ..utils import default_conn
from ..utils.feishualter import FeishuAlter
from django.conf import settings
from .check_node import *


def dataalter(*args):
    title = "%s cluster status" % args[0][0]
    result_list = []
    result_list.append(
        [{"tag": "a", "text": "Cluster name: %s" % args[0][0], "href": args[0][1]}])
    result_list.append([{"tag": "text", "text": "Cluster status: %s" % args[0][4]}])
    result_list.append([{"tag": "text", "text": "Cluster env: %s" % args[0][2]}])
    result_list.append([{"tag": "text", "text": "Cloud: %s" % args[0][3]}])
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "en_us": {
                    "title": settings.FEISHU['KEY_WORDS'] + title,
                    "content": result_list
                }
            }
        }
    }
    FeishuAlter().SendMessage(message)

def check_health():
    params = {'format': 'json'}
    try:
        healths = MetaInfo.objects.filter(health=True)
        for k in healths:
            try:
                results = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.health(
                    params=params)
            except TransportError as e:
                if e.status_code in [503, 502, 500]:
                    results = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.health(
                        params=params)
                elif e.status_code in [401]:
                    raise ValueError("Incorrect account password")
                else:
                    raise ValueError("connent timeout")
            if results['status'] == 'green':
                data = [k.name, k.kibana, k.env, k.cloud.name, results['status']]
            elif results['status'] == 'yellow':
                data = [k.name, k.kibana, k.env, k.cloud.name, results['status']]
                EsProcessCheck().get_health(k,results)
            else:
                data = [k.name, k.kibana, k.env, k.cloud.name, results['status']]
            if data:
                dataalter(data)
    except MetaInfo.DoesNotExist:
        return
