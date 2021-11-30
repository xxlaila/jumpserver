# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/10 10:39 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.shortcuts import get_object_or_404

from orgs.mixins.api import OrgBulkModelViewSet
from ..hands import IsOrgAdmin
from ..models import Index
from .. import serializers
from common.permissions import (
    IsOrgAdmin, IsOrgAdminOrAppUser,
    CanUpdateDeleteUser, IsSuperUser
)

__all__ = ['IndexViewSet']

class IndexViewSet(OrgBulkModelViewSet):
    model = Index
    filter_fields = ("name",)
    search_fields = filter_fields
    serializer_classes = {
        'default': serializers.IndexSerializer,
    }
    permission_classes = (IsOrgAdmin,)

    def get_queryset(self):
        return super().get_queryset().prefetch_related('metainfo')

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            self.permission_classes = (IsOrgAdminOrAppUser,)
        if self.request.query_params.get('all'):
            self.permission_classes = (IsSuperUser,)
        return super().get_permissions()