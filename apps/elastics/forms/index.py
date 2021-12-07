# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/11 11:42 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django import forms
from ..models import Index, MetaInfo
from orgs.mixins.forms import OrgModelForm
from common.utils import validate_ssh_private_key, ssh_pubkey_gen, get_logger
from django.forms import fields, widgets

logger = get_logger(__file__)
__all__ = ['IndexForm']

class IndexForm(forms.Form):

    _templates = {
        "mappings": {
            "_doc": {
                "dynamic": "strict",
                "properties": {
                    "paid_amount_fen": {
                        "type": "long"
                    }

                }
            }
        }
    }

    name = forms.CharField(label="名称", max_length=64, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    pri = forms.IntegerField(label="主分片", required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    rep = forms.IntegerField(label="副本", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    mapping = forms.CharField(label="mapping", required=False, widget=forms.Textarea(
        attrs={'placeholder': _templates, 'class': 'form-control input-small'}))
    # metainfo = fields.CharField(label="集群", required=True,
    #                          widget=widgets.Select(attrs={'class': 'form-control'}, choices=[], ))
    metainfo = fields.MultipleChoiceField(label="云", widget=forms.CheckboxSelectMultiple(), choices=[], )

    def __init__(self, *args, **kwargs):
        super(IndexForm, self).__init__(*args, **kwargs)
        self.fields['metainfo'].widget.choices = MetaInfo.objects.values_list('id', 'name')
