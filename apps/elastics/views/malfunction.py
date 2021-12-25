# -*- coding: utf-8 -*-
"""
@File    : malfunction.py
@Time    : 2021/12/25 9:46 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from common.permissions import PermissionsMixin, IsOrgAdmin, IsSuperUser, IsValidUser
from common.utils import get_object_or_none, get_logger
from ..models import Malfunction

__all__ = (
    "MalfunctionListView",
)
logger = get_logger(__file__)

class MalfunctionListView(PermissionsMixin,TemplateView):
    model = Malfunction
    template_name = 'elastics/malfunction_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Malfunction list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)