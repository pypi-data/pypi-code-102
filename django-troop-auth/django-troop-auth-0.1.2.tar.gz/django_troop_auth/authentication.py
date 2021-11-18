# -*- coding: utf-8 -*-
"""
@  time    : 2021/03/30
@  author  : XieYZ
"""
import jwt
from django.utils.encoding import smart_text

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework_jwt.settings import api_settings

from .user import user_info

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class BaseJSONWebTokenAuthentication(BaseAuthentication):
    """
    身份验证
    """
    JWT_AUTH_HEADER_PREFIX = "Bearer"
    JWT_AUTH_COOKIE = "Authorization"

    def authenticate(self, request):
        """
        验证TOKEN是否有效，如果有效，返回User和TOKEN，否则返回None
        """

        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            raise exceptions.AuthenticationFailed()

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = '凭证已过期'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = '无效的凭证'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = '凭证已失效'
            raise exceptions.AuthenticationFailed(msg)
        user = self.authenticate_credentials(payload)
        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        user = user_info(payload["user_id"])

        if not user:
            msg = '用户不存在'
            raise exceptions.NotFound(msg)

        email = user.get("email")
        if not email:
            msg = '无效的 payload.'
            raise exceptions.AuthenticationFailed(msg)

        is_active = user.get("is_active")
        if not is_active:
            msg = '账户已被禁用'
            raise exceptions.AuthenticationFailed(msg)

        return user


class Authentication(BaseJSONWebTokenAuthentication):
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None
        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        return auth[1]

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
