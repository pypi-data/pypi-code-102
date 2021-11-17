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

from pulpcore.client.pulp_ostree.configuration import Configuration


class OstreeRepoImport(object):
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
        'artifact': 'str',
        'repository_name': 'str',
        'ref': 'str',
        'parent_commit': 'str'
    }

    attribute_map = {
        'artifact': 'artifact',
        'repository_name': 'repository_name',
        'ref': 'ref',
        'parent_commit': 'parent_commit'
    }

    def __init__(self, artifact=None, repository_name=None, ref=None, parent_commit=None, local_vars_configuration=None):  # noqa: E501
        """OstreeRepoImport - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._artifact = None
        self._repository_name = None
        self._ref = None
        self._parent_commit = None
        self.discriminator = None

        self.artifact = artifact
        self.repository_name = repository_name
        if ref is not None:
            self.ref = ref
        if parent_commit is not None:
            self.parent_commit = parent_commit

    @property
    def artifact(self):
        """Gets the artifact of this OstreeRepoImport.  # noqa: E501

        An artifact representing OSTree content compressed as a tarball.  # noqa: E501

        :return: The artifact of this OstreeRepoImport.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this OstreeRepoImport.

        An artifact representing OSTree content compressed as a tarball.  # noqa: E501

        :param artifact: The artifact of this OstreeRepoImport.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and artifact is None:  # noqa: E501
            raise ValueError("Invalid value for `artifact`, must not be `None`")  # noqa: E501

        self._artifact = artifact

    @property
    def repository_name(self):
        """Gets the repository_name of this OstreeRepoImport.  # noqa: E501

        The name of a repository that contains the compressed OSTree content.  # noqa: E501

        :return: The repository_name of this OstreeRepoImport.  # noqa: E501
        :rtype: str
        """
        return self._repository_name

    @repository_name.setter
    def repository_name(self, repository_name):
        """Sets the repository_name of this OstreeRepoImport.

        The name of a repository that contains the compressed OSTree content.  # noqa: E501

        :param repository_name: The repository_name of this OstreeRepoImport.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and repository_name is None:  # noqa: E501
            raise ValueError("Invalid value for `repository_name`, must not be `None`")  # noqa: E501

        self._repository_name = repository_name

    @property
    def ref(self):
        """Gets the ref of this OstreeRepoImport.  # noqa: E501

        The name of a ref branch that holds the reference to the last commit.  # noqa: E501

        :return: The ref of this OstreeRepoImport.  # noqa: E501
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """Sets the ref of this OstreeRepoImport.

        The name of a ref branch that holds the reference to the last commit.  # noqa: E501

        :param ref: The ref of this OstreeRepoImport.  # noqa: E501
        :type: str
        """

        self._ref = ref

    @property
    def parent_commit(self):
        """Gets the parent_commit of this OstreeRepoImport.  # noqa: E501

        The checksum of a parent commit with which the content needs to be associated.  # noqa: E501

        :return: The parent_commit of this OstreeRepoImport.  # noqa: E501
        :rtype: str
        """
        return self._parent_commit

    @parent_commit.setter
    def parent_commit(self, parent_commit):
        """Sets the parent_commit of this OstreeRepoImport.

        The checksum of a parent commit with which the content needs to be associated.  # noqa: E501

        :param parent_commit: The parent_commit of this OstreeRepoImport.  # noqa: E501
        :type: str
        """

        self._parent_commit = parent_commit

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
        if not isinstance(other, OstreeRepoImport):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OstreeRepoImport):
            return True

        return self.to_dict() != other.to_dict()
