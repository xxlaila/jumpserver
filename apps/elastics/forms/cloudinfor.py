# -*- coding: utf-8 -*-
"""
@File    : cloudinfor.py
@Time    : 2021/10/19 4:28 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ..models import CloudInfor

class CloudInforForm(forms.ModelForm):

    class Meta:
        model = CloudInfor
        fields = ['name', 'value', 'key', 'secret', 'comment']
