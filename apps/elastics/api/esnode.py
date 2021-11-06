# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/11/4 5:53 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.shortcuts import get_object_or_404
from common.utils import get_logger
from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import EsNode
from .. import serializers

logger = get_logger(__file__)

__all__ = [
    'EsNodeViewSet'
]

# class EsNodeViewSet(OrgBulkModelViewSet):
#     model = EsNode
#     filter_fields = ("name", "ip")
#     search_fields = filter_fields
#     permission_classes = (IsOrgAdmin,)
#     serializer_class = serializers.EsNodeSerializer


class EsNodeViewSet(OrgBulkModelViewSet):
    model = EsNode
    filter_fields = ("metainfo__name", "name", "ip", "metainfo")
    search_fields = ("metainfo__name", "name", "ip")
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.EsNodeSerializer
