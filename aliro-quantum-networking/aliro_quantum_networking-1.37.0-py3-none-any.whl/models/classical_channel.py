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


class ClassicalChannel(object):
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
        'delay': 'float',
        'distance': 'float',
        'node_from': 'str',
        'node_to': 'str'
    }

    attribute_map = {
        'delay': 'delay',
        'distance': 'distance',
        'node_from': 'nodeFrom',
        'node_to': 'nodeTo'
    }

    def __init__(self, delay=0, distance=1000, node_from=None, node_to=None, local_vars_configuration=None):  # noqa: E501
        """ClassicalChannel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._delay = None
        self._distance = None
        self._node_from = None
        self._node_to = None
        self.discriminator = None

        if delay is not None:
            self.delay = delay
        if distance is not None:
            self.distance = distance
        self.node_from = node_from
        self.node_to = node_to

    @property
    def delay(self):
        """Gets the delay of this ClassicalChannel.  # noqa: E501

        The delay in addition to the travel time in ps (default 500 * 10^6 ps)  # noqa: E501

        :return: The delay of this ClassicalChannel.  # noqa: E501
        :rtype: float
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
        """Sets the delay of this ClassicalChannel.

        The delay in addition to the travel time in ps (default 500 * 10^6 ps)  # noqa: E501

        :param delay: The delay of this ClassicalChannel.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                delay is not None and delay < 0):  # noqa: E501
            raise ValueError("Invalid value for `delay`, must be a value greater than or equal to `0`")  # noqa: E501

        self._delay = delay

    @property
    def distance(self):
        """Gets the distance of this ClassicalChannel.  # noqa: E501

        The distance in meters (default 1000 m)  # noqa: E501

        :return: The distance of this ClassicalChannel.  # noqa: E501
        :rtype: float
        """
        return self._distance

    @distance.setter
    def distance(self, distance):
        """Sets the distance of this ClassicalChannel.

        The distance in meters (default 1000 m)  # noqa: E501

        :param distance: The distance of this ClassicalChannel.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                distance is not None and distance < 0):  # noqa: E501
            raise ValueError("Invalid value for `distance`, must be a value greater than or equal to `0`")  # noqa: E501

        self._distance = distance

    @property
    def node_from(self):
        """Gets the node_from of this ClassicalChannel.  # noqa: E501


        :return: The node_from of this ClassicalChannel.  # noqa: E501
        :rtype: str
        """
        return self._node_from

    @node_from.setter
    def node_from(self, node_from):
        """Sets the node_from of this ClassicalChannel.


        :param node_from: The node_from of this ClassicalChannel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and node_from is None:  # noqa: E501
            raise ValueError("Invalid value for `node_from`, must not be `None`")  # noqa: E501

        self._node_from = node_from

    @property
    def node_to(self):
        """Gets the node_to of this ClassicalChannel.  # noqa: E501


        :return: The node_to of this ClassicalChannel.  # noqa: E501
        :rtype: str
        """
        return self._node_to

    @node_to.setter
    def node_to(self, node_to):
        """Sets the node_to of this ClassicalChannel.


        :param node_to: The node_to of this ClassicalChannel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and node_to is None:  # noqa: E501
            raise ValueError("Invalid value for `node_to`, must not be `None`")  # noqa: E501

        self._node_to = node_to

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
        if not isinstance(other, ClassicalChannel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClassicalChannel):
            return True

        return self.to_dict() != other.to_dict()
