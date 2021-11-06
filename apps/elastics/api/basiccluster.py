# -*- coding: utf-8 -*-
"""
@File    : basiccluster.py
@Time    : 2021/10/29 6:01 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework.views import APIView, Response
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from common.utils import get_logger
from common.permissions import IsOrgAdmin, IsOrgAdminOrAppUser
from orgs.mixins.api import OrgBulkModelViewSet
from ..models import BasicCluster
from .. import serializers
from orgs.mixins import generics


logger = get_logger(__file__)
__all__ = ["BasicclusterViewSet", "BasicClusterListApi"]

class BasicclusterViewSet(OrgBulkModelViewSet):
    model = BasicCluster
    filter_fields = ("metainfo__name", "name", "status")
    search_fields = ("metainfo__name", "name", "status")
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.BasicClusterSerializer


class BasicClusterListApi(generics.ListAPIView):
    permission_classes = (IsOrgAdminOrAppUser,)
    serializer_class = serializers.BasicClusterSerializer
    model = BasicCluster

    def get_queryset(self):
        metainfo_id = self.kwargs.get('pk')
        meta = get_object_or_404(BasicCluster, pk=metainfo_id)
        if not meta.metainfo_id:
            return []
        queryset = BasicCluster.objects.filter(metainfo_id=metainfo_id)
        return queryset