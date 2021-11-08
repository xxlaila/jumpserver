# -*- coding: utf-8 -*-
"""
@File    : balanced.py
@Time    : 2021/11/6 1:27 下午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..models.asset_expansion import CTYPE_CHOICES, CATEGORY_CHOICES, PAYBY_CHOICES
from ..models import AssetExpansion

__all__ = ['Balanced']
logger = logging.getLogger(__name__)

NETWORK_TYPE_CHOICES = (
        ("internet", "公网"),
        ("intranet", "内网"),
    )

class Balanced(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    loadid = models.CharField(null=True, blank=True, max_length=128, verbose_name=_('Instance id'))
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP'), db_index=True)
    loadname = models.CharField(null=True, blank=True, max_length=512, verbose_name=_('Instance name'))
    vswitchId = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Virtual switch'))
    resgroup = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Enterprise Resource Group'))
    paytype = models.CharField(choices=PAYBY_CHOICES, max_length=64, verbose_name=_('Billing method'))
    masterzoneid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Main zone'))
    slavezoneid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Backup zone'))
    addresstype = models.CharField(choices=NETWORK_TYPE_CHOICES, max_length=64, verbose_name=_('Network Type'))
    loadbalancerspec = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Instance type'))
    vpcid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Vpc network'))
    regionid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Area'))
    status = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Status'))
    describeinfo = models.TextField(null=True, blank=True, verbose_name=_('Detail'))
    create_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation time'))
    update_data = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=_("Date updated"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    def __int__(self):
        return '{0.loadid}({0.ip})'.format(self)

    class Meta:
        ordering = ['ip']
        verbose_name = ("Balanced")