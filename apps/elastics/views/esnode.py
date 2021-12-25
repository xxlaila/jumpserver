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
from common.utils import get_logger
from ..models import EsNode, MetaInfo, IndiceNode
from common.const import create_success_msg, update_success_msg
from django.urls import reverse_lazy
from rest_framework.views import APIView, Response
from ..utils import get_nodes_connenct, exclude_node, get_node_stats

__all__ = (
    "NodeListView", "NodeDetailView", "NodeUpdateView", "NodeOnlineView",
    "NodeIndiceListView", 'MetainfoNodeListView'
)
logger = get_logger(__name__)

class NodeListView(PermissionsMixin,TemplateView):
    model = EsNode
    template_name = 'elastics/node_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Node list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class MetainfoNodeListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/meta_node_list.html'
    model = MetaInfo
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Node list'),
            'object': self.get_object(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeDetailView(PermissionsMixin, DetailView):
    model = EsNode
    template_name = 'elastics/node_detail.html'
    permission_classes = [IsOrgAdmin]
    object = None

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Node detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeIndiceListView(PermissionsMixin, SingleObjectMixin, TemplateView):
    template_name = 'elastics/node_stats_indices_detail.html'
    model = EsNode
    object = None
    permission_classes = [IsOrgAdmin]
    
    def nodes_stats(self, id):
        datas = self.model.objects.filter(id=id)
        nodes = get_node_stats(datas)
        return nodes

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Node indices'),
            'object': self.get_object(),
            'nodes_stats': self.nodes_stats(self.kwargs['pk'])
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeUpdateView(SingleObjectMixin, APIView):
    model = MetaInfo
    success_url = reverse_lazy('api-elastics:node-list')
    template_name = 'elastics/meta_node_list.html'
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]
    
    # def get_success_url(self):
    #     return reverse('assets:elastics:node-list', kwargs={
    #         'pk': self.cmd_filter.id
    #     })

    def get_object1(self, k):
        result = self.model.objects.filter(id=k, node=True)
        return result

    def get(self, request, *args, **kwargs):
        try:
            try:
                obj = self.get_object1(self.kwargs['pk'])
                if obj:
                    get_nodes_connenct(obj)
            except MetaInfo.DoesNotExist:
                return Response({'Error': 'obj Does Not Exist.'})
            return Response({"status": "success"}, status=200)
            # return redirect('api-elastics:node-list')
        except Exception as e:
            logger.error(f'Error getting obj detail with error: {e}')
            return Response({'Error': 'Database error, return to previous page'}, status=500)

class NodeOnlineView(SingleObjectMixin, APIView):

    permission_classes = (IsOrgAdmin,)
    object = None

    def post(self, request, *args, **kwargs):
        datas = self.get_object(EsNode.objects.filter(id=self.kwargs['pk']))
        ok, e = exclude_node(datas)
        if datas.status == False:
            datas.status = True
        else:
            datas.status = False
        datas.save()
        if ok:
            return Response("ok")
        else:
            return Response({"error": e}, status=400)
