# -*- coding: utf-8 -*-
"""
@File    : index.py
@Time    : 2021/11/10 10:27 上午
@Author  : xxlaila
@Software: PyCharm
"""
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from common.permissions import PermissionsMixin, IsOrgAdmin, IsOrgAdminOrAppUser, IsValidUser
from ..utils import get_indexs_connent,delete_index
from common.utils import get_logger
from django.urls import reverse_lazy
from common.const import create_success_msg, update_success_msg
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, DetailView
)
from ..models import Index, MetaInfo
from ..forms import IndexForm
from rest_framework.views import APIView, Response


__all__ = (
    "IndexListView", "IndexDetailView", "IndexCreateView"
)
logger = get_logger(__name__)

class IndexListView(PermissionsMixin, TemplateView):
    template_name = 'elastics/index_list.html'
    model = Index
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Index list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class IndexDetailView(PermissionsMixin, DetailView):
    model = Index
    template_name = 'elastics/index_detail.html'
    permission_classes = [IsOrgAdmin]
    object = None

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Index detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class IndexCreateView(PermissionsMixin, CreateView):
    model = MetaInfo
    form_class = IndexForm
    template_name = 'elastics/index_create.html'
    success_url = reverse_lazy('elastics:index-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Create index'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class IndexDeleteView(PermissionsMixin, DeleteView):
    model = Index
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('elastics:index-list')
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        old = Index.objects.filter(id=self.kwargs['pk'])
        result = delete_index(old)
        return Response({"status": result}, status=200)





