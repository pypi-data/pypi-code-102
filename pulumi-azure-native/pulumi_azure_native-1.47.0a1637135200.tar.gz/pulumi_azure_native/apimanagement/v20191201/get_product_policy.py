# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetProductPolicyResult',
    'AwaitableGetProductPolicyResult',
    'get_product_policy',
    'get_product_policy_output',
]

@pulumi.output_type
class GetProductPolicyResult:
    """
    Policy Contract details.
    """
    def __init__(__self__, format=None, id=None, name=None, type=None, value=None):
        if format and not isinstance(format, str):
            raise TypeError("Expected argument 'format' to be a str")
        pulumi.set(__self__, "format", format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def format(self) -> Optional[str]:
        """
        Format of the policyContent.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Contents of the Policy as defined by the format.
        """
        return pulumi.get(self, "value")


class AwaitableGetProductPolicyResult(GetProductPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProductPolicyResult(
            format=self.format,
            id=self.id,
            name=self.name,
            type=self.type,
            value=self.value)


def get_product_policy(format: Optional[str] = None,
                       policy_id: Optional[str] = None,
                       product_id: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       service_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProductPolicyResult:
    """
    Policy Contract details.


    :param str format: Policy Export Format.
    :param str policy_id: The identifier of the Policy.
    :param str product_id: Product identifier. Must be unique in the current API Management service instance.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['format'] = format
    __args__['policyId'] = policy_id
    __args__['productId'] = product_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20191201:getProductPolicy', __args__, opts=opts, typ=GetProductPolicyResult).value

    return AwaitableGetProductPolicyResult(
        format=__ret__.format,
        id=__ret__.id,
        name=__ret__.name,
        type=__ret__.type,
        value=__ret__.value)


@_utilities.lift_output_func(get_product_policy)
def get_product_policy_output(format: Optional[pulumi.Input[Optional[str]]] = None,
                              policy_id: Optional[pulumi.Input[str]] = None,
                              product_id: Optional[pulumi.Input[str]] = None,
                              resource_group_name: Optional[pulumi.Input[str]] = None,
                              service_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProductPolicyResult]:
    """
    Policy Contract details.


    :param str format: Policy Export Format.
    :param str policy_id: The identifier of the Policy.
    :param str product_id: Product identifier. Must be unique in the current API Management service instance.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    ...
