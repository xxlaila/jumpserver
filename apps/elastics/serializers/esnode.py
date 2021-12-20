# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/11/4 5:55 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import EsNode, IndiceNode
from orgs.mixins.serializers import BulkOrgResourceModelSerializer

class EsNodeSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = EsNode
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'ip', 'name', 'disktotal', 'org_name', 'diskused', 'diskavail', 'ramcurrent',
            'rammax', 'noderole', 'pid', 'port', 'http_address', 'version', 'jdk', 'status', 'uptime', 'metainfo',
            'date_created', 'date_updated'
        ]
        
class IndiceNodeSerializer(BulkOrgResourceModelSerializer):
    
    class Meta:
        model = IndiceNode
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'esnode', 'index', 'refresh', 'flush', 'recovery', 'org_name',
            'date_created', 'date_updated'
        ]

