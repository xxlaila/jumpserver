# -*- coding: utf-8 -*-
"""
@File    : assetexpansion.py
@Time    : 2021/12/17 2:15 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import AssetExpansion
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from rest_framework import serializers

class AssetExpansionSerializer(BulkOrgResourceModelSerializer):
    cloudinfor_display = serializers.ReadOnlyField()
    # disk_count = serializers.SerializerMethodField()

    class Meta:
        model = AssetExpansion
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            "id", "hostname", "instance", 'org_name', "memory", "core_thread", "cpu_vcpus", "cpu_cores", "localstoranum",
            "localstorasize", "os_version", "os_arch", "images", "vpc", "security", "vswaitch", "instancetype", "eip",
            "ebandwidth", "paybywidth", "publicip", "primaryip", "primarynetwork", "primarymac", "regionid", "zoneid",
            "chargetype", "operuser", "devuser", "dept", "status", "cloudinfor_display", "create_time", "expired_time",
            "start_time", "update_data", "comment",
        ]

        extra_kwargs = {
            'instance': {'required': True},
            'primaryip': {'required': True},
        }