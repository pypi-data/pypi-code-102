# -*- coding: utf-8 -*-
"""
@  time    : 2021/03/30
@  author  : XieYZ
"""
from rest_framework import exceptions
from rest_framework.permissions import BasePermission

from .user import perm_check


class CheckActionPermMixin(BasePermission):

    authenticated_users_only = True
    message = '没有权限进行此操作！'

    def has_permission(self, request, view):
        method = request.method
        permissions_map = {
            "GET": "",
            "OPTIONS": "",
            "HEAD": "",
            "POST": "",
            "PUT": "",
            "PATCH": "",
            "DELETE": "",
        }
        if hasattr(view, 'permission_actions_map') and view.action in view.permission_actions_map and method in \
                view.permission_actions_map[view.action]:
            permissions_map.update(view.permission_actions_map[view.action])
        elif hasattr(view, 'permissions_map'):
            permissions_map.update(view.permissions_map)
        if not request.user and self.authenticated_users_only:
            return False
        if method in permissions_map:
            perm = permissions_map[method]
            if not perm:
                return True
            else:
                return perm_check(request.user["id"], perm)
        else:
            raise exceptions.MethodNotAllowed(method)
