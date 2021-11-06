# -*- coding: utf-8 -*-
"""
@File    : server_port.py
@Time    : 2021/10/26 3:32 下午
@Author  : xxlaila
@Software: PyCharm
"""

import socket, sys,os

def server_port_connect(*args):
    print("1")
    server_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_result = server_sk.connect_ex((args[1], args[2]))
    print(server_result)
    if server_result == 0:
        print('%s Port is Open' % (args[1] + ':' + args[2]))
    else:
        print ('%s Port is Not Open' % (args[1] + ':' + args[2]))
        sys.exit(121)

def server_ping(ip):
    backinfo = os.system('ping -c 1 %s' % ip)
    if backinfo == 0:
        print("The network is normal")
    else:
        print("Connection failed")
