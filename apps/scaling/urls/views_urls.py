# -*- coding: utf-8 -*-
"""
@File    : views_urls.py
@Time    : 2021/12/15 2:51 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.urls import path
from .. import views
from .. import utils

app_name = 'scaling'

urlpatterns = [
    path('asset-list/', views.AssetExpansionListView.as_view(), name='scaling-asset-list'),
    path('asset-list/<uuid:pk>/', views.AssetExpansionDetailView.as_view(), name='scaling-asset-detail'),
    path('asset-list/<uuid:pk>/disk/', views.AssetDiskInfoListView.as_view(), name='scaling-disk-list'),
    path('disk/', views.DiskInfoListView.as_view(), name='disk-list'),
    path('disk/<uuid:pk>/', views.DiskInfoDetailView.as_view(), name='disk-detail'),

    path('sync-node/', utils.cloud_asset_rsync, name='sync-node'),
]
