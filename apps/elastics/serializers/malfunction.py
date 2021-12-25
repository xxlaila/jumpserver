# -*- coding: utf-8 -*-
"""
@File    : malfunction.py
@Time    : 2021/12/25 9:37 下午
@Author  : xxlaila
@Software: PyCharm
"""

from common.serializers import AdaptedBulkListSerializer
from ..models import Malfunction
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from rest_framework import serializers

class MalfunctionSerializer(BulkOrgResourceModelSerializer):
    metainfo_base = serializers.ReadOnlyField()

    class Meta:
        model = Malfunction
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'org_name', 'comment', 'status', 'metainfo_base'
            'metainfo', 'date_created', 'created_by'
        ]