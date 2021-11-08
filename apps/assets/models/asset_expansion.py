# -*- coding: utf-8 -*-
"""
@File    : asset_expansion.py
@Time    : 2021/11/6 10:33 上午
@Author  : xxlaila
@Software: PyCharm
"""
import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = ['AssetExpansion']
logger = logging.getLogger(__name__)

CTYPE_CHOICES = (
        ("PrePaid", "包年包月"),
        ("PostPaid", "按量付费")
    )
PAYBY_CHOICES = (
        ("PayByBandwidth", "固定带宽"),
        ("PayByTraffic", "按流量"),
        ("PayOnDemand", "按量付费"),
        ("PrePay", "包年包月"),
    )
CATEGORY_CHOICES = (
        ("cloud", "普通云盘"),
        ("cloud_efficiency", "高效云盘"),
        ("cloud_ssd", "SSD盘"),
        ("cloud_essd", "ESSD云盘"),
        ("local_ssd_pro", "I/O密集型本地盘"),
        ("local_hdd_pro", "吞吐密集型本地盘"),
    )

class AssetExpansion(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostname = models.CharField(null=True, blank=True, max_length=64, verbose_name=_('Hostname'), db_index=True)
    instance = models.CharField(null=True, blank=True, max_length=64, verbose_name=_('Instance name'), db_index=True)
    memory = models.IntegerField(null=True, blank=True, verbose_name=_('Memory'))
    core_thread = models.IntegerField(null=True, blank=True, verbose_name=_('Cpu threads'))
    cpu_vcpus = models.IntegerField(null=True, blank=True, verbose_name=_('Virtual cpu'))
    cpu_cores = models.IntegerField(null=True, blank=True, verbose_name=_('Cpu core'))
    localstoranum = models.IntegerField(null=True, blank=True, verbose_name=_("Number of data disks"))
    localstorasize = models.IntegerField(null=True, blank=True, verbose_name=_("Single disk size"))
    os_version = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('OS version'), db_index=True)
    os_arch = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Release'), db_index=True)
    images = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Mirror image'))
    vpc = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Vpc network'))
    security = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('Security group'))
    vswaitch = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Virtual switch'))
    instancetype = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Instance type'))
    eip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('Flexible ip'), db_index=True)
    ebandwidth = models.IntegerField(null=True, blank=True, verbose_name=_('Elastic ip bandwidth'))
    paybywidth = models.CharField(choices=PAYBY_CHOICES, max_length=64, verbose_name=_('Bandwidth billing method'))
    publicip = models.CharField(max_length=128, blank=True, null=True, verbose_name=('Public IP'), db_index=True)
    primaryip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP'), db_index=True)
    primarynetwork = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Private network card'))
    primarymac = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Private network card mac'))
    regionid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Area'), db_index=True)
    zoneid = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Availability zone'), db_index=True)
    chargetype = models.CharField(choices=CTYPE_CHOICES, max_length=64, verbose_name=_('Billing method'), db_index=True)
    operuser = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("Operation and maintenance principal"), db_index=True)
    devuser = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("Development Director"), db_index=True)
    dept = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("Department"), db_index=True)
    status = models.CharField(max_length=128, null=True, blank=True, db_index=True, verbose_name=_('Status'))
    create_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation time'))
    expired_time = models.DateTimeField(blank=True, null=True, verbose_name=_("Expired"))
    start_time = models.DateTimeField(blank=True, null=True, verbose_name=_("Start Time"))
    update_data = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=_("Date updated"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    def __str__(self):
        return '{0.hostname}({0.primaryip})({0.instance})'.format(self)

    class Meta:
        ordering = ['create_time']
        unique_together = [('hostname', 'primaryip', 'instance')]
        verbose_name = _("AssetExpansion")