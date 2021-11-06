# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/11/4 5:55 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import EsNode
from orgs.mixins.serializers import BulkOrgResourceModelSerializer


class EsNodeSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = EsNode
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'ip', 'name', 'disktotal', 'org_name', 'diskused', 'diskavail', 'ramcurrent',
            'rammax', 'noderole', 'pid', 'port', 'http_address', 'version', 'jdk', 'uptime', 'metainfo',
            'date_created', 'date_updated'
        ]