# coding: utf-8

"""
    Merge HRIS API

    The unified API for building rich integrations with multiple HR Information System platforms.  # noqa: E501

    The version of the OpenAPI document: 1.0
    Contact: hello@merge.dev
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from MergeHRISClient.api_client import ApiClient
from MergeHRISClient.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class CreateLinkTokenApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_link_token_create(self, create_linked_account_config_deserializer, **kwargs):  # noqa: E501
        """create_link_token_create  # noqa: E501

        Creates a link token to be used when linking a new end user.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_link_token_create(create_linked_account_config_deserializer, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CreateLinkedAccountConfigDeserializer create_linked_account_config_deserializer: (required)
        :param str production_key: The requesting organization's production key.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: LinkToken
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_link_token_create_with_http_info(create_linked_account_config_deserializer, **kwargs)  # noqa: E501

    def create_link_token_create_with_http_info(self, create_linked_account_config_deserializer, **kwargs):  # noqa: E501
        """create_link_token_create  # noqa: E501

        Creates a link token to be used when linking a new end user.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_link_token_create_with_http_info(create_linked_account_config_deserializer, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CreateLinkedAccountConfigDeserializer create_linked_account_config_deserializer: (required)
        :param str production_key: The requesting organization's production key.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(LinkToken, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'create_linked_account_config_deserializer',
            'production_key'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_link_token_create" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'create_linked_account_config_deserializer' is set
        if self.api_client.client_side_validation and ('create_linked_account_config_deserializer' not in local_var_params or  # noqa: E501
                                                        local_var_params['create_linked_account_config_deserializer'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `create_linked_account_config_deserializer` when calling `create_link_token_create`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'production_key' in local_var_params and local_var_params['production_key'] is not None:  # noqa: E501
            query_params.append(('production_key', local_var_params['production_key']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_linked_account_config_deserializer' in local_var_params:
            body_params = local_var_params['create_linked_account_config_deserializer']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        return self.api_client.call_api(
            '/create-link-token', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LinkToken',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
