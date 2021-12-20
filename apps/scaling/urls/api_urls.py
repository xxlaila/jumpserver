# -*- coding: utf-8 -*-
"""
@File    : api_urls.py
@Time    : 2021/12/15 2:51 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.urls import path, re_path
from rest_framework_nested import routers
from rest_framework_bulk.routes import BulkRouter
from common import api as capi
from .. import views
from .. import api

app_name = 'scaling'

router = BulkRouter()
router.register(r'scaling-assets', api.AssetExpansionViewSet, 'scaling-asset')
router.register(r'disks', api.AssetExpansionViewSet, 'disk')

urlpatterns = [
]

old_version_urlpatterns = [
    re_path('(?P<resource>scaling-asset|disk)/.*', capi.redirect_plural_name_api)
]

urlpatterns += router.urls