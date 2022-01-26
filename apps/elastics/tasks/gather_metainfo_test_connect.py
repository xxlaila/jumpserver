# -*- coding: utf-8 -*-
"""
@File    : gather_metainfo_test_connect.py
@Time    : 2021/10/26 6:52 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.utils.translation import ugettext as _
from common.utils import get_logger
from ..utils import server_port_connect, server_ping

logger = get_logger(__file__)

def test_mete_info_network_manual(meteinfo):
    task_name = _("test server network: {}").format(meteinfo.address.split(':')[0])
    created = server_ping(meteinfo.address.split(':')[0])
    return created

def test_mete_info_port_manual(meteinfo):
    task_name = _("test server network: {}").format(meteinfo.address.split(':')[0])
    created = server_port_connect([task_name, meteinfo.address.split(':')[0], meteinfo.address.split(':')[1]])
    return created