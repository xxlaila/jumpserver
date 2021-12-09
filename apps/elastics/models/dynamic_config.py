# -*- coding: utf-8 -*-
"""
@File    : dynamic_config.py
@Time    : 2021/12/7 10:04 上午
@Author  : xxlaila
@Software: PyCharm
"""
import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from orgs.mixins.models import OrgModelMixin
from ..models import MetaInfo

__all__ = ['BreakerConfig', 'RoutingConfig', 'BreakerConfigNum', 'RoutingConfigNum']
logger = logging.getLogger(__name__)

class BreakerConfig(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fielddata_over = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Fielddata overhead'))
    request_over = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Request overhead'))
    total_limit = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Total limit'))
    request_limit = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Request limit'))
    fielddata_limit = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Fielddata limit'))
    inflight_req = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Inflight_requests overhead'))
    inflight_req_limit = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Inflight_requests limit'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_('Metainfo'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))

    def __str__(self):
        return self.request_over

    class Meta:
        verbose_name = _("BreakerConfig")

class BreakerConfigNum(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    breakerconfig = models.ForeignKey(BreakerConfig, on_delete=models.CASCADE, verbose_name=_('BreakerConfig'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_('Metainfo'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    class Meta:
        verbose_name = _("BreakerConfigNum")


class RoutingConfig(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rebalance_enable = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Rebalance enable'))

    node_concurrent_recoveries = models.IntegerField(null=True, blank=True, verbose_name=_('Node concurrent recoveries'))
    cluster_concurrent_rebalance = models.IntegerField(null=True, blank=True,
                                                       verbose_name=_('Cluster concurrent rebalance'))
    node_initial_primaries_recoveries = models.IntegerField(null=True, blank=True,
                                                            verbose_name=_('Node initial primaries recoveries'))
    node_concurrent_outgoing_recoveries = models.IntegerField(null=True, blank=True,
                                                            verbose_name=_('Node concurrent outgoing recoveries'))
    disk_watermark_flood_stage = models.CharField(null=True, blank=True,  max_length=16, verbose_name=_('Disk watermark flood stage'))
    disk_watermark_low = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Disk watermark low'))
    disk_watermark_high = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Disk watermark high'))
    allow_rebalance = models.CharField(null=True, blank=True, max_length=32, verbose_name=_('Allow rebalance'))
    allocation_enable = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Allocation enable'))
    awareness_attributes = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Awareness attributes'))
    balance_index = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Balance index'))
    balance_threshold = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Balance threshold'))
    balance_shard = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Balance shard'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_('Metainfo'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))

    def __str__(self):
        return self.rebalance_enable

    class Meta:
        verbose_name = _("RoutingConfig")

class RoutingConfigNum(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    routingConfig = models.ForeignKey(RoutingConfig, on_delete=models.CASCADE, verbose_name=_('RoutingConfig'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_('Metainfo'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    class Meta:
        verbose_name = _("RoutingConfigNum")