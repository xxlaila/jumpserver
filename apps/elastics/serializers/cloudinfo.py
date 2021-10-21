# -*- coding: utf-8 -*-
"""
@File    : cloudinfo.py
@Time    : 2021/10/21 10:03 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import CloudInfor
from orgs.mixins.serializers import BulkOrgResourceModelSerializer


class CloudInfoSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = CloudInfor
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'value', 'org_name', 'key', 'secret', 'comment',
            'created_by', 'date_created', 'date_updated'
        ]

        extra_kwargs = {
            'secret': {'required': True},
            'name': {'required': False},
        }
