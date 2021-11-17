# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_ansible.configuration import Configuration


class AnsibleGitRemoteResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'client_cert': 'str',
        'ca_cert': 'str',
        'pulp_last_updated': 'datetime',
        'pulp_href': 'str',
        'connect_timeout': 'float',
        'headers': 'list[object]',
        'name': 'str',
        'tls_validation': 'bool',
        'proxy_url': 'str',
        'sock_read_timeout': 'float',
        'pulp_labels': 'object',
        'download_concurrency': 'int',
        'url': 'str',
        'rate_limit': 'int',
        'max_retries': 'int',
        'pulp_created': 'datetime',
        'total_timeout': 'float',
        'sock_connect_timeout': 'float',
        'metadata_only': 'bool'
    }

    attribute_map = {
        'client_cert': 'client_cert',
        'ca_cert': 'ca_cert',
        'pulp_last_updated': 'pulp_last_updated',
        'pulp_href': 'pulp_href',
        'connect_timeout': 'connect_timeout',
        'headers': 'headers',
        'name': 'name',
        'tls_validation': 'tls_validation',
        'proxy_url': 'proxy_url',
        'sock_read_timeout': 'sock_read_timeout',
        'pulp_labels': 'pulp_labels',
        'download_concurrency': 'download_concurrency',
        'url': 'url',
        'rate_limit': 'rate_limit',
        'max_retries': 'max_retries',
        'pulp_created': 'pulp_created',
        'total_timeout': 'total_timeout',
        'sock_connect_timeout': 'sock_connect_timeout',
        'metadata_only': 'metadata_only'
    }

    def __init__(self, client_cert=None, ca_cert=None, pulp_last_updated=None, pulp_href=None, connect_timeout=None, headers=None, name=None, tls_validation=None, proxy_url=None, sock_read_timeout=None, pulp_labels=None, download_concurrency=None, url=None, rate_limit=None, max_retries=None, pulp_created=None, total_timeout=None, sock_connect_timeout=None, metadata_only=None, local_vars_configuration=None):  # noqa: E501
        """AnsibleGitRemoteResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._client_cert = None
        self._ca_cert = None
        self._pulp_last_updated = None
        self._pulp_href = None
        self._connect_timeout = None
        self._headers = None
        self._name = None
        self._tls_validation = None
        self._proxy_url = None
        self._sock_read_timeout = None
        self._pulp_labels = None
        self._download_concurrency = None
        self._url = None
        self._rate_limit = None
        self._max_retries = None
        self._pulp_created = None
        self._total_timeout = None
        self._sock_connect_timeout = None
        self._metadata_only = None
        self.discriminator = None

        self.client_cert = client_cert
        self.ca_cert = ca_cert
        if pulp_last_updated is not None:
            self.pulp_last_updated = pulp_last_updated
        if pulp_href is not None:
            self.pulp_href = pulp_href
        self.connect_timeout = connect_timeout
        if headers is not None:
            self.headers = headers
        self.name = name
        if tls_validation is not None:
            self.tls_validation = tls_validation
        self.proxy_url = proxy_url
        self.sock_read_timeout = sock_read_timeout
        if pulp_labels is not None:
            self.pulp_labels = pulp_labels
        self.download_concurrency = download_concurrency
        self.url = url
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.total_timeout = total_timeout
        self.sock_connect_timeout = sock_connect_timeout
        if metadata_only is not None:
            self.metadata_only = metadata_only

    @property
    def client_cert(self):
        """Gets the client_cert of this AnsibleGitRemoteResponse.  # noqa: E501

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :return: The client_cert of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: str
        """
        return self._client_cert

    @client_cert.setter
    def client_cert(self, client_cert):
        """Sets the client_cert of this AnsibleGitRemoteResponse.

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :param client_cert: The client_cert of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: str
        """

        self._client_cert = client_cert

    @property
    def ca_cert(self):
        """Gets the ca_cert of this AnsibleGitRemoteResponse.  # noqa: E501

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :return: The ca_cert of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert):
        """Sets the ca_cert of this AnsibleGitRemoteResponse.

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :param ca_cert: The ca_cert of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: str
        """

        self._ca_cert = ca_cert

    @property
    def pulp_last_updated(self):
        """Gets the pulp_last_updated of this AnsibleGitRemoteResponse.  # noqa: E501

        Timestamp of the most recent update of the remote.  # noqa: E501

        :return: The pulp_last_updated of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_last_updated

    @pulp_last_updated.setter
    def pulp_last_updated(self, pulp_last_updated):
        """Sets the pulp_last_updated of this AnsibleGitRemoteResponse.

        Timestamp of the most recent update of the remote.  # noqa: E501

        :param pulp_last_updated: The pulp_last_updated of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_last_updated = pulp_last_updated

    @property
    def pulp_href(self):
        """Gets the pulp_href of this AnsibleGitRemoteResponse.  # noqa: E501


        :return: The pulp_href of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this AnsibleGitRemoteResponse.


        :param pulp_href: The pulp_href of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def connect_timeout(self):
        """Gets the connect_timeout of this AnsibleGitRemoteResponse.  # noqa: E501

        aiohttp.ClientTimeout.connect (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :return: The connect_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: float
        """
        return self._connect_timeout

    @connect_timeout.setter
    def connect_timeout(self, connect_timeout):
        """Sets the connect_timeout of this AnsibleGitRemoteResponse.

        aiohttp.ClientTimeout.connect (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :param connect_timeout: The connect_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                connect_timeout is not None and connect_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `connect_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._connect_timeout = connect_timeout

    @property
    def headers(self):
        """Gets the headers of this AnsibleGitRemoteResponse.  # noqa: E501

        Headers for aiohttp.Clientsession  # noqa: E501

        :return: The headers of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: list[object]
        """
        return self._headers

    @headers.setter
    def headers(self, headers):
        """Sets the headers of this AnsibleGitRemoteResponse.

        Headers for aiohttp.Clientsession  # noqa: E501

        :param headers: The headers of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: list[object]
        """

        self._headers = headers

    @property
    def name(self):
        """Gets the name of this AnsibleGitRemoteResponse.  # noqa: E501

        A unique name for this remote.  # noqa: E501

        :return: The name of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AnsibleGitRemoteResponse.

        A unique name for this remote.  # noqa: E501

        :param name: The name of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def tls_validation(self):
        """Gets the tls_validation of this AnsibleGitRemoteResponse.  # noqa: E501

        If True, TLS peer validation must be performed.  # noqa: E501

        :return: The tls_validation of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: bool
        """
        return self._tls_validation

    @tls_validation.setter
    def tls_validation(self, tls_validation):
        """Sets the tls_validation of this AnsibleGitRemoteResponse.

        If True, TLS peer validation must be performed.  # noqa: E501

        :param tls_validation: The tls_validation of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: bool
        """

        self._tls_validation = tls_validation

    @property
    def proxy_url(self):
        """Gets the proxy_url of this AnsibleGitRemoteResponse.  # noqa: E501

        The proxy URL. Format: scheme://host:port  # noqa: E501

        :return: The proxy_url of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: str
        """
        return self._proxy_url

    @proxy_url.setter
    def proxy_url(self, proxy_url):
        """Sets the proxy_url of this AnsibleGitRemoteResponse.

        The proxy URL. Format: scheme://host:port  # noqa: E501

        :param proxy_url: The proxy_url of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: str
        """

        self._proxy_url = proxy_url

    @property
    def sock_read_timeout(self):
        """Gets the sock_read_timeout of this AnsibleGitRemoteResponse.  # noqa: E501

        aiohttp.ClientTimeout.sock_read (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :return: The sock_read_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: float
        """
        return self._sock_read_timeout

    @sock_read_timeout.setter
    def sock_read_timeout(self, sock_read_timeout):
        """Sets the sock_read_timeout of this AnsibleGitRemoteResponse.

        aiohttp.ClientTimeout.sock_read (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :param sock_read_timeout: The sock_read_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sock_read_timeout is not None and sock_read_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sock_read_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sock_read_timeout = sock_read_timeout

    @property
    def pulp_labels(self):
        """Gets the pulp_labels of this AnsibleGitRemoteResponse.  # noqa: E501


        :return: The pulp_labels of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: object
        """
        return self._pulp_labels

    @pulp_labels.setter
    def pulp_labels(self, pulp_labels):
        """Sets the pulp_labels of this AnsibleGitRemoteResponse.


        :param pulp_labels: The pulp_labels of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: object
        """

        self._pulp_labels = pulp_labels

    @property
    def download_concurrency(self):
        """Gets the download_concurrency of this AnsibleGitRemoteResponse.  # noqa: E501

        Total number of simultaneous connections. If not set then the default value will be used.  # noqa: E501

        :return: The download_concurrency of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: int
        """
        return self._download_concurrency

    @download_concurrency.setter
    def download_concurrency(self, download_concurrency):
        """Sets the download_concurrency of this AnsibleGitRemoteResponse.

        Total number of simultaneous connections. If not set then the default value will be used.  # noqa: E501

        :param download_concurrency: The download_concurrency of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                download_concurrency is not None and download_concurrency < 1):  # noqa: E501
            raise ValueError("Invalid value for `download_concurrency`, must be a value greater than or equal to `1`")  # noqa: E501

        self._download_concurrency = download_concurrency

    @property
    def url(self):
        """Gets the url of this AnsibleGitRemoteResponse.  # noqa: E501

        The URL of an external content source.  # noqa: E501

        :return: The url of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this AnsibleGitRemoteResponse.

        The URL of an external content source.  # noqa: E501

        :param url: The url of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and url is None:  # noqa: E501
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def rate_limit(self):
        """Gets the rate_limit of this AnsibleGitRemoteResponse.  # noqa: E501

        Limits total download rate in requests per second  # noqa: E501

        :return: The rate_limit of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: int
        """
        return self._rate_limit

    @rate_limit.setter
    def rate_limit(self, rate_limit):
        """Sets the rate_limit of this AnsibleGitRemoteResponse.

        Limits total download rate in requests per second  # noqa: E501

        :param rate_limit: The rate_limit of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: int
        """

        self._rate_limit = rate_limit

    @property
    def max_retries(self):
        """Gets the max_retries of this AnsibleGitRemoteResponse.  # noqa: E501

        Maximum number of retry attempts after a download failure. If not set then the default value (3) will be used.  # noqa: E501

        :return: The max_retries of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: int
        """
        return self._max_retries

    @max_retries.setter
    def max_retries(self, max_retries):
        """Sets the max_retries of this AnsibleGitRemoteResponse.

        Maximum number of retry attempts after a download failure. If not set then the default value (3) will be used.  # noqa: E501

        :param max_retries: The max_retries of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: int
        """

        self._max_retries = max_retries

    @property
    def pulp_created(self):
        """Gets the pulp_created of this AnsibleGitRemoteResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this AnsibleGitRemoteResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def total_timeout(self):
        """Gets the total_timeout of this AnsibleGitRemoteResponse.  # noqa: E501

        aiohttp.ClientTimeout.total (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :return: The total_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: float
        """
        return self._total_timeout

    @total_timeout.setter
    def total_timeout(self, total_timeout):
        """Sets the total_timeout of this AnsibleGitRemoteResponse.

        aiohttp.ClientTimeout.total (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :param total_timeout: The total_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                total_timeout is not None and total_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `total_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._total_timeout = total_timeout

    @property
    def sock_connect_timeout(self):
        """Gets the sock_connect_timeout of this AnsibleGitRemoteResponse.  # noqa: E501

        aiohttp.ClientTimeout.sock_connect (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :return: The sock_connect_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: float
        """
        return self._sock_connect_timeout

    @sock_connect_timeout.setter
    def sock_connect_timeout(self, sock_connect_timeout):
        """Sets the sock_connect_timeout of this AnsibleGitRemoteResponse.

        aiohttp.ClientTimeout.sock_connect (q.v.) for download-connections. The default is null, which will cause the default from the aiohttp library to be used.  # noqa: E501

        :param sock_connect_timeout: The sock_connect_timeout of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sock_connect_timeout is not None and sock_connect_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sock_connect_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sock_connect_timeout = sock_connect_timeout

    @property
    def metadata_only(self):
        """Gets the metadata_only of this AnsibleGitRemoteResponse.  # noqa: E501

        If True, only metadata about the content will be stored in Pulp. Clients will retrieve content from the remote URL.  # noqa: E501

        :return: The metadata_only of this AnsibleGitRemoteResponse.  # noqa: E501
        :rtype: bool
        """
        return self._metadata_only

    @metadata_only.setter
    def metadata_only(self, metadata_only):
        """Sets the metadata_only of this AnsibleGitRemoteResponse.

        If True, only metadata about the content will be stored in Pulp. Clients will retrieve content from the remote URL.  # noqa: E501

        :param metadata_only: The metadata_only of this AnsibleGitRemoteResponse.  # noqa: E501
        :type: bool
        """

        self._metadata_only = metadata_only

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AnsibleGitRemoteResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AnsibleGitRemoteResponse):
            return True

        return self.to_dict() != other.to_dict()
