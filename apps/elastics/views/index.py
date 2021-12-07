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
from ..utils import get_indexs_connent, delete_index, index_shards_num, create_index
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
    "IndexListView", "IndexDetailView", "IndexCreateView", "IndexShardsNodeView"
)
logger = get_logger(__name__)

class IndexListView(PermissionsMixin, TemplateView):
    template_name = 'elastics/index_list.html'
    model = Index
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = get_indexs_connent()
        return super().get(request, *args, **kwargs)

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

from django.shortcuts import (
    render, redirect
)
class IndexCreateView(PermissionsMixin, APIView):
    
    form_class = IndexForm
    template_name = 'elastics/index_create.html'
    
    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        info_forms = self.form_class(request.POST)

        if info_forms.is_valid():
            print("ok")
            name = info_forms.changed_data.get("name")
            pri = info_forms.cleaned_data.get("pri")
            rep = info_forms.cleaned_data.get("rep")
            mapping = info_forms.cleaned_data.get('mapping')
            # metainfo = info_forms.cleaned_data['metainfo']
            metainfo = request.POST.getlist('metainfo')
            print(name)
            print(metainfo, mapping)

            # settings = {
            #     "settings": {
            #         "number_of_shards": pri,
            #         "number_of_replicas": rep
            #     }
            # }
            # results = create_index(MetaInfo.objects.get(id=str(metainfo).replace("-", "")), name, body=settings)
            # if results:
            #     pass
        else:
            print("no")
        from django.http import HttpResponse
        return HttpResponse("ok")


    # model = MetaInfo
    # form_class = IndexForm
    # template_name = 'elastics/index_create.html'
    # success_url = reverse_lazy('elastics:index-list')
    # success_message = create_success_msg
    # permission_classes = [IsOrgAdmin]
    #
    # def get_context_data(self, **kwargs):
    #     context = {
    #         'app': _('Elastics'),
    #         'action': _('Create index'),
    #         'type': 'create'
    #     }
    #     kwargs.update(context)
    #     return super().get_context_data(**kwargs)

class IndexDeleteView(PermissionsMixin, DeleteView):
    model = Index
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('elastics:index-list')
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        old = Index.objects.filter(id=self.kwargs['pk'])
        result = delete_index(old)
        return Response({"status": result}, status=200)

class IndexShardsNodeView(PermissionsMixin, SingleObjectMixin, TemplateView):

    template_name = 'elastics/index_detail.html'
    model = Index
    object = None
    permission_classes = [IsOrgAdmin]

    def index_shards(self):
        data = self.model.objects.get(id=self.kwargs['pk'])
        result = index_shards_num(data)
        return result

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Elastics'),
            'action': _('Index shards'),
            'shards': self.index_shards(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)




