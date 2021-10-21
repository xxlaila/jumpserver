# -*- coding: utf-8 -*-
"""
@File    : views_urls.py
@Time    : 2021/10/19 3:38 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.urls import path
from .. import views

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

]
