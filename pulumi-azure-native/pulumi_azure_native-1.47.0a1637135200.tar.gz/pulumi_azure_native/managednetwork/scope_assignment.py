# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ScopeAssignmentArgs', 'ScopeAssignment']

@pulumi.input_type
class ScopeAssignmentArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 assigned_managed_network: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 scope_assignment_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ScopeAssignment resource.
        :param pulumi.Input[str] scope: The base resource of the scope assignment to create. The scope can be any REST resource instance. For example, use 'subscriptions/{subscription-id}' for a subscription, 'subscriptions/{subscription-id}/resourceGroups/{resource-group-name}' for a resource group, and 'subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name}' for a resource.
        :param pulumi.Input[str] assigned_managed_network: The managed network ID with scope will be assigned to.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] scope_assignment_name: The name of the scope assignment to create.
        """
        pulumi.set(__self__, "scope", scope)
        if assigned_managed_network is not None:
            pulumi.set(__self__, "assigned_managed_network", assigned_managed_network)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if scope_assignment_name is not None:
            pulumi.set(__self__, "scope_assignment_name", scope_assignment_name)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The base resource of the scope assignment to create. The scope can be any REST resource instance. For example, use 'subscriptions/{subscription-id}' for a subscription, 'subscriptions/{subscription-id}/resourceGroups/{resource-group-name}' for a resource group, and 'subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name}' for a resource.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="assignedManagedNetwork")
    def assigned_managed_network(self) -> Optional[pulumi.Input[str]]:
        """
        The managed network ID with scope will be assigned to.
        """
        return pulumi.get(self, "assigned_managed_network")

    @assigned_managed_network.setter
    def assigned_managed_network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "assigned_managed_network", value)

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
    @pulumi.getter(name="scopeAssignmentName")
    def scope_assignment_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the scope assignment to create.
        """
        return pulumi.get(self, "scope_assignment_name")

    @scope_assignment_name.setter
    def scope_assignment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scope_assignment_name", value)


class ScopeAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assigned_managed_network: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 scope_assignment_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Managed Network resource
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] assigned_managed_network: The managed network ID with scope will be assigned to.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] scope: The base resource of the scope assignment to create. The scope can be any REST resource instance. For example, use 'subscriptions/{subscription-id}' for a subscription, 'subscriptions/{subscription-id}/resourceGroups/{resource-group-name}' for a resource group, and 'subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name}' for a resource.
        :param pulumi.Input[str] scope_assignment_name: The name of the scope assignment to create.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScopeAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Managed Network resource
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param ScopeAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScopeAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assigned_managed_network: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 scope_assignment_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ScopeAssignmentArgs.__new__(ScopeAssignmentArgs)

            __props__.__dict__["assigned_managed_network"] = assigned_managed_network
            __props__.__dict__["location"] = location
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["scope_assignment_name"] = scope_assignment_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:managednetwork/v20190601preview:ScopeAssignment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ScopeAssignment, __self__).__init__(
            'azure-native:managednetwork:ScopeAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ScopeAssignment':
        """
        Get an existing ScopeAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ScopeAssignmentArgs.__new__(ScopeAssignmentArgs)

        __props__.__dict__["assigned_managed_network"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["type"] = None
        return ScopeAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assignedManagedNetwork")
    def assigned_managed_network(self) -> pulumi.Output[Optional[str]]:
        """
        The managed network ID with scope will be assigned to.
        """
        return pulumi.get(self, "assigned_managed_network")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the ManagedNetwork resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

