# -*- coding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2021/10/26 7:49 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.utils.translation import ugettext as _

from common.utils import get_logger

logger = get_logger(__file__)
__all__ = [
    'clean_ansible_task_hosts', 'clean_ansible_task_hosts',
    'check_asset_can_run_ansible'
]

def check_asset_can_run_ansible(asset):
    if not asset.is_active:
        msg = _("Asset has been disabled, skipped: {}").format(asset)
        logger.info(msg)
        return False
    if not asset.is_support_ansible():
        msg = _("Asset may not be support ansible, skipped: {}").format(asset)
        logger.info(msg)
        return False
    return True

def check_system_user_can_run_ansible(system_user):
    if not system_user.is_need_push():
        msg = _("Push system user task skip, auto push not enable or "
                "protocol is not ssh or rdp: {}").format(system_user.name)
        logger.info(msg)
        return False

    # Push root as system user is dangerous
    if system_user.username.lower() in ["root", "administrator"]:
        msg = _("For security, do not push user {}".format(system_user.username))
        logger.info(msg)
        return False

def check_system_user_can_run_ansible(system_user):
    if not system_user.is_need_push():
        msg = _("Push system user task skip, auto push not enable or "
                "protocol is not ssh or rdp: {}").format(system_user.name)
        logger.info(msg)
        return False

    # Push root as system user is dangerous
    if system_user.username.lower() in ["root", "administrator"]:
        msg = _("For security, do not push user {}".format(system_user.username))
        logger.info(msg)
        return False

    # if system_user.protocol != "ssh":
    #     msg = _("System user protocol not ssh: {}".format(system_user))
    #     logger.info(msg)
    #     return False
    return True

def clean_ansible_task_hosts(assets, system_user=None):
    if system_user and not check_system_user_can_run_ansible(system_user):
        return []
    cleaned_assets = []
    for asset in assets:
        if not check_asset_can_run_ansible(asset):
            continue
        cleaned_assets.append(asset)
    if not cleaned_assets:
        logger.info(_("No assets matched, stop task"))
    return cleaned_assets