# -*- coding: utf-8 -*-
"""
@File    : hands.py
@Time    : 2021/10/21 10:05 上午
@Author  : xxlaila
@Software: PyCharm
"""
from common.permissions import IsAppUser, IsOrgAdmin, IsValidUser, IsOrgAdminOrAppUser
from users.models import User, UserGroup