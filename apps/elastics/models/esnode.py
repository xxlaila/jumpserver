# -*- coding: utf-8 -*-
"""
@File    : esnode.py
@Time    : 2021/10/22 11:27 上午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from orgs.mixins.models import OrgModelMixin
from ..models import MetaInfo

__all__ = ['EsNode', 'NodeFs']
logger = logging.getLogger(__name__)

class EsNode(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    uuid = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Uuid'))
    ip = models.GenericIPAddressField(max_length=128, verbose_name=_('IP'), db_index=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    disktotal = models.BigIntegerField(verbose_name=_('Total disk'))
    diskused = models.BigIntegerField(verbose_name=_('Used disk'))
    diskavail = models.BigIntegerField(verbose_name=_('Avail disk'))
    ramcurrent = models.BigIntegerField(verbose_name=_('Used total memory'))
    rammax = models.BigIntegerField(verbose_name=_('Total memory'))
    noderole = models.CharField(max_length=64, db_index=True, verbose_name=_('Node roles'))
    pid = models.IntegerField(verbose_name=_('Process id'))
    port = models.IntegerField(verbose_name=_('Transmission port'))
    http_address = models.CharField(blank=True, max_length=64, db_index=True, verbose_name=_('Http monitoring'))
    version = models.CharField(max_length=64, verbose_name=_('Version'))
    jdk = models.CharField(max_length=64, db_index=True, verbose_name=_('Jdk version'))
    uptime = models.CharField(max_length=64, db_index=True, verbose_name=_('Running uptime'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    metainfo = models.ForeignKey(MetaInfo, on_delete=models.CASCADE, verbose_name=_('Metainfo'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))

    def __str__(self):
        return '{0.name}({0.ip})'.format(self)

    @property
    def nodes_amount(self):
        return self.ip.all().count()

    class Meta:
        ordering = ['ip']
        verbose_name = _("EsNode")

class NodeFs(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    esnode = models.ForeignKey(EsNode, db_index=True, on_delete=models.CASCADE, verbose_name=_('Esnode'))
    path = models.CharField(null=True, blank=True, max_length=512, verbose_name=_('Data path'))
    mount = models.CharField(null=True, blank=True, max_length=512, verbose_name=_('Mount path'))
    filesystem = models.CharField(null=True, max_length=64, verbose_name=_('File system'))
    total = models.BigIntegerField(verbose_name=_('Total size'))
    free = models.BigIntegerField(verbose_name=_('Free size'))
    available = models.BigIntegerField(verbose_name=_('Available'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Date updated'))

    def __str__(self):
        return '{0.id}'.format(self)

    class Meta:
        verbose_name = _("NodeFs")