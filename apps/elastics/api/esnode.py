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
from ..models import EsNode, IndiceNode
from .. import serializers

logger = get_logger(__file__)

__all__ = [
    'EsNodeViewSet', 'IndiceNodeViewSet'
]

class EsNodeViewSet(OrgBulkModelViewSet):
    model = EsNode
    filter_fields = ("metainfo__name", "name", "ip", "metainfo")
    search_fields = ("metainfo__name", "name", "ip")
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.EsNodeSerializer


class IndiceNodeViewSet(OrgBulkModelViewSet):
    model = IndiceNode
    filter_fields = ("esnode__name", "esnode")
    search_fields = ("esnode__name")
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.IndiceNodeSerializer

