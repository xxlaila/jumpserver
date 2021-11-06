# -*- coding: utf-8 -*-
"""
@File    : meteinfo.py
@Time    : 2021/10/21 11:33 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ..models import MetaInfo,CloudInfor
from orgs.mixins.forms import OrgModelForm
from common.utils import validate_ssh_private_key, ssh_pubkey_gen, get_logger

logger = get_logger(__file__)
__all__ = ['MetaInfoForm']

class MetaInfoForm(OrgModelForm):

    def save(self, commit=True):
        raise forms.ValidationError("Use api to save")

    class Meta:
        model = MetaInfo
        fields = ['name', 'env', 'address', 'username', 'password',
                  'kibana', 'kafka', 'cloud', 'comment', 'labels',
                  'health', 'setting', 'alter', 'index', 'node']

    # widgets = {
    #     # 'name': forms.TextInput(attrs={'placeholder': _('Name')}),
    #     'cloud': forms.SelectMultiple(
    #         attrs={
    #             'class': 'select2',
    #             'data-placeholder': _('Cloud')
    #         }
    #     )
    # }

