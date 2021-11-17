# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetApiOperationPolicyResult',
    'AwaitableGetApiOperationPolicyResult',
    'get_api_operation_policy',
    'get_api_operation_policy_output',
]

@pulumi.output_type
class GetApiOperationPolicyResult:
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


class AwaitableGetApiOperationPolicyResult(GetApiOperationPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApiOperationPolicyResult(
            format=self.format,
            id=self.id,
            name=self.name,
            type=self.type,
            value=self.value)


def get_api_operation_policy(api_id: Optional[str] = None,
                             format: Optional[str] = None,
                             operation_id: Optional[str] = None,
                             policy_id: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             service_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApiOperationPolicyResult:
    """
    Policy Contract details.


    :param str api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
    :param str format: Policy Export Format.
    :param str operation_id: Operation identifier within an API. Must be unique in the current API Management service instance.
    :param str policy_id: The identifier of the Policy.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['apiId'] = api_id
    __args__['format'] = format
    __args__['operationId'] = operation_id
    __args__['policyId'] = policy_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20191201:getApiOperationPolicy', __args__, opts=opts, typ=GetApiOperationPolicyResult).value

    return AwaitableGetApiOperationPolicyResult(
        format=__ret__.format,
        id=__ret__.id,
        name=__ret__.name,
        type=__ret__.type,
        value=__ret__.value)


@_utilities.lift_output_func(get_api_operation_policy)
def get_api_operation_policy_output(api_id: Optional[pulumi.Input[str]] = None,
                                    format: Optional[pulumi.Input[Optional[str]]] = None,
                                    operation_id: Optional[pulumi.Input[str]] = None,
                                    policy_id: Optional[pulumi.Input[str]] = None,
                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                    service_name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApiOperationPolicyResult]:
    """
    Policy Contract details.


    :param str api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
    :param str format: Policy Export Format.
    :param str operation_id: Operation identifier within an API. Must be unique in the current API Management service instance.
    :param str policy_id: The identifier of the Policy.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    ...
