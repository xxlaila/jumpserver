# -*- coding: utf-8 -*-
"""
@File    : check_node.py
@Time    : 2021/11/19 1:38 下午
@Author  : xxlaila
@Software: PyCharm
"""

from elasticsearch import Elasticsearch,RequestsHttpConnection
from elasticsearch.transport import Transport
import datetime
from elasticsearch import TransportError
import shlex
import datetime
import subprocess
import time
import json, requests
import socket, threading
from ..utils import default_conn
from ..models import EsNode, MetaInfo
from ..utils import health

class EsProcessCheck:

    def __init__(self):
    #     # self.conn_pool = Transport(hosts=address, http_auth=(user, pwd), connection_class=RequestsHttpConnection).connection_pool
    #     self.conn_pool = Elasticsearch(hosts=address, http_auth=(user, pwd), timeout=100000)
        self.params = {'format': 'json'}
        self.display = ('ip')
        self.command = 'sudo systemctl start elasticsearch'

    def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
        end_time = ''
        if shell:
            cmdstring_list = cmdstring
        else:
            cmdstring_list = shlex.split(cmdstring)
        if timeout:
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        sub = subprocess.Popen(cmdstring_list, cwd=cwd, shell=shell, bufsize=4096, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while sub.poll() is None:
            time.sleep(0.1)
            if timeout:
                if end_time <= datetime.datetime.now():
                    raise Exception("Timeout：%s" % cmdstring)
        return str(sub.returncode)

    def scoketconnet(self, addr, port):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1000)
        try:
            sk.connect((addr, int(port)))
        except socket.error as e:
            return ('%s Down, restarting, please wait' % addr)
        sk.close()

    def get_health(self, k, results):
        old_data = []
        new_data = []
        node_res = EsNode.objects.filter(metainfo_id=(MetaInfo.objects.get(name=k.name)).id)
        node_news = default_conn.EsConnection(k.address, k.username, k.password).connentauth().cat.nodes(
            h=self.display, params=self.params)
        for node_re in node_res:
            old_data.append(node_re.ip)
        for node_new in node_news:
            new_data.append(node_new['ip'])
        if results['status'] in ['yellow'] and results['relocating'] == 0 and results['unassigned'] > 0:
            default_conn.EsConnection(k.address, k.username, k.password).connentauth().cluster.reroute(
                params={"retry_failed": "true"})
        elif results['status'] in ['red']:
            if results['number_of_nodes'] != len(old_data):
                for i in list(set(old_data).difference(new_data)):
                    ports = self.scoketconnet(i, '39900')
                    if ports is not None:
                        data = [k.name, k.kibana, k.env, k.cloud.name, ports]
                        health.dataalter(data)
                        self.execute_command("ssh -P56358 user@%s " % i + self.command)
                        time.sleep(3000)
                        ports = self.scoketconnet(i, '39900')
                        if ports is not None:
                            data = [k.name, k.kibana, k.env, k.cloud.name, ports]
                            health.dataalter(data)
        else:
            pass
