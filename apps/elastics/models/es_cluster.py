# -*- coding: utf-8 -*-
"""
@File    : es_cluster.py
@Time    : 2021/10/21 9:01 下午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.fields.model import JsonDictTextField
from orgs.mixins.models import OrgModelMixin
from ..models import MetaInfo

__all__ = ['BasicCluster', 'ClusterSetting', 'ClusterRemote']
logger = logging.getLogger(__name__)

class BasicCluster(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=64, db_index=True, verbose_name=_('Name'))
    status = models.CharField(null=True, blank=True, max_length=64, verbose_name=_('Status'))
    st = models.IntegerField(null=True, blank=True, verbose_name=_('Total shard'))
    sp = models.IntegerField(null=True, blank=True, verbose_name=_('Primary shard'))
    incount = models.IntegerField(null=True, blank=True, verbose_name=_('Total index'))
    indocs = models.BigIntegerField(null=True, blank=True, verbose_name=_('Total docs'))
    instore = models.BigIntegerField(null=True, blank=True, verbose_name=_('Total use space'))
    nt = models.IntegerField(null=True, blank=True, verbose_name=_('Total node'))
    nc = models.IntegerField(null=True, blank=True, verbose_name=_('Read-only node'))
    nd = models.IntegerField(null=True, blank=True, verbose_name=_('Data node'))
    ni = models.IntegerField(null=True, blank=True, verbose_name=_('Ingest node'))
    nm = models.IntegerField(null=True, blank=True, verbose_name=_('Master node'))
    nr = models.IntegerField(null=True, blank=True, verbose_name=_('Client node'))
    mt = models.BigIntegerField(null=True, blank=True, verbose_name=_('Total memory'))
    mf = models.BigIntegerField(null=True, blank=True, verbose_name=_('Free memory'))
    mu = models.BigIntegerField(null=True, blank=True, verbose_name=_('Use memory'))
    pt = JsonDictTextField(blank=True, null=True, verbose_name=_('Install'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_("Metainfo"))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("BasicCluster")

class ClusterSetting(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    persis = models.TextField(null=True, blank=True, verbose_name=_('Permanent parameters'))
    tran = models.TextField(null=True, blank=True, verbose_name=_('Temporary parameters'))
    def_clus = models.TextField(null=True, blank=True, verbose_name=_('Default cluster parameters'))
    def_xpack= models.TextField(null=True, blank=True, verbose_name=_('Security'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_("Metainfo"))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    def __int__(self):
        return '{0.id}({0.label})'.format(self)

    class Meta:
        ordering = ['date_updated']
        verbose_name = ("ClusterSetting")

class ClusterRemote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=128, verbose_name=_('Name'))
    mode = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Connection mode'))
    conn = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Status'))
    conn_timeout = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Connection timed out'))
    skip_una = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Skip cluster'))
    seeds = models.TextField(null=True, blank=True, verbose_name=_('Connection address'))
    num_nodes = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Number of nodes'))
    max_conn = models.CharField(null=True, blank=True, max_length=16, verbose_name=_('Maximum connection'))
    proxy_add = models.CharField(null=True, blank=True, max_length=128, verbose_name=_('Proxy model'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_("Metainfo"))
    date_updated = models.DateTimeField(auto_now=True, blank=True, verbose_name=_('Date updated'))

    def __int__(self):
        return '{0.id}({0.name})'.format(self)

    class Meta:
        ordering = ['date_updated']
        verbose_name = ("ClusterRemote")