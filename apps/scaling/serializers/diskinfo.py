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
from rest_framework import serializers

class DiskInfoSerializer(BulkOrgResourceModelSerializer):
    assetexpansion_display = serializers.ReadOnlyField()

    class Meta:
        model = DiskInfo
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            "id", "diskid", "device", 'org_name', "category", "disk_size", "chargetype", "zoneid", "assetexpansion", "delwith",
            "snapshot", "autoanspshot", "regionid", "disk_type", "encrypted", "status", "expired_time", "create_time",
            "assetexpansion_display", "update_data", "comment", "get_category_display", "get_chargetype_display",
            "get_delwith_display", "get_snapshot_display", "get_autoanspshot_display", "get_disk_type_display",
            "get_status_display"
        ]

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend(['get_category_display', 'get_delwith_display'])
        return fields