# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/11 11:42 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django import forms
from ..models import Index
from orgs.mixins.forms import OrgModelForm
from common.utils import validate_ssh_private_key, ssh_pubkey_gen, get_logger

logger = get_logger(__file__)
__all__ = ['IndexForm']

class IndexForm(OrgModelForm):

    def save(self, commit=True):
        raise forms.ValidationError("Use api to save")

    class Meta:
        model = Index
        fields = []