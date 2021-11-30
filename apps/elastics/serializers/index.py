# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/10 10:36 上午
@Author  : xxlaila
@Software: PyCharm
"""
from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from common.mixins import BulkSerializerMixin
from ..models import Index, IndiceShard
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from rest_framework import serializers

__all__ = [
    'IndexSerializer',
]

class IndexSerializer(BulkOrgResourceModelSerializer):

    metainfo_display = serializers.CharField(source='metainfo.name')

    class Meta:
        model = Index
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'uuid', 'pri', 'rep', 'dc', 'ssize',
            'pss', 'health', 'status', 'metainfo', 'metainfo_display', 'date_updated'
        ]

