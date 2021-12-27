# -*- coding: utf-8 -*-
"""
@File    : alter.py
@Time    : 2021/10/24 5:11 下午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from orgs.mixins.models import OrgModelMixin
from ..models import MetaInfo
from common.utils import lazyproperty

__all__ = ['AlterWeaken', 'Malfunction']
logger = logging.getLogger(__name__)

class Malfunction(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=128, verbose_name=_('Name'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comment'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    date_created = models.DateTimeField(auto_now_add=True)
    metainfo = models.ForeignKey(MetaInfo, null=True, on_delete=models.SET_NULL, verbose_name=_('Metainfo'))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))


    class Meta:
        ordering = ['-date_created']
        verbose_name = _("Malfunction")


class AlterWeaken(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_active = models.BooleanField(default=False, verbose_name=_('Is active '))
    frequency = models.IntegerField(blank=True, null=True, verbose_name=_('Frequency'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("AlterWeaken")