# -*- coding: utf-8 -*-
"""
@File    : assetexpansion.py
@Time    : 2021/12/17 2:20 下午
@Author  : xxlaila
@Software: PyCharm
"""
from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import AssetExpansion
from .. import serializers


__all__ = ['AssetExpansionViewSet']

class AssetExpansionViewSet(OrgBulkModelViewSet):
    model = AssetExpansion
    filter_fields = ("hostname", "instance", "primaryip")
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.AssetExpansionSerializer