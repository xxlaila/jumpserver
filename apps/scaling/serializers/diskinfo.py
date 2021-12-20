# -*- coding: utf-8 -*-
"""
@File    : diskinfo.py
@Time    : 2021/12/18 1:42 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import DiskInfo
from orgs.mixins.serializers import BulkOrgResourceModelSerializer

class DiskInfoSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = DiskInfo
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            "id", "diskid", "device", 'org_name', "category", "disk_size", "chargetype", "zoneid", "assetexpansion", "delwith",
            "snapshot", "autoanspshot", "regionid", "disk_type", "encrypted", "status", "expired_time", "create_time",
            "update_data", "comment"
        ]