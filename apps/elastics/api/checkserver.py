# -*- coding: utf-8 -*-
"""
@File    : checkserver.py
@Time    : 2021/11/6 11:33 下午
@Author  : xxlaila
@Software: PyCharm
"""

import socket, sys, os
from rest_framework.views import APIView, Response
from django.views.generic.detail import SingleObjectMixin
from common.permissions import IsOrgAdmin, IsOrgAdminOrAppUser


class ServerPortConnectApi(SingleObjectMixin, APIView):
    permission_classes = (IsOrgAdmin,)
    object = None

    def post(self, request, *args, **kwargs):
        server_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_result = server_sk.connect_ex((args[1], args[2]))
        if server_result == 0:
            return Response("%s Port is Open" % (args[1] + ':' + args[2]))
        else:
            return Response('%s Port is Not Open' % (args[1] + ':' + args[2]))


class ServerPingApi(SingleObjectMixin, APIView):
    permission_classes = (IsOrgAdmin,)
    object = None

    def post(self, request, *args, **kwargs):
        backinfo = os.system('ping -c 1 %s' % self.kwargs['pk'])
        if backinfo == 0:
            return Response("The network is normal")
        else:
            return Response({"error": "Connection failed"}, status=400)