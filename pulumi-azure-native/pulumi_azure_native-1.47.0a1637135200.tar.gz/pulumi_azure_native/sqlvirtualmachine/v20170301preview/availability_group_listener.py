# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['AvailabilityGroupListenerArgs', 'AvailabilityGroupListener']

@pulumi.input_type
class AvailabilityGroupListenerArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sql_virtual_machine_group_name: pulumi.Input[str],
                 availability_group_listener_name: Optional[pulumi.Input[str]] = None,
                 availability_group_name: Optional[pulumi.Input[str]] = None,
                 create_default_availability_group_if_not_exist: Optional[pulumi.Input[bool]] = None,
                 load_balancer_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerConfigurationArgs']]]] = None,
                 port: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a AvailabilityGroupListener resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] sql_virtual_machine_group_name: Name of the SQL virtual machine group.
        :param pulumi.Input[str] availability_group_listener_name: Name of the availability group listener.
        :param pulumi.Input[str] availability_group_name: Name of the availability group.
        :param pulumi.Input[bool] create_default_availability_group_if_not_exist: Create a default availability group if it does not exist.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancerConfigurationArgs']]] load_balancer_configurations: List of load balancer configurations for an availability group listener.
        :param pulumi.Input[int] port: Listener port.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sql_virtual_machine_group_name", sql_virtual_machine_group_name)
        if availability_group_listener_name is not None:
            pulumi.set(__self__, "availability_group_listener_name", availability_group_listener_name)
        if availability_group_name is not None:
            pulumi.set(__self__, "availability_group_name", availability_group_name)
        if create_default_availability_group_if_not_exist is not None:
            pulumi.set(__self__, "create_default_availability_group_if_not_exist", create_default_availability_group_if_not_exist)
        if load_balancer_configurations is not None:
            pulumi.set(__self__, "load_balancer_configurations", load_balancer_configurations)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sqlVirtualMachineGroupName")
    def sql_virtual_machine_group_name(self) -> pulumi.Input[str]:
        """
        Name of the SQL virtual machine group.
        """
        return pulumi.get(self, "sql_virtual_machine_group_name")

    @sql_virtual_machine_group_name.setter
    def sql_virtual_machine_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "sql_virtual_machine_group_name", value)

    @property
    @pulumi.getter(name="availabilityGroupListenerName")
    def availability_group_listener_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the availability group listener.
        """
        return pulumi.get(self, "availability_group_listener_name")

    @availability_group_listener_name.setter
    def availability_group_listener_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_group_listener_name", value)

    @property
    @pulumi.getter(name="availabilityGroupName")
    def availability_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the availability group.
        """
        return pulumi.get(self, "availability_group_name")

    @availability_group_name.setter
    def availability_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_group_name", value)

    @property
    @pulumi.getter(name="createDefaultAvailabilityGroupIfNotExist")
    def create_default_availability_group_if_not_exist(self) -> Optional[pulumi.Input[bool]]:
        """
        Create a default availability group if it does not exist.
        """
        return pulumi.get(self, "create_default_availability_group_if_not_exist")

    @create_default_availability_group_if_not_exist.setter
    def create_default_availability_group_if_not_exist(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "create_default_availability_group_if_not_exist", value)

    @property
    @pulumi.getter(name="loadBalancerConfigurations")
    def load_balancer_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerConfigurationArgs']]]]:
        """
        List of load balancer configurations for an availability group listener.
        """
        return pulumi.get(self, "load_balancer_configurations")

    @load_balancer_configurations.setter
    def load_balancer_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancerConfigurationArgs']]]]):
        pulumi.set(self, "load_balancer_configurations", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        Listener port.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


class AvailabilityGroupListener(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_group_listener_name: Optional[pulumi.Input[str]] = None,
                 availability_group_name: Optional[pulumi.Input[str]] = None,
                 create_default_availability_group_if_not_exist: Optional[pulumi.Input[bool]] = None,
                 load_balancer_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerConfigurationArgs']]]]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_virtual_machine_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A SQL Server availability group listener.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_group_listener_name: Name of the availability group listener.
        :param pulumi.Input[str] availability_group_name: Name of the availability group.
        :param pulumi.Input[bool] create_default_availability_group_if_not_exist: Create a default availability group if it does not exist.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerConfigurationArgs']]]] load_balancer_configurations: List of load balancer configurations for an availability group listener.
        :param pulumi.Input[int] port: Listener port.
        :param pulumi.Input[str] resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] sql_virtual_machine_group_name: Name of the SQL virtual machine group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AvailabilityGroupListenerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A SQL Server availability group listener.

        :param str resource_name: The name of the resource.
        :param AvailabilityGroupListenerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AvailabilityGroupListenerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_group_listener_name: Optional[pulumi.Input[str]] = None,
                 availability_group_name: Optional[pulumi.Input[str]] = None,
                 create_default_availability_group_if_not_exist: Optional[pulumi.Input[bool]] = None,
                 load_balancer_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancerConfigurationArgs']]]]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_virtual_machine_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = AvailabilityGroupListenerArgs.__new__(AvailabilityGroupListenerArgs)

            __props__.__dict__["availability_group_listener_name"] = availability_group_listener_name
            __props__.__dict__["availability_group_name"] = availability_group_name
            __props__.__dict__["create_default_availability_group_if_not_exist"] = create_default_availability_group_if_not_exist
            __props__.__dict__["load_balancer_configurations"] = load_balancer_configurations
            __props__.__dict__["port"] = port
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sql_virtual_machine_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'sql_virtual_machine_group_name'")
            __props__.__dict__["sql_virtual_machine_group_name"] = sql_virtual_machine_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sqlvirtualmachine:AvailabilityGroupListener")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AvailabilityGroupListener, __self__).__init__(
            'azure-native:sqlvirtualmachine/v20170301preview:AvailabilityGroupListener',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AvailabilityGroupListener':
        """
        Get an existing AvailabilityGroupListener resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AvailabilityGroupListenerArgs.__new__(AvailabilityGroupListenerArgs)

        __props__.__dict__["availability_group_name"] = None
        __props__.__dict__["create_default_availability_group_if_not_exist"] = None
        __props__.__dict__["load_balancer_configurations"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["type"] = None
        return AvailabilityGroupListener(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilityGroupName")
    def availability_group_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the availability group.
        """
        return pulumi.get(self, "availability_group_name")

    @property
    @pulumi.getter(name="createDefaultAvailabilityGroupIfNotExist")
    def create_default_availability_group_if_not_exist(self) -> pulumi.Output[Optional[bool]]:
        """
        Create a default availability group if it does not exist.
        """
        return pulumi.get(self, "create_default_availability_group_if_not_exist")

    @property
    @pulumi.getter(name="loadBalancerConfigurations")
    def load_balancer_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.LoadBalancerConfigurationResponse']]]:
        """
        List of load balancer configurations for an availability group listener.
        """
        return pulumi.get(self, "load_balancer_configurations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        Listener port.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state to track the async operation status.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

