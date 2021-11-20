# -*- coding: utf-8 -*-
"""
@File    : views_urls.py
@Time    : 2021/10/19 3:38 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.urls import path
from .. import views
from .. import utils

app_name = 'elastics'

urlpatterns = [
    path('cloud-info/', views.CloudInforListView.as_view(), name='cloud-info-list'),
    path('cloud-info/create/', views.CloudInforCreateView.as_view(), name='cloud-info-create'),
    path('cloud-info/<uuid:pk>/update/', views.CloudInforUpdateView.as_view(), name='cloud-info-update'),
    path('cloud-info/<uuid:pk>/', views.CloudInforDetailView.as_view(), name='cloud-info-detail'),
    path('cloud-info/<uuid:pk>/delete/', views.CloudInforDeleteView.as_view(), name='cloud-info-delete'),
    path('meta-info/', views.MetaInfoListView.as_view(), name='meta-info-list'),
    path('meta-info/create/', views.MetaInfoCreateView.as_view(), name='meta-info-create'),
    path('meta-info/<uuid:pk>/update/', views.MetaInfoUpdateView.as_view(), name='meta-info-update'),
    path('meta-info/<uuid:pk>/', views.MetaInfoDetailView.as_view(), name='meta-info-detail'),
    path('meta-info/<uuid:pk>/delete/', views.MetaInfoDeleteView.as_view(), name='meta-info-delete'),
    path('meta-info/<uuid:pk>/basiccluster/', views.BasicClusterListView.as_view(), name='basic-cluster-list'),
    path('meta-info/<uuid:pk>/cluterremote/', views.ClusterRemoteListView.as_view(), name='cluster-remote-list'),
    path('meta-info/<uuid:pk>/node/', views.NodeListView.as_view(), name='node-list'),
    path('node/<uuid:pk>/', views.NodeDetailView.as_view(), name='node-detail'),
    path('node/<uuid:pk>/update/', views.NodeUpdateView.as_view(), name='node-update'),
    path('node/<uuid:pk>/indices/', views.NodeStatsDetailView.as_view(), name='node-indices'),
    path('node/<uuid:pk>/online/', views.NodeOnlineView.as_view(), name='node-online'),
    path('cluterremote/<uuid:pk>/update/', views.ClusterRemoteInfoUpdateView.as_view(), name='cluster-remote-update'),
    path('default-settings/<uuid:pk>/update/', views.DefaultSettingsUpdateView.as_view(),
         name='default-settings-update'),
    path('basic-cluster/<uuid:pk>/update/', views.BasicClusterUpdateView.as_view(),
         name='basic-cluster-update'),
    path('index/', views.IndexListView.as_view(), name='index-list'),
    path('index/<uuid:pk>/', views.IndexDetailView.as_view(), name='index-detail'),
    path('index/create/', views.IndexCreateView.as_view(), name='index-create'),



    path('meta-info/health/', utils.get_indexs_connent, name='meta-info-health'),

]
