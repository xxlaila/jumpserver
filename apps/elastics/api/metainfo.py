# -*- coding: utf-8 -*-
"""
@File    : metainfo.py
@Time    : 2021/10/21 11:50 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.shortcuts import get_object_or_404

from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import MetaInfo
from .. import serializers


__all__ = ['MetaInfoViewSet']

class MetaInfoViewSet(OrgBulkModelViewSet):
    model = MetaInfo
    filter_fields = ("name",)
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.MetaInfoSerializer