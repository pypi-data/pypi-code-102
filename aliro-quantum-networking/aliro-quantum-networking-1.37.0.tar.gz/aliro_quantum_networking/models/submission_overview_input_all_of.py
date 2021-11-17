# coding: utf-8

"""
    Aliro Q.Network

    This is an api for the Aliro Q.Network  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from aliro_quantum_networking.configuration import Configuration


class SubmissionOverviewInputAllOf(object):
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
        'submission_overview_type': 'str'
    }

    attribute_map = {
        'submission_overview_type': 'submissionOverviewType'
    }

    def __init__(self, submission_overview_type=None, local_vars_configuration=None):  # noqa: E501
        """SubmissionOverviewInputAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._submission_overview_type = None
        self.discriminator = None

        self.submission_overview_type = submission_overview_type

    @property
    def submission_overview_type(self):
        """Gets the submission_overview_type of this SubmissionOverviewInputAllOf.  # noqa: E501

        Must be \"SubmissionOverviewInput\"  # noqa: E501

        :return: The submission_overview_type of this SubmissionOverviewInputAllOf.  # noqa: E501
        :rtype: str
        """
        return self._submission_overview_type

    @submission_overview_type.setter
    def submission_overview_type(self, submission_overview_type):
        """Sets the submission_overview_type of this SubmissionOverviewInputAllOf.

        Must be \"SubmissionOverviewInput\"  # noqa: E501

        :param submission_overview_type: The submission_overview_type of this SubmissionOverviewInputAllOf.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and submission_overview_type is None:  # noqa: E501
            raise ValueError("Invalid value for `submission_overview_type`, must not be `None`")  # noqa: E501

        self._submission_overview_type = submission_overview_type

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
        if not isinstance(other, SubmissionOverviewInputAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SubmissionOverviewInputAllOf):
            return True

        return self.to_dict() != other.to_dict()
