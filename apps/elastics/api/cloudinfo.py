# -*- coding: utf-8 -*-
"""
@File    : cloudinfo.py
@Time    : 2021/10/21 10:02 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.shortcuts import get_object_or_404

from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import CloudInfor
from .. import serializers


__all__ = ['CloudInfoViewSet']

class CloudInfoViewSet(OrgBulkModelViewSet):
    model = CloudInfor
    filter_fields = ("name",)
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.CloudInfoSerializer