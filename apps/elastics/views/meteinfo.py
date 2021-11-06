# -*- coding: utf-8 -*-
"""
@File    : meteinfo.py
@Time    : 2021/10/21 11:32 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from common.permissions import PermissionsMixin, IsOrgAdmin, IsSuperUser, IsValidUser
from django.shortcuts import get_object_or_404, reverse
from common.const import create_success_msg, update_success_msg
from common.utils import get_object_or_none, get_logger
from ..forms import MetaInfoForm
from ..models import MetaInfo, CloudInfor

__all__ = (
    "MetaInfoListView", "MetaInfoCreateView", "MetaInfoUpdateView",
    "MetaInfoDetailView", "MetaInfoDeleteView"
)
logger = get_logger(__file__)

class MetaInfoListView(PermissionsMixin,TemplateView):
    model = MetaInfo
    template_name = 'elastics/meta_info_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            # 'labels': Label.objects.all().order_by('name'),
            # 'cloud': CloudInfor.objects.all().order_by('name'),
            'action': _('Meta info list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class MetaInfoCreateView(PermissionsMixin, CreateView):
    model = MetaInfo
    form_class = MetaInfoForm
    template_name = 'elastics/meta_info_create_update.html'
    success_url = reverse_lazy('elastics:meta-info-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Create meta info'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class MetaInfoUpdateView(PermissionsMixin, UpdateView):
    model = MetaInfo
    template_name = 'elastics/meta_info_create_update.html'
    form_class = MetaInfoForm
    success_url = reverse_lazy('elastics:meta-info-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Update meta info'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class MetaInfoDetailView(PermissionsMixin, DetailView):
    model = MetaInfo
    context_object_name = 'meteinfo'
    template_name = 'elastics/meta_info_detail.html'
    permission_classes = [IsOrgAdmin, IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Meta info detail')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class MetaInfoDeleteView(PermissionsMixin, DeleteView):
    model = MetaInfo
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('elastics:meta-info-list')
    permission_classes = [IsOrgAdmin]