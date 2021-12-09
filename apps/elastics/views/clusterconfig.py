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
from rest_framework.views import APIView
from ..models import MetaInfo, BreakerConfig, RoutingConfig
from common.utils import get_logger
from ..utils import default_conn,put_settings_cluster
from django.http import JsonResponse

__all__ = (
    "ClusterDynamicConfigView", "ClusterRouteringView",
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
    
    def get_routing_data(self):
        data = self.get_object().routingconfig_set.all().first()
        return data

    def get_breaker_data(self):
        data = self.get_object().breakerconfig_set.all().first()
        return data

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Dynamic configuration'),
            'object': self.get_object(),
            'routing': self.get_routing_data(),
            'breaker': self.get_breaker_data(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class ClusterRouteringView(PermissionsMixin, SingleObjectMixin, APIView):

    permission_classes = (IsOrgAdmin,)
    object = None

    def post(self, request, *args, **kwargs):
        data = request.POST
        escoo = self.get_object(MetaInfo.objects.get(id=self.kwargs['pk']))
        body = {
          "persistent": {
            "cluster": {
              "routing": {
                "allocation.node_concurrent_recoveries": data.get('node_concurrent_recoveries'),
                "allocation.cluster_concurrent_rebalance": data.get('cluster_concurrent_rebalance'),
                "allocation.node_initial_primaries_recoveries": data.get('node_initial_primaries_recoveries'),
                "allocation.disk.watermark.high": "%s" % data.get('disk_watermark_high'),
                "allocation.disk.watermark.low": "%s" % data.get('disk_watermark_low'),
                "allocation.disk.watermark.flood_stage": "%s" % data.get('disk_watermark_flood_stage'),
                "allocation.allow_rebalance": "%s" % data.get('allow_rebalance'),
                "rebalance": {
                  "enable": "%s" % data.get('rebalance_enable')
                },
                "allocation.enable": "%s" % data.get('allocation_enable'),
                "allocation.awareness.attributes": [data.get('awareness_attributes')],
                "allocation.balance.index": data.get('balance_index'),
                "allocation.balance.threshold": data.get('balance_threshold'),
                "allocation.balance.shard": data.get('balance_shard'),
                "allocation.node_concurrent_outgoing_recoveries": data.get('node_concurrent_outgoing_recoveries')
              }
            }
          }
        }
        result = put_settings_cluster(escoo, body)
        if result:
            return JsonResponse({"status": "success"})