# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/10 10:36 上午
@Author  : xxlaila
@Software: PyCharm
"""
from django.utils.translation import ugettext_lazy as _
from common.serializers import AdaptedBulkListSerializer
from ..models import Index, IndiceShard
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from rest_framework import serializers

__all__ = [
    'IndexSerializer', 'IndexDisplaySerializer', 'IndiceShardSerializer',
]

class IndexSerializer(BulkOrgResourceModelSerializer):

    class Meta:
        model = Index
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'uuid', 'pri', 'rep', 'dc', 'ssize',
            'pss', 'health', 'status', 'metainfo', 'date_updated'
        ]

    def validate_metainfo(self, metainfo):
        return metainfo

class IndexDisplaySerializer(IndexSerializer):
    # can_update = serializers.SerializerMethodField()
    # can_delete = serializers.SerializerMethodField()

    class Meta(IndexSerializer.Meta):
        fields = IndexSerializer.Meta.fields + [
            'metainfo_display',
        ]

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        kwargs.update({
            'metainfo_display': {'label': _('Cluster')},
        })
        return kwargs


class IndiceShardSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndiceShard
        fields = ("id", "index", "shard", "pr", "st", "dc", "sto", "esnode", "uid")

    def create(self, validated_data):
        authors = validated_data.pop('index')
        print(validated_data)
        book = IndiceShard.objects.create(**validated_data)
        for author in authors:
            author = Index.objects.filter(name=author.name).first()
            book.index.add(author)
            book.save()

        return book