# -*- coding: utf-8 -*-
"""
@File    : cloudinfor.py
@Time    : 2021/10/19 3:24 下午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from orgs.mixins.models import OrgModelMixin

__all__ = ['CloudInfor']

class CloudInfor(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    value = models.CharField(null=True, blank=True, max_length=128, verbose_name=_("Value"))
    key = models.CharField(null=True, blank=True, max_length=128, verbose_name=_("Key"))
    secret = models.CharField(null=True, blank=True, max_length=128, verbose_name=_('Secret'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))

    # @classmethod
    # def default(cls):
    #     cloud, created = cls.objects.get_or_create(
    #         defaults={'name': ''}, name=''
    #     )
    #     return cloud.id
    #
    # def is_windows(self):
    #     return self.name.lower() in ('')
    #
    # def is_unixlike(self):
    #     return self.name.lower() in ("")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = [('org_id', 'name')]
        verbose_name = _("CloudInfor")