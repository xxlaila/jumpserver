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
from ..models import MetaInfo

__all__ = ['Index']
logger = logging.getLogger(__name__)

class Index(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Name'))
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


