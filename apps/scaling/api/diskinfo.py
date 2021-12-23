# -*- coding: utf-8 -*-
"""
@File    : diskinfo.py
@Time    : 2021/12/18 1:47 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.shortcuts import get_object_or_404
from common.utils import get_logger
from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import DiskInfo
from .. import serializers

logger = get_logger(__file__)

__all__ = [
    'DiskInfoViewSet',
]

class DiskInfoViewSet(OrgBulkModelViewSet):
    model = DiskInfo
    filter_fields = ("assetexpansion__hostname", "diskid", "device", "assetexpansion")
    search_fields = ("assetexpansion__hostname", "diskid", "device",)
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.DiskInfoSerializer