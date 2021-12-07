# -*- coding: utf-8 -*-
"""
@File    : clusterconfig.py
@Time    : 2021/12/4 2:33 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, DetailView
)
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from common.permissions import PermissionsMixin, IsOrgAdmin,IsOrgAdminOrAppUser
from ..models import MetaInfo
from common.utils import get_logger

__all__ = (
    "ClusterDynamicConfigView", 
)
logger = get_logger(__name__)

class ClusterDynamicConfigView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/cluster_dynamic_config.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def cluster_data(self):
        data = self.get_object().basiccluster_set.all().first()
        return data

    def get_cluster_setting(self):
        results = self.get_object().clustersetting_set.all().first()
        return results

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Dynamic configuration'),
            'object': self.get_object(),
            'cluster': self.cluster_data(),
            'clustersettings': self.get_cluster_setting(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)