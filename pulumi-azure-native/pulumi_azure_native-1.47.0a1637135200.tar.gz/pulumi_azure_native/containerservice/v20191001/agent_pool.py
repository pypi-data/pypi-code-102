# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['AgentPoolArgs', 'AgentPool']

@pulumi.input_type
class AgentPoolArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 agent_pool_name: Optional[pulumi.Input[str]] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 count: Optional[pulumi.Input[int]] = None,
                 enable_auto_scaling: Optional[pulumi.Input[bool]] = None,
                 enable_node_public_ip: Optional[pulumi.Input[bool]] = None,
                 max_count: Optional[pulumi.Input[int]] = None,
                 max_pods: Optional[pulumi.Input[int]] = None,
                 min_count: Optional[pulumi.Input[int]] = None,
                 node_taints: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 orchestrator_version: Optional[pulumi.Input[str]] = None,
                 os_disk_size_gb: Optional[pulumi.Input[int]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OSType']]] = None,
                 scale_set_eviction_policy: Optional[pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']]] = None,
                 scale_set_priority: Optional[pulumi.Input[Union[str, 'ScaleSetPriority']]] = None,
                 type: Optional[pulumi.Input[Union[str, 'AgentPoolType']]] = None,
                 vm_size: Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]] = None,
                 vnet_subnet_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AgentPool resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_name: The name of the managed cluster resource.
        :param pulumi.Input[str] agent_pool_name: The name of the agent pool.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] availability_zones: (PREVIEW) Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        :param pulumi.Input[int] count: Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1.
        :param pulumi.Input[bool] enable_auto_scaling: Whether to enable auto-scaler
        :param pulumi.Input[bool] enable_node_public_ip: Enable public IP for nodes
        :param pulumi.Input[int] max_count: Maximum number of nodes for auto-scaling
        :param pulumi.Input[int] max_pods: Maximum number of pods that can run on a node.
        :param pulumi.Input[int] min_count: Minimum number of nodes for auto-scaling
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_taints: Taints added to new nodes during node pool create and scale. For example, key=value:NoSchedule.
        :param pulumi.Input[str] orchestrator_version: Version of orchestrator specified when creating the managed cluster.
        :param pulumi.Input[int] os_disk_size_gb: OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        :param pulumi.Input[Union[str, 'OSType']] os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']] scale_set_eviction_policy: ScaleSetEvictionPolicy to be used to specify eviction policy for low priority virtual machine scale set. Default to Delete.
        :param pulumi.Input[Union[str, 'ScaleSetPriority']] scale_set_priority: ScaleSetPriority to be used to specify virtual machine scale set priority. Default to regular.
        :param pulumi.Input[Union[str, 'AgentPoolType']] type: AgentPoolType represents types of an agent pool
        :param pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']] vm_size: Size of agent VMs.
        :param pulumi.Input[str] vnet_subnet_id: VNet SubnetID specifies the VNet's subnet identifier.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if agent_pool_name is not None:
            pulumi.set(__self__, "agent_pool_name", agent_pool_name)
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if count is not None:
            pulumi.set(__self__, "count", count)
        if enable_auto_scaling is not None:
            pulumi.set(__self__, "enable_auto_scaling", enable_auto_scaling)
        if enable_node_public_ip is not None:
            pulumi.set(__self__, "enable_node_public_ip", enable_node_public_ip)
        if max_count is not None:
            pulumi.set(__self__, "max_count", max_count)
        if max_pods is not None:
            pulumi.set(__self__, "max_pods", max_pods)
        if min_count is not None:
            pulumi.set(__self__, "min_count", min_count)
        if node_taints is not None:
            pulumi.set(__self__, "node_taints", node_taints)
        if orchestrator_version is not None:
            pulumi.set(__self__, "orchestrator_version", orchestrator_version)
        if os_disk_size_gb is not None:
            pulumi.set(__self__, "os_disk_size_gb", os_disk_size_gb)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if scale_set_eviction_policy is not None:
            pulumi.set(__self__, "scale_set_eviction_policy", scale_set_eviction_policy)
        if scale_set_priority is not None:
            pulumi.set(__self__, "scale_set_priority", scale_set_priority)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if vm_size is not None:
            pulumi.set(__self__, "vm_size", vm_size)
        if vnet_subnet_id is not None:
            pulumi.set(__self__, "vnet_subnet_id", vnet_subnet_id)

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
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the managed cluster resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="agentPoolName")
    def agent_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the agent pool.
        """
        return pulumi.get(self, "agent_pool_name")

    @agent_pool_name.setter
    def agent_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_pool_name", value)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        (PREVIEW) Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        """
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1.
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter(name="enableAutoScaling")
    def enable_auto_scaling(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable auto-scaler
        """
        return pulumi.get(self, "enable_auto_scaling")

    @enable_auto_scaling.setter
    def enable_auto_scaling(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_auto_scaling", value)

    @property
    @pulumi.getter(name="enableNodePublicIP")
    def enable_node_public_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable public IP for nodes
        """
        return pulumi.get(self, "enable_node_public_ip")

    @enable_node_public_ip.setter
    def enable_node_public_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_node_public_ip", value)

    @property
    @pulumi.getter(name="maxCount")
    def max_count(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum number of nodes for auto-scaling
        """
        return pulumi.get(self, "max_count")

    @max_count.setter
    def max_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_count", value)

    @property
    @pulumi.getter(name="maxPods")
    def max_pods(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum number of pods that can run on a node.
        """
        return pulumi.get(self, "max_pods")

    @max_pods.setter
    def max_pods(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_pods", value)

    @property
    @pulumi.getter(name="minCount")
    def min_count(self) -> Optional[pulumi.Input[int]]:
        """
        Minimum number of nodes for auto-scaling
        """
        return pulumi.get(self, "min_count")

    @min_count.setter
    def min_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_count", value)

    @property
    @pulumi.getter(name="nodeTaints")
    def node_taints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Taints added to new nodes during node pool create and scale. For example, key=value:NoSchedule.
        """
        return pulumi.get(self, "node_taints")

    @node_taints.setter
    def node_taints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "node_taints", value)

    @property
    @pulumi.getter(name="orchestratorVersion")
    def orchestrator_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of orchestrator specified when creating the managed cluster.
        """
        return pulumi.get(self, "orchestrator_version")

    @orchestrator_version.setter
    def orchestrator_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "orchestrator_version", value)

    @property
    @pulumi.getter(name="osDiskSizeGB")
    def os_disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        """
        return pulumi.get(self, "os_disk_size_gb")

    @os_disk_size_gb.setter
    def os_disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "os_disk_size_gb", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[Union[str, 'OSType']]]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[Union[str, 'OSType']]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="scaleSetEvictionPolicy")
    def scale_set_eviction_policy(self) -> Optional[pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']]]:
        """
        ScaleSetEvictionPolicy to be used to specify eviction policy for low priority virtual machine scale set. Default to Delete.
        """
        return pulumi.get(self, "scale_set_eviction_policy")

    @scale_set_eviction_policy.setter
    def scale_set_eviction_policy(self, value: Optional[pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']]]):
        pulumi.set(self, "scale_set_eviction_policy", value)

    @property
    @pulumi.getter(name="scaleSetPriority")
    def scale_set_priority(self) -> Optional[pulumi.Input[Union[str, 'ScaleSetPriority']]]:
        """
        ScaleSetPriority to be used to specify virtual machine scale set priority. Default to regular.
        """
        return pulumi.get(self, "scale_set_priority")

    @scale_set_priority.setter
    def scale_set_priority(self, value: Optional[pulumi.Input[Union[str, 'ScaleSetPriority']]]):
        pulumi.set(self, "scale_set_priority", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'AgentPoolType']]]:
        """
        AgentPoolType represents types of an agent pool
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'AgentPoolType']]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]]):
        pulumi.set(self, "vm_size", value)

    @property
    @pulumi.getter(name="vnetSubnetID")
    def vnet_subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        VNet SubnetID specifies the VNet's subnet identifier.
        """
        return pulumi.get(self, "vnet_subnet_id")

    @vnet_subnet_id.setter
    def vnet_subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vnet_subnet_id", value)


class AgentPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_pool_name: Optional[pulumi.Input[str]] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 count: Optional[pulumi.Input[int]] = None,
                 enable_auto_scaling: Optional[pulumi.Input[bool]] = None,
                 enable_node_public_ip: Optional[pulumi.Input[bool]] = None,
                 max_count: Optional[pulumi.Input[int]] = None,
                 max_pods: Optional[pulumi.Input[int]] = None,
                 min_count: Optional[pulumi.Input[int]] = None,
                 node_taints: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 orchestrator_version: Optional[pulumi.Input[str]] = None,
                 os_disk_size_gb: Optional[pulumi.Input[int]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OSType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 scale_set_eviction_policy: Optional[pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']]] = None,
                 scale_set_priority: Optional[pulumi.Input[Union[str, 'ScaleSetPriority']]] = None,
                 type: Optional[pulumi.Input[Union[str, 'AgentPoolType']]] = None,
                 vm_size: Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]] = None,
                 vnet_subnet_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Agent Pool.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_pool_name: The name of the agent pool.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] availability_zones: (PREVIEW) Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        :param pulumi.Input[int] count: Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1.
        :param pulumi.Input[bool] enable_auto_scaling: Whether to enable auto-scaler
        :param pulumi.Input[bool] enable_node_public_ip: Enable public IP for nodes
        :param pulumi.Input[int] max_count: Maximum number of nodes for auto-scaling
        :param pulumi.Input[int] max_pods: Maximum number of pods that can run on a node.
        :param pulumi.Input[int] min_count: Minimum number of nodes for auto-scaling
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_taints: Taints added to new nodes during node pool create and scale. For example, key=value:NoSchedule.
        :param pulumi.Input[str] orchestrator_version: Version of orchestrator specified when creating the managed cluster.
        :param pulumi.Input[int] os_disk_size_gb: OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        :param pulumi.Input[Union[str, 'OSType']] os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_name_: The name of the managed cluster resource.
        :param pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']] scale_set_eviction_policy: ScaleSetEvictionPolicy to be used to specify eviction policy for low priority virtual machine scale set. Default to Delete.
        :param pulumi.Input[Union[str, 'ScaleSetPriority']] scale_set_priority: ScaleSetPriority to be used to specify virtual machine scale set priority. Default to regular.
        :param pulumi.Input[Union[str, 'AgentPoolType']] type: AgentPoolType represents types of an agent pool
        :param pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']] vm_size: Size of agent VMs.
        :param pulumi.Input[str] vnet_subnet_id: VNet SubnetID specifies the VNet's subnet identifier.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AgentPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Agent Pool.

        :param str resource_name: The name of the resource.
        :param AgentPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AgentPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_pool_name: Optional[pulumi.Input[str]] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 count: Optional[pulumi.Input[int]] = None,
                 enable_auto_scaling: Optional[pulumi.Input[bool]] = None,
                 enable_node_public_ip: Optional[pulumi.Input[bool]] = None,
                 max_count: Optional[pulumi.Input[int]] = None,
                 max_pods: Optional[pulumi.Input[int]] = None,
                 min_count: Optional[pulumi.Input[int]] = None,
                 node_taints: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 orchestrator_version: Optional[pulumi.Input[str]] = None,
                 os_disk_size_gb: Optional[pulumi.Input[int]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OSType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 scale_set_eviction_policy: Optional[pulumi.Input[Union[str, 'ScaleSetEvictionPolicy']]] = None,
                 scale_set_priority: Optional[pulumi.Input[Union[str, 'ScaleSetPriority']]] = None,
                 type: Optional[pulumi.Input[Union[str, 'AgentPoolType']]] = None,
                 vm_size: Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]] = None,
                 vnet_subnet_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = AgentPoolArgs.__new__(AgentPoolArgs)

            __props__.__dict__["agent_pool_name"] = agent_pool_name
            __props__.__dict__["availability_zones"] = availability_zones
            __props__.__dict__["count"] = count
            __props__.__dict__["enable_auto_scaling"] = enable_auto_scaling
            __props__.__dict__["enable_node_public_ip"] = enable_node_public_ip
            __props__.__dict__["max_count"] = max_count
            __props__.__dict__["max_pods"] = max_pods
            __props__.__dict__["min_count"] = min_count
            __props__.__dict__["node_taints"] = node_taints
            __props__.__dict__["orchestrator_version"] = orchestrator_version
            __props__.__dict__["os_disk_size_gb"] = os_disk_size_gb
            __props__.__dict__["os_type"] = os_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["scale_set_eviction_policy"] = scale_set_eviction_policy
            __props__.__dict__["scale_set_priority"] = scale_set_priority
            __props__.__dict__["type"] = type
            __props__.__dict__["vm_size"] = vm_size
            __props__.__dict__["vnet_subnet_id"] = vnet_subnet_id
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerservice:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20190201:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20190401:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20190601:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20190801:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20191101:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200101:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200201:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200301:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200401:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200601:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200701:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20200901:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20201101:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20201201:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20210201:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20210301:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20210501:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20210701:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20210801:AgentPool"), pulumi.Alias(type_="azure-native:containerservice/v20210901:AgentPool")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AgentPool, __self__).__init__(
            'azure-native:containerservice/v20191001:AgentPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AgentPool':
        """
        Get an existing AgentPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AgentPoolArgs.__new__(AgentPoolArgs)

        __props__.__dict__["availability_zones"] = None
        __props__.__dict__["count"] = None
        __props__.__dict__["enable_auto_scaling"] = None
        __props__.__dict__["enable_node_public_ip"] = None
        __props__.__dict__["max_count"] = None
        __props__.__dict__["max_pods"] = None
        __props__.__dict__["min_count"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["node_taints"] = None
        __props__.__dict__["orchestrator_version"] = None
        __props__.__dict__["os_disk_size_gb"] = None
        __props__.__dict__["os_type"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["scale_set_eviction_policy"] = None
        __props__.__dict__["scale_set_priority"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vm_size"] = None
        __props__.__dict__["vnet_subnet_id"] = None
        return AgentPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        (PREVIEW) Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        """
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter
    def count(self) -> pulumi.Output[Optional[int]]:
        """
        Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="enableAutoScaling")
    def enable_auto_scaling(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable auto-scaler
        """
        return pulumi.get(self, "enable_auto_scaling")

    @property
    @pulumi.getter(name="enableNodePublicIP")
    def enable_node_public_ip(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable public IP for nodes
        """
        return pulumi.get(self, "enable_node_public_ip")

    @property
    @pulumi.getter(name="maxCount")
    def max_count(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum number of nodes for auto-scaling
        """
        return pulumi.get(self, "max_count")

    @property
    @pulumi.getter(name="maxPods")
    def max_pods(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum number of pods that can run on a node.
        """
        return pulumi.get(self, "max_pods")

    @property
    @pulumi.getter(name="minCount")
    def min_count(self) -> pulumi.Output[Optional[int]]:
        """
        Minimum number of nodes for auto-scaling
        """
        return pulumi.get(self, "min_count")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nodeTaints")
    def node_taints(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Taints added to new nodes during node pool create and scale. For example, key=value:NoSchedule.
        """
        return pulumi.get(self, "node_taints")

    @property
    @pulumi.getter(name="orchestratorVersion")
    def orchestrator_version(self) -> pulumi.Output[Optional[str]]:
        """
        Version of orchestrator specified when creating the managed cluster.
        """
        return pulumi.get(self, "orchestrator_version")

    @property
    @pulumi.getter(name="osDiskSizeGB")
    def os_disk_size_gb(self) -> pulumi.Output[Optional[int]]:
        """
        OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        """
        return pulumi.get(self, "os_disk_size_gb")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[Optional[str]]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="scaleSetEvictionPolicy")
    def scale_set_eviction_policy(self) -> pulumi.Output[Optional[str]]:
        """
        ScaleSetEvictionPolicy to be used to specify eviction policy for low priority virtual machine scale set. Default to Delete.
        """
        return pulumi.get(self, "scale_set_eviction_policy")

    @property
    @pulumi.getter(name="scaleSetPriority")
    def scale_set_priority(self) -> pulumi.Output[Optional[str]]:
        """
        ScaleSetPriority to be used to specify virtual machine scale set priority. Default to regular.
        """
        return pulumi.get(self, "scale_set_priority")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        AgentPoolType represents types of an agent pool
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> pulumi.Output[Optional[str]]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, "vm_size")

    @property
    @pulumi.getter(name="vnetSubnetID")
    def vnet_subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        VNet SubnetID specifies the VNet's subnet identifier.
        """
        return pulumi.get(self, "vnet_subnet_id")

