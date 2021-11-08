# -*- coding: utf-8 -*-
"""
@File    : basiccluster.py
@Time    : 2021/10/29 5:59 下午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework import serializers

from common.serializers import AdaptedBulkListSerializer
from orgs.mixins.serializers import BulkOrgResourceModelSerializer

from ..models import BasicCluster

class BasicClusterSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = BasicCluster
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'status', 'st', 'sp', 'incount', 'indocs','instore',
            'nt', 'nc', 'nd', 'ni', 'nm', 'nr', 'mt', 'mf', 'mu', 'pt', 'metainfo',
            'date_updated'
        ]