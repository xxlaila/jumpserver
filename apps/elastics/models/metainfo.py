# -*- coding: utf-8 -*-
"""
@File    : metainfo.py
@Time    : 2021/10/19 3:27 下午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .cloudinfor import CloudInfor
from orgs.mixins.models import OrgModelMixin
from common.utils import lazyproperty

__all__ = ['MetaInfo']
logger = logging.getLogger(__name__)

ENV_CHOICES = (
        ("dev", "dev"),
        ("test", "test"),
        ("uat", "uat"),
        ("pre", "pre"),
        ("gra", "gra"),
        ("prd", "prd"),
    )



class MetaInfo(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=64, verbose_name=_('Name'), db_index=True)
    env = models.CharField(choices=ENV_CHOICES, default='', max_length=32, verbose_name=_("Env"))
    address = models.CharField(null=True, blank=True, max_length=512, verbose_name=_("Address"), db_index=True)
    username = models.CharField(null=True, blank=True, max_length=128, verbose_name=_("Username"))
    password = models.CharField(null=True, blank=True, max_length=128, verbose_name=_("Password"))
    kibana = models.URLField(null=True, blank=True, max_length=512, verbose_name=_("Kibana addr"))
    kafka = models.URLField(null=True, blank=True, max_length=512, verbose_name=_("Kafka addr"))
    cloud = models.ForeignKey(CloudInfor, related_name='cloudinfor', on_delete=models.CASCADE,
                              verbose_name=_("Cloud"))
    health = models.BooleanField(default=True, verbose_name=_('Health'))
    setting = models.BooleanField(default=False, verbose_name=_('Setting '))
    alter = models.BooleanField(default=False, verbose_name=_('Alter'))
    indexes = models.BooleanField(default=False, verbose_name=_('Index'))
    node = models.BooleanField(default=True, verbose_name=_('Node'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    labels = models.CharField(null=True, blank=True, max_length=32, verbose_name=_("Labels"))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=_('Created by'))

    def __str__(self):
        return self.name

    @lazyproperty
    def cloud_base(self):
        return self.cloud.name

    @property
    def cloud_display(self):
        return ' '.join([cloud.name for cloud in self.cloud.all()])

    def is_member_of(self, cloud):
        if cloud in self.cloud.all():
            return True
        return False

    class Meta:
        ordering = ['name']
        verbose_name = _("MetaInfo")

