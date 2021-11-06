# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/10/25 11:02 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, DetailView
)
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from common.permissions import PermissionsMixin, IsOrgAdmin
from ..models import EsNode, MetaInfo

__all__ = (
    "NodeListView", "NodeDetailView"
)

class NodeListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/node_list.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    # def node_data(self):
    #     data = self.get_object().esnode_set.all()
    #     return data

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Node list'),
            'object': self.get_object(),
            # 'nodes': self.node_data(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeDetailView(PermissionsMixin, DetailView):
    model = EsNode
    template_name = 'elastics/node_detail.html'
    permission_classes = [IsOrgAdmin]
    object = None


    # def get(self, *args, **kwargs):
    #     self.object = self.get_object(queryset=self.model.objects.filter(id=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Node detail'),
            # 'nodes': self.object()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)