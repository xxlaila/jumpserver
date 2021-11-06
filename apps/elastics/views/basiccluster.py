# -*- coding: utf-8 -*-
"""
@File    : basiccluster.py
@Time    : 2021/10/25 10:54 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, DetailView
)
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from common.permissions import PermissionsMixin, IsOrgAdmin,IsOrgAdminOrAppUser
from ..models import ClusterSetting, ClusterRemote, BasicCluster, MetaInfo
from orgs.mixins import generics
from .. import serializers

__all__ = (
    "BasicClusterListView", "ClusterRemoteListView", "ClusterSettingListView"
)

class BasicClusterListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/basic_cluster_list.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def cluster_data(self, **kwargs):
        data = self.get_object().basiccluster_set.all()
        return data

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Basic cluster list'),
            'object': self.get_object(),
            'cluster': self.cluster_data(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class ClusterRemoteListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/cluster_remote_list.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def cluster_remote_data(self, **kwargs):
        data = self.get_object().clusterremote_set.all()
        return data

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Cluster remote list'),
            'object': self.get_object(),
            'remotes': self.cluster_remote_data(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class ClusterSettingListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/cluster_setting_list.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def default_setting_data(self, **kwargs):
        data = self.get_object().clustersetting_set.all()
        return data

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Cluster setting list'),
            'object': self.get_object(),
            'settings': self.default_setting_data(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/cluster_setting_list.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def node_data(self, **kwargs):
        data = self.get_object().node_set.all()
        return data

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Cluster setting list'),
            'object': self.get_object(),
            'nodes': self.node_data(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)



