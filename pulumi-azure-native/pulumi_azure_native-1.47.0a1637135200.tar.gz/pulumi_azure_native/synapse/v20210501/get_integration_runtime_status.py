# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetIntegrationRuntimeStatusResult',
    'AwaitableGetIntegrationRuntimeStatusResult',
    'get_integration_runtime_status',
    'get_integration_runtime_status_output',
]

@pulumi.output_type
class GetIntegrationRuntimeStatusResult:
    """
    Integration runtime status response.
    """
    def __init__(__self__, name=None, properties=None):
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The integration runtime name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> Any:
        """
        Integration runtime properties.
        """
        return pulumi.get(self, "properties")


class AwaitableGetIntegrationRuntimeStatusResult(GetIntegrationRuntimeStatusResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIntegrationRuntimeStatusResult(
            name=self.name,
            properties=self.properties)


def get_integration_runtime_status(integration_runtime_name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   workspace_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIntegrationRuntimeStatusResult:
    """
    Integration runtime status response.


    :param str integration_runtime_name: Integration runtime name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['integrationRuntimeName'] = integration_runtime_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:synapse/v20210501:getIntegrationRuntimeStatus', __args__, opts=opts, typ=GetIntegrationRuntimeStatusResult).value

    return AwaitableGetIntegrationRuntimeStatusResult(
        name=__ret__.name,
        properties=__ret__.properties)


@_utilities.lift_output_func(get_integration_runtime_status)
def get_integration_runtime_status_output(integration_runtime_name: Optional[pulumi.Input[str]] = None,
                                          resource_group_name: Optional[pulumi.Input[str]] = None,
                                          workspace_name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIntegrationRuntimeStatusResult]:
    """
    Integration runtime status response.


    :param str integration_runtime_name: Integration runtime name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
