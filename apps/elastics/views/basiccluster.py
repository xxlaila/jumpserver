# -*- coding: utf-8 -*-
"""
@File    : basiccluster.py
@Time    : 2021/10/25 10:54 上午
@Author  : xxlaila
@Software: PyCharm
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, DetailView
)
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from common.permissions import PermissionsMixin, IsOrgAdmin,IsOrgAdminOrAppUser
from ..models import ClusterSetting, ClusterRemote, BasicCluster, MetaInfo
from orgs.mixins import generics
from .. import serializers
from common.utils import get_logger
from common.const import create_success_msg, update_success_msg
from django.urls import reverse_lazy
from rest_framework.views import APIView, Response
from django.shortcuts import (
    render, redirect
)
from ..utils import get_default_setting,check_setting_connent, cluster_remote_connent

__all__ = (
    "BasicClusterListView", "ClusterRemoteListView", "ClusterSettingListView",
    "ClusterRemoteInfoUpdateView", "DefaultSettingsUpdateView", "BasicClusterUpdateView"
)
logger = get_logger(__name__)

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

    def get_cluster_setting(self):
        # results = self.get_object().clustersetting_set.all().values('persis', 'tran', 'def_clus', 'def_xpack')
        results = self.get_object().clustersetting_set.all()
        return results

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Basic cluster list'),
            'object': self.get_object(),
            'cluster': self.cluster_data(),
            'clustersettings': self.get_cluster_setting(),
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

class BasicClusterUpdateView(SingleObjectMixin, APIView):
    model = MetaInfo
    success_url = reverse_lazy('elastics:basic-cluster-list')
    template_name = 'elastics/basic_cluster_list.html'
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_object1(self, k):
        result = self.model.objects.filter(id=k, setting=True)
        return result

    def get(self, request, *args, **kwargs):
        try:
            try:
                obj = self.get_object1(self.kwargs['pk'])
                if obj:
                    get_default_setting(obj)
                    check_setting_connent(obj)
            except MetaInfo.DoesNotExist:
                return Response({'Error': 'obj Does Not Exist.'}, status=404)
            return Response({"status": "success"}, status=200)
        except Exception as e:
            logger.error(f'Error getting obj detail with error: {e}')
            return Response({'Error': 'Database error, return to previous page'}, status=500)
        # return redirect('elastics:basic-cluster-list')

class DefaultSettingsUpdateView(SingleObjectMixin, APIView):
    model = MetaInfo
    success_url = reverse_lazy('api-elastics:node-list')
    template_name = 'elastics/node_detail.html'
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_object1(self, k):
        result = self.model.objects.filter(id=k, setting=True)
        return result

    def get(self, request, *args, **kwargs):
        try:
            try:
                obj = self.get_object1(self.kwargs['pk'])
                if obj:
                    check_setting_connent(obj)
            except MetaInfo.DoesNotExist:
                return Response({'Error': 'obj Does Not Exist.'}, status=404)
            return Response({"status": "success"}, status=200)
            # return redirect('api-elastics:node-list')
        except Exception as e:
            logger.error(f'Error getting obj detail with error: {e}')
            return Response({'Error': 'Database error, return to previous page'}, status=500)

class ClusterRemoteInfoUpdateView(SingleObjectMixin, APIView):
    model = MetaInfo
    success_url = reverse_lazy('elastics:cluster-remote-list')
    template_name = 'elastics/cluster_remote_list.html'
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_object1(self, k):
        result = self.model.objects.filter(id=k, setting=True)
        return result

    def get(self, request, *args, **kwargs):
        try:
            try:
                obj = self.get_object1(self.kwargs['pk'])
                if obj:
                    cluster_remote_connent(obj)
            except MetaInfo.DoesNotExist:
                return Response({'Error': 'obj Does Not Exist.'}, status=404)
            return Response({"status": "success"}, status=200)
        except Exception as e:
            logger.error(f'Error getting obj detail with error: {e}')
            return Response({'Error': 'Database error, return to previous page'}, status=500)
        # return redirect('elastics:cluster-remote-list')

