# -*- coding: utf-8 -*-
"""
@File    : gather_metainfo_test_connect.py
@Time    : 2021/10/26 6:52 下午
@Author  : xxlaila
@Software: PyCharm
"""
from celery import shared_task
from django.utils.translation import ugettext as _
from common.utils import get_logger
from orgs.utils import org_aware_func
# from .utils import clean_ansible_task_hosts, group_asset_by_platform
from ..utils import server_port_connect, server_ping
from ..models import MetaInfo


logger = get_logger(__file__)
__all__ = [
    'test_mete_info_network_manual', 'test_mete_info_port_manual',
    # 'test_mete_info_network_util', 'test_mete_info_port_util'
]

# @shared_task
# @org_aware_func("meteinfo")
# def test_mete_info_network_util(meteinfo, task_name=None):
#     """
#     Using ansible api to update asset hardware info
#     :param assets:  asset seq
#     :param task_name: task_name running
#     :return: result summary ['contacted': {}, 'dark': {}]
#     """
#     if task_name is None:
#         task_name = _("Test network connectivity")
#     ip = meteinfo.address.split(':')[0]
#     port = meteinfo.address.split(':')[1]
#     task, created = server_port_connect(
#         [task_name, ip, port],
#     )
#     result = task.run()
#     return True

# @shared_task(queue="")
# @org_aware_func("meteinfo")
# def test_mete_info_port_util(meteinfo, task_name=None):
#     if task_name is None:
#         task_name = _("Test meteinfo connectivity")


# @shared_task(queue="")
# def test_mete_info_network_manual(meteinfo):
#     task_name = _("test server network: {}").format(meteinfo.address.split(':')[0])
#     test_mete_info_network_util([meteinfo], task_name=task_name)


# @shared_task(queue="")
# def test_mete_info_port_manual(meteinfo):
#     task_name = _("Test assets connectivity: {}").format(meteinfo)
#     summary = test_mete_info_port_util([meteinfo], task_name=task_name)
# 
#     if summary.get('dark'):
#         return False, summary['dark']
#     else:
#         return True, ""

def test_mete_info_network_manual(meteinfo):
    task_name = _("test server network: {}").format(meteinfo.address.split(':')[0])
    print(task_name)
    created = server_port_connect([task_name, meteinfo.address.split(':')[0], meteinfo.address.split(':')[1]])
    return created

def test_mete_info_port_manual(meteinfo):
    task_name = _("test server network: {}").format(meteinfo.address.split(':')[0])
    created = server_ping(meteinfo.address.split(':')[0])
    return created