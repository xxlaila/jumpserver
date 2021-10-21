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

__all__ = ['MetaInfoForm']

class MetaInfoForm(forms.ModelForm):
    # cloud = forms.ModelMultipleChoiceField(
    #     queryset=CloudInfor.objects, label=_('Cloud'), required=False,
    #     widget=forms.SelectMultiple(
    #         attrs={'class': 'select2', 'data-placeholder': _('Select Cloud')}
    #     )
    # )

    class Meta:
        model = MetaInfo
        fields = ['name', 'env', 'address', 'username', 'password',
                  'kibana', 'kafka', 'cloud', 'comment', 'labels']

    widgets = {
        'mfa_level': forms.RadioSelect(),
        'cloud': forms.SelectMultiple(
            attrs={
                'class': 'select2',
                # 'data-placeholder': _('Join user groups')
            }
        )
    }
