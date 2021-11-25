# -*- coding: utf-8 -*-
"""
@File    : api_urls.py
@Time    : 2021/10/19 3:37 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.urls import path, re_path
from rest_framework_nested import routers
from rest_framework_bulk.routes import BulkRouter
from common import api as capi
from .. import views

from .. import api

app_name = 'elastics'

router = BulkRouter()
router.register(r'cloud-infos', api.CloudInfoViewSet, 'cloud-info')
router.register(r'meta-infos', api.MetaInfoViewSet, 'meta-info')
router.register(r'basicclusters', api.BasicclusterViewSet, 'basiccluster')
router.register(r'nodes', api.EsNodeViewSet, 'node')
router.register(r'indexs', api.IndexViewSet, 'index')
router.register(r'nodeindices', api.IndiceNodeViewSet, 'nodeindice')

urlpatterns = [
    path('metainfo/<uuid:pk>/tasks/', api.MetaInfoTaskCreateApi.as_view(), name='metainfo-task-create'),
    path('metainfo/<uuid:pk>/basiccluster/', api.BasicClusterListApi.as_view(), name='basic-cluster-list'),
    path('gateways/<uuid:pk>/test-serverport/', api.ServerPortConnectApi.as_view(), name='test-server-port'),
    path('gateways/<uuid:pk>/test-network/', api.ServerPingApi.as_view(), name='test-server-ping'),

]

old_version_urlpatterns = [
    re_path('(?P<resource>cloud-info|meta-info|nodeindice|node|index|basiccluster)/.*', capi.redirect_plural_name_api)
]

urlpatterns += router.urls
