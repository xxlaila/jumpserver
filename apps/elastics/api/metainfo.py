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
from orgs.mixins import generics
from ..tasks import (
    test_mete_info_network_manual, test_mete_info_port_manual
)


__all__ = ['MetaInfoViewSet',
           'MetaInfoTaskCreateApi'
           ]

class MetaInfoViewSet(OrgBulkModelViewSet):
    model = MetaInfo
    filter_fields = ("name",)
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.MetaInfoSerializer


class MetaInfoTaskCreateApi(generics.CreateAPIView):
    model = MetaInfo
    serializer_class = serializers.MetaInfoTaskSerializer
    permission_classes = (IsOrgAdmin,)

    def get_object(self):
        pk = self.kwargs.get("pk")
        instance = get_object_or_404(MetaInfo, pk=pk)
        return instance

    def perform_create(self, serializer):
        metainfo = self.get_object()
        action = serializer.validated_data["action"]
        if action == "refresh":
            task = test_mete_info_network_manual(metainfo)
        else:
            task = test_mete_info_port_manual(metainfo)
        data = getattr(serializer, '_data', {})
        if task == True:
            data["task"] = task
        else:
            data["task"] = task.id
        setattr(serializer, '_data', data)