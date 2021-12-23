# -*- coding: utf-8 -*-
"""
@File    : assetexpansion.py
@Time    : 2021/12/17 2:30 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from common.permissions import PermissionsMixin, IsOrgAdmin, IsSuperUser, IsValidUser
from django.shortcuts import get_object_or_404, reverse
from common.const import create_success_msg, update_success_msg
from common.utils import get_object_or_none, get_logger

from ..models import AssetExpansion,DiskInfo

__all__ = (
    "AssetExpansionListView", "AssetExpansionDetailView", "DiskInfoListView",
    "DiskInfoDetailView",
)
logger = get_logger(__file__)

class AssetExpansionListView(PermissionsMixin, TemplateView):
    model = AssetExpansion
    template_name = 'scaling/assets_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Scaling'),
            'action': _('Assets list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AssetExpansionDetailView(PermissionsMixin, DetailView):
    model = AssetExpansion
    template_name = 'scaling/asset_detail.html'
    permission_classes = [IsOrgAdmin, IsValidUser]

    def secur(self):
        security = self.get_object(queryset=self.model.objects.all().values('security'))
        return security['security']

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Scaling'),
            'action': _('Assets detail'),
            'security': self.secur(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DiskInfoListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'scaling/disk_list.html'
    model = AssetExpansion
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Scaling'),
            'action': _('Disk list'),
            'object': self.get_object(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DiskInfoDetailView(PermissionsMixin, DetailView):
    model = DiskInfo
    template_name = 'scaling/disk_detail.html'
    permission_classes = [IsOrgAdmin]
    object = None

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Scaling'),
            'action': _('Disk detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)