# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['ManagedNetworkPeeringPolicyArgs', 'ManagedNetworkPeeringPolicy']

@pulumi.input_type
class ManagedNetworkPeeringPolicyArgs:
    def __init__(__self__, *,
                 managed_network_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 managed_network_peering_policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['ManagedNetworkPeeringPolicyPropertiesArgs']] = None):
        """
        The set of arguments for constructing a ManagedNetworkPeeringPolicy resource.
        :param pulumi.Input[str] managed_network_name: The name of the Managed Network.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] managed_network_peering_policy_name: The name of the Managed Network Peering Policy.
        :param pulumi.Input['ManagedNetworkPeeringPolicyPropertiesArgs'] properties: Gets or sets the properties of a Managed Network Policy
        """
        pulumi.set(__self__, "managed_network_name", managed_network_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if managed_network_peering_policy_name is not None:
            pulumi.set(__self__, "managed_network_peering_policy_name", managed_network_peering_policy_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="managedNetworkName")
    def managed_network_name(self) -> pulumi.Input[str]:
        """
        The name of the Managed Network.
        """
        return pulumi.get(self, "managed_network_name")

    @managed_network_name.setter
    def managed_network_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "managed_network_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="managedNetworkPeeringPolicyName")
    def managed_network_peering_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Managed Network Peering Policy.
        """
        return pulumi.get(self, "managed_network_peering_policy_name")

    @managed_network_peering_policy_name.setter
    def managed_network_peering_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_network_peering_policy_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['ManagedNetworkPeeringPolicyPropertiesArgs']]:
        """
        Gets or sets the properties of a Managed Network Policy
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['ManagedNetworkPeeringPolicyPropertiesArgs']]):
        pulumi.set(self, "properties", value)


class ManagedNetworkPeeringPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_network_name: Optional[pulumi.Input[str]] = None,
                 managed_network_peering_policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ManagedNetworkPeeringPolicyPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Managed Network Peering Policy resource
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] managed_network_name: The name of the Managed Network.
        :param pulumi.Input[str] managed_network_peering_policy_name: The name of the Managed Network Peering Policy.
        :param pulumi.Input[pulumi.InputType['ManagedNetworkPeeringPolicyPropertiesArgs']] properties: Gets or sets the properties of a Managed Network Policy
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedNetworkPeeringPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Managed Network Peering Policy resource
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param ManagedNetworkPeeringPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedNetworkPeeringPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_network_name: Optional[pulumi.Input[str]] = None,
                 managed_network_peering_policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ManagedNetworkPeeringPolicyPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedNetworkPeeringPolicyArgs.__new__(ManagedNetworkPeeringPolicyArgs)

            __props__.__dict__["location"] = location
            if managed_network_name is None and not opts.urn:
                raise TypeError("Missing required property 'managed_network_name'")
            __props__.__dict__["managed_network_name"] = managed_network_name
            __props__.__dict__["managed_network_peering_policy_name"] = managed_network_peering_policy_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:managednetwork/v20190601preview:ManagedNetworkPeeringPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedNetworkPeeringPolicy, __self__).__init__(
            'azure-native:managednetwork:ManagedNetworkPeeringPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedNetworkPeeringPolicy':
        """
        Get an existing ManagedNetworkPeeringPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagedNetworkPeeringPolicyArgs.__new__(ManagedNetworkPeeringPolicyArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return ManagedNetworkPeeringPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ManagedNetworkPeeringPolicyPropertiesResponse']:
        """
        Gets or sets the properties of a Managed Network Policy
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

