# -*- coding: utf-8 -*-
"""
@  time    : 2021/04/01
@  author  : XieYZ
"""
from django.core.cache import cache
from django.conf import settings

from jsonrpc.proxy import ServiceProxy

USER_INFO_KEY_PREFIX = "user_info"


def get_user_info_by_rpc(user_id):
    s = ServiceProxy(settings.AUTH_SERVICE_RPC_API)
    res = s.usercenter.get_user_info(user_id)
    if not res or not res.get("error"):
        result = res.get("result", None)
        cache.set(f"{USER_INFO_KEY_PREFIX}_{user_id}", result, timeout=3600)
        return result
    return None


def user_info(user_id):
    data = cache.get(f"{USER_INFO_KEY_PREFIX}_{user_id}")
    if not data:
        data = get_user_info_by_rpc(user_id)
    return data


def perm_check(user_id, perm):
    s = ServiceProxy(settings.AUTH_SERVICE_RPC_API)
    res = s.usercenter.permission_check(user_id, perm)
    if not res or not res.get("error"):
        return res.get("result", False)
    return False
