# -*- coding: utf-8 -*-
"""
@File    : diskinfo.py
@Time    : 2021/12/23 10:28 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from common.permissions import PermissionsMixin, IsOrgAdmin, IsSuperUser, IsValidUser
from common.utils import get_object_or_none, get_logger
from ..models import AssetExpansion, DiskInfo

__all__ = (
    "DiskInfoListView", "DiskInfoDetailView", "AssetDiskInfoListView",
)
logger = get_logger(__file__)

class DiskInfoListView(PermissionsMixin, TemplateView):
    model = AssetExpansion
    template_name = 'scaling/disk_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Scaling'),
            'action': _('Disk list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AssetDiskInfoListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'scaling/disk_asset_list.html'
    model = AssetExpansion
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Scaling'),
            'action': _('Associate Disk'),
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