# -*- coding: utf-8 -*-
"""
@File    : metainfo.py
@Time    : 2021/10/21 11:46 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import MetaInfo
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from rest_framework import serializers

class MetaInfoSerializer(BulkOrgResourceModelSerializer):
    cloud_base = serializers.ReadOnlyField()

    class Meta:
        model = MetaInfo
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'env', 'org_name', 'address', 'username',
            'password', 'kibana', 'kafka', 'cloud', 'cloud_base', 'labels', 'comment',
            'health', 'setting', 'alter', 'indexes', 'node', 'remote', 'scbcl',
            'created_by', 'date_created'
        ]

        extra_kwargs = {
            'address': {'required': True},
            'name': {'required': False},
        }

class MetaInfoTaskSerializer(serializers.Serializer):
    ACTION_CHOICES = (
        ('refresh', 'refresh'),
        ('test', 'test'),
    )
    task = serializers.CharField(read_only=True)
    action = serializers.ChoiceField(choices=ACTION_CHOICES, write_only=True)

