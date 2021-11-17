# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListClusterUpgradableVersionsResult',
    'AwaitableListClusterUpgradableVersionsResult',
    'list_cluster_upgradable_versions',
    'list_cluster_upgradable_versions_output',
]

@pulumi.output_type
class ListClusterUpgradableVersionsResult:
    """
    The list of intermediate cluster code versions for an upgrade or downgrade. Or minimum and maximum upgradable version if no target was given
    """
    def __init__(__self__, supported_path=None):
        if supported_path and not isinstance(supported_path, list):
            raise TypeError("Expected argument 'supported_path' to be a list")
        pulumi.set(__self__, "supported_path", supported_path)

    @property
    @pulumi.getter(name="supportedPath")
    def supported_path(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "supported_path")


class AwaitableListClusterUpgradableVersionsResult(ListClusterUpgradableVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListClusterUpgradableVersionsResult(
            supported_path=self.supported_path)


def list_cluster_upgradable_versions(cluster_name: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     target_version: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListClusterUpgradableVersionsResult:
    """
    The list of intermediate cluster code versions for an upgrade or downgrade. Or minimum and maximum upgradable version if no target was given


    :param str cluster_name: The name of the cluster resource.
    :param str resource_group_name: The name of the resource group.
    :param str target_version: The target code version.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['targetVersion'] = target_version
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:servicefabric/v20210601:listClusterUpgradableVersions', __args__, opts=opts, typ=ListClusterUpgradableVersionsResult).value

    return AwaitableListClusterUpgradableVersionsResult(
        supported_path=__ret__.supported_path)


@_utilities.lift_output_func(list_cluster_upgradable_versions)
def list_cluster_upgradable_versions_output(cluster_name: Optional[pulumi.Input[str]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            target_version: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListClusterUpgradableVersionsResult]:
    """
    The list of intermediate cluster code versions for an upgrade or downgrade. Or minimum and maximum upgradable version if no target was given


    :param str cluster_name: The name of the cluster resource.
    :param str resource_group_name: The name of the resource group.
    :param str target_version: The target code version.
    """
    ...
