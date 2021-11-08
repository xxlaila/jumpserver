# -*- coding: utf-8 -*-
"""
@File    : diskinfo.py
@Time    : 2021/11/6 1:20 下午
@Author  : xxlaila
@Software: PyCharm
"""

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..models.asset_expansion import CTYPE_CHOICES, CATEGORY_CHOICES, PAYBY_CHOICES
from ..models import AssetExpansion

__all__ = ['DiskInfo']
logger = logging.getLogger(__name__)

DEL_TYPE_CHOICES = (
    ("false", "保留不释放"),
    ("true", "随实例释放")
)
END_SANPSHOT_CHOICES = (
    ("true", "启用"),
    ("false", "未启用")
)
SNAPSHOT_POLICY_CHOICES = (
    ("true", "已设置"),
    ("false", "未设置")
)
DISK_STATUS_CHOICES = (
    ("In_use", "使用中"),
    ("Available", "待挂载")
)
DISK_TYPE_CHOICES = (
    ("system", "系统盘"),
    ("data", "数据盘")
)

class DiskInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    diskid = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Disk id"))
    device = models.CharField(max_length=32, blank=True, null=True, verbose_name=_("Disk device"))
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=64, verbose_name=_("Disk type"))
    disk_size = models.BigIntegerField(null=True, blank=True, verbose_name=_("Disk size"))
    chargetype = models.CharField(choices=CTYPE_CHOICES, max_length=64,
                                  verbose_name=_('Billing method'), db_index=True)
    zoneid = models.CharField(max_length=128, null=True, blank=True,
                              verbose_name=_('Availability zone'), db_index=True)
    assetexpansion = models.OneToOneField(AssetExpansion, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name=_('assetexpansion'))
    delwith = models.CharField(choices=DEL_TYPE_CHOICES, default="false", max_length=64,
                               verbose_name=_("Release method"))
    snapshot = models.CharField(choices=SNAPSHOT_POLICY_CHOICES, max_length=64, null=True, blank=True,
                                verbose_name=_("Automatic snapshot strategy"))
    autoanspshot = models.CharField(choices=END_SANPSHOT_CHOICES, max_length=64, null=True, blank=True,
                                    verbose_name=_("Snapshot policy function"))
    regionid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Area'), db_index=True)
    disk_type = models.CharField(choices=DISK_TYPE_CHOICES, max_length=64, verbose_name=_("Disk attributes"))
    encrypted = models.CharField(default="false", max_length=64, verbose_name=_("Whether to encrypt"))
    status = models.CharField(choices=DISK_STATUS_CHOICES, max_length=64, null=True, blank=True,
                              verbose_name=_("Status"))
    expired_time = models.DateTimeField(blank=True, null=True, verbose_name=_("Expired"))
    create_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation time'))
    update_data = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=_("Date updated"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    def __int__(self):
        return '{0.diskid}({0.device})'.format(self)

    class Meta:
        ordering = ['create_time']
        unique_together = [('diskid')]
        verbose_name = ("DiskInfo")
