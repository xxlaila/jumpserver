# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/10 9:53 上午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from orgs.mixins.models import OrgModelMixin
from ..models import MetaInfo, EsNode

__all__ = ['Index', 'IndiceNode', 'IndiceShard']
logger = logging.getLogger(__name__)

PRIREP_CHOICES = (
        ("p", "Primary"),
        ("r", "Replica"),
    )

STATE_CHOICES = (
        ("INITIALIZING", "The shard is recovering from a peer shard or gateway."),
        ("RELOCATING", "The shard is relocating."),
        ("STARTED", "The shard has started."),
        ("UNASSIGNED", "The shard is not assigned to any node."),
    )

class Index(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Name'))
    uuid = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Uuid'))
    pri = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Primary shard'))
    rep = models.IntegerField(null=True, blank=True, verbose_name=_('Replica Set'))
    dc = models.BigIntegerField(null=True, blank=True, verbose_name=_('Total docs'))
    ssize = models.BigIntegerField(null=True, blank=True, verbose_name=_('Store size'))
    pss = models.BigIntegerField(null=True, blank=True, verbose_name=_('Pri store size'))
    health = models.CharField(max_length=32, verbose_name=_('Health'))
    status = models.CharField(max_length=32, verbose_name=_('Status'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_("Metainfo"))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    def __str__(self):
        return self.name

    @property
    def metainfo_display(self):
        return ' '.join([metainfo.name for metainfo in self.metainfo.all()])

    class Meta:
        ordering = ['name', 'date_updated']
        verbose_name = _("Index")

class IndiceShard(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    index = models.ManyToManyField(Index, verbose_name=_('Index'))
    shard = models.IntegerField(null=True, verbose_name=_('Shard'))
    pr = models.CharField(choices=PRIREP_CHOICES, max_length=32, null=True, verbose_name=_('Primary or Replica'))
    st = models.CharField(choices=STATE_CHOICES, max_length=128, null=True, verbose_name=_('State'))
    dc = models.BigIntegerField(null=True, blank=True, verbose_name=_('Shard docs'))
    sto = models.BigIntegerField(null=True, blank=True, verbose_name=_('Shard store size'))
    esnode = models.ForeignKey(EsNode, on_delete=models.CASCADE, verbose_name=_('Esnode'))
    uid = models.CharField(null=True, blank=True, max_length=128, verbose_name=_('Uid'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['date_updated']
        verbose_name = _("IndiceShard")


class IndiceNode(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    esnode = models.ForeignKey(EsNode, on_delete=models.CASCADE, verbose_name=_('Esnode'))
    index = models.ForeignKey(Index, on_delete=models.CASCADE, verbose_name=_('Index'))
    refresh = models.IntegerField(verbose_name=_('Refresh'))
    flush = models.IntegerField(verbose_name=_('Flush'))
    recovery = models.IntegerField(verbose_name=_('Recovery'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['esnode']
        verbose_name = _("IndiceNode")
