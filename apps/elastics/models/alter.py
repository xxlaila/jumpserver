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

__all__ = ['AlterWeaken']
logger = logging.getLogger(__name__)

class AlterWeaken(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_active = models.BooleanField(default=False, verbose_name=_('Is active '))
    frequency = models.IntegerField(blank=True, null=True, verbose_name=_('Frequency'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("AlterWeaken")