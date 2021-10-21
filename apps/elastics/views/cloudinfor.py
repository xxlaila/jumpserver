# -*- coding: utf-8 -*-
"""
@File    : cloudinfor.py
@Time    : 2021/10/19 4:27 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from common.permissions import PermissionsMixin, IsOrgAdmin, IsSuperUser
from django.shortcuts import get_object_or_404, reverse
from common.const import create_success_msg, update_success_msg
from ..forms.cloudinfor import CloudInforForm
from ..models.cloudinfor import CloudInfor


__all__ = (
    "CloudInforListView", "CloudInforCreateView", "CloudInforUpdateView",
    "CloudInforDetailView", "CloudInforDeleteView"
)

class CloudInforListView(PermissionsMixin, TemplateView):
    model = CloudInfor
    template_name = 'elastics/cloud_info_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Cloud info list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CloudInforCreateView(PermissionsMixin, CreateView):
    model = CloudInfor
    form_class = CloudInforForm
    template_name = 'elastics/cloud_info_create_update.html'
    success_url = reverse_lazy('elastics:cloud-info-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Create cloud info'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CloudInforUpdateView(PermissionsMixin, UpdateView):
    model = CloudInfor
    template_name = 'elastics/cloud_info_create_update.html'
    form_class = CloudInforForm
    success_url = reverse_lazy('elastics:cloud-info-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Update cloud info'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CloudInforDetailView(PermissionsMixin, DetailView):
    model = CloudInfor
    template_name = 'elastics/cloud_info_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Cloud info detail')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CloudInforDeleteView(PermissionsMixin, DeleteView):
    model = CloudInfor
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('elastics:cloud-info-list')
    permission_classes = [IsOrgAdmin]