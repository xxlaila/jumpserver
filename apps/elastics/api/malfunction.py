# -*- coding: utf-8 -*-
"""
@File    : malfunction.py
@Time    : 2021/12/25 9:44 下午
@Author  : xxlaila
@Software: PyCharm
"""
from common.utils import get_logger
from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import Malfunction
from .. import serializers

logger = get_logger(__file__)

__all__ = [
    'MalfunctionViewSet',
]

class MalfunctionViewSet(OrgBulkModelViewSet):
    model = Malfunction
    filter_fields = ("metainfo__name", "name", "metainfo")
    search_fields = ("metainfo__name", "name", "ip")
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.MalfunctionSerializer