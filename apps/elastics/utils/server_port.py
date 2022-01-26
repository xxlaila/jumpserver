# -*- coding: utf-8 -*-
"""
@File    : server_port.py
@Time    : 2021/10/26 3:32 下午
@Author  : xxlaila
@Software: PyCharm
"""

import socket, sys,os

def server_port_connect(data):
    try:
        server_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_result = server_sk.connect_ex((data[1], int(data[2])))
        if server_result == 0:
            print('%s Port is Open' % (data[1] + ':' + data[2]))
            return True
        else:
            print('%s Port is Not Open' % (data[1] + ':' + data[2]))
            sys.exit(121)
    except socket.error:
        print("error")
        return False

def server_ping(ip):
    backinfo = os.system('ping -c 1 %s' % ip)
    if backinfo == 0:
        print("The network is normal")
        return True
    else:
        print("Connection failed")
        return False