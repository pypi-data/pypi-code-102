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
    'GetConnectionTypeResult',
    'AwaitableGetConnectionTypeResult',
    'get_connection_type',
    'get_connection_type_output',
]

@pulumi.output_type
class GetConnectionTypeResult:
    """
    Definition of the connection type.
    """
    def __init__(__self__, creation_time=None, description=None, field_definitions=None, id=None, is_global=None, last_modified_time=None, name=None, type=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if field_definitions and not isinstance(field_definitions, dict):
            raise TypeError("Expected argument 'field_definitions' to be a dict")
        pulumi.set(__self__, "field_definitions", field_definitions)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_global and not isinstance(is_global, bool):
            raise TypeError("Expected argument 'is_global' to be a bool")
        pulumi.set(__self__, "is_global", is_global)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Gets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fieldDefinitions")
    def field_definitions(self) -> Mapping[str, 'outputs.FieldDefinitionResponse']:
        """
        Gets the field definitions of the connection type.
        """
        return pulumi.get(self, "field_definitions")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Gets the id of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isGlobal")
    def is_global(self) -> Optional[bool]:
        """
        Gets or sets a Boolean value to indicate if the connection type is global.
        """
        return pulumi.get(self, "is_global")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[str]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Gets the name of the connection type.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetConnectionTypeResult(GetConnectionTypeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectionTypeResult(
            creation_time=self.creation_time,
            description=self.description,
            field_definitions=self.field_definitions,
            id=self.id,
            is_global=self.is_global,
            last_modified_time=self.last_modified_time,
            name=self.name,
            type=self.type)


def get_connection_type(automation_account_name: Optional[str] = None,
                        connection_type_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectionTypeResult:
    """
    Definition of the connection type.


    :param str automation_account_name: The name of the automation account.
    :param str connection_type_name: The name of connection type.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['automationAccountName'] = automation_account_name
    __args__['connectionTypeName'] = connection_type_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:automation/v20190601:getConnectionType', __args__, opts=opts, typ=GetConnectionTypeResult).value

    return AwaitableGetConnectionTypeResult(
        creation_time=__ret__.creation_time,
        description=__ret__.description,
        field_definitions=__ret__.field_definitions,
        id=__ret__.id,
        is_global=__ret__.is_global,
        last_modified_time=__ret__.last_modified_time,
        name=__ret__.name,
        type=__ret__.type)


@_utilities.lift_output_func(get_connection_type)
def get_connection_type_output(automation_account_name: Optional[pulumi.Input[str]] = None,
                               connection_type_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConnectionTypeResult]:
    """
    Definition of the connection type.


    :param str automation_account_name: The name of the automation account.
    :param str connection_type_name: The name of connection type.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    ...
