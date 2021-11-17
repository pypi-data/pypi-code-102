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
    'GetRestorePointCollectionResult',
    'AwaitableGetRestorePointCollectionResult',
    'get_restore_point_collection',
    'get_restore_point_collection_output',
]

@pulumi.output_type
class GetRestorePointCollectionResult:
    """
    Create or update Restore Point collection parameters.
    """
    def __init__(__self__, id=None, location=None, name=None, provisioning_state=None, restore_point_collection_id=None, restore_points=None, source=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if restore_point_collection_id and not isinstance(restore_point_collection_id, str):
            raise TypeError("Expected argument 'restore_point_collection_id' to be a str")
        pulumi.set(__self__, "restore_point_collection_id", restore_point_collection_id)
        if restore_points and not isinstance(restore_points, list):
            raise TypeError("Expected argument 'restore_points' to be a list")
        pulumi.set(__self__, "restore_points", restore_points)
        if source and not isinstance(source, dict):
            raise TypeError("Expected argument 'source' to be a dict")
        pulumi.set(__self__, "source", source)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the restore point collection.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="restorePointCollectionId")
    def restore_point_collection_id(self) -> str:
        """
        The unique id of the restore point collection.
        """
        return pulumi.get(self, "restore_point_collection_id")

    @property
    @pulumi.getter(name="restorePoints")
    def restore_points(self) -> Sequence['outputs.RestorePointResponse']:
        """
        A list containing all restore points created under this restore point collection.
        """
        return pulumi.get(self, "restore_points")

    @property
    @pulumi.getter
    def source(self) -> Optional['outputs.RestorePointCollectionSourcePropertiesResponse']:
        """
        The properties of the source resource that this restore point collection is created from.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetRestorePointCollectionResult(GetRestorePointCollectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRestorePointCollectionResult(
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            restore_point_collection_id=self.restore_point_collection_id,
            restore_points=self.restore_points,
            source=self.source,
            tags=self.tags,
            type=self.type)


def get_restore_point_collection(expand: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 restore_point_collection_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRestorePointCollectionResult:
    """
    Create or update Restore Point collection parameters.


    :param str expand: The expand expression to apply on the operation. If expand=restorePoints, server will return all contained restore points in the restorePointCollection.
    :param str resource_group_name: The name of the resource group.
    :param str restore_point_collection_name: The name of the restore point collection.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['restorePointCollectionName'] = restore_point_collection_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20210701:getRestorePointCollection', __args__, opts=opts, typ=GetRestorePointCollectionResult).value

    return AwaitableGetRestorePointCollectionResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        restore_point_collection_id=__ret__.restore_point_collection_id,
        restore_points=__ret__.restore_points,
        source=__ret__.source,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_restore_point_collection)
def get_restore_point_collection_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                        restore_point_collection_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRestorePointCollectionResult]:
    """
    Create or update Restore Point collection parameters.


    :param str expand: The expand expression to apply on the operation. If expand=restorePoints, server will return all contained restore points in the restorePointCollection.
    :param str resource_group_name: The name of the resource group.
    :param str restore_point_collection_name: The name of the restore point collection.
    """
    ...
