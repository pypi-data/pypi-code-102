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

__all__ = ['JobAgentArgs', 'JobAgent']

@pulumi.input_type
class JobAgentArgs:
    def __init__(__self__, *,
                 database_id: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a JobAgent resource.
        :param pulumi.Input[str] database_id: Resource ID of the database to store job metadata in.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] job_agent_name: The name of the job agent to be created or updated.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input['SkuArgs'] sku: The name and tier of the SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "database_id", database_id)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if job_agent_name is not None:
            pulumi.set(__self__, "job_agent_name", job_agent_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> pulumi.Input[str]:
        """
        Resource ID of the database to store job metadata in.
        """
        return pulumi.get(self, "database_id")

    @database_id.setter
    def database_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_id", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter(name="jobAgentName")
    def job_agent_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the job agent to be created or updated.
        """
        return pulumi.get(self, "job_agent_name")

    @job_agent_name.setter
    def job_agent_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_agent_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The name and tier of the SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class JobAgent(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_id: Optional[pulumi.Input[str]] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        An Azure SQL job agent.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_id: Resource ID of the database to store job metadata in.
        :param pulumi.Input[str] job_agent_name: The name of the job agent to be created or updated.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The name and tier of the SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobAgentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Azure SQL job agent.

        :param str resource_name: The name of the resource.
        :param JobAgentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobAgentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_id: Optional[pulumi.Input[str]] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = JobAgentArgs.__new__(JobAgentArgs)

            if database_id is None and not opts.urn:
                raise TypeError("Missing required property 'database_id'")
            __props__.__dict__["database_id"] = database_id
            __props__.__dict__["job_agent_name"] = job_agent_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:JobAgent"), pulumi.Alias(type_="azure-native:sql/v20170301preview:JobAgent"), pulumi.Alias(type_="azure-native:sql/v20200801preview:JobAgent"), pulumi.Alias(type_="azure-native:sql/v20201101preview:JobAgent"), pulumi.Alias(type_="azure-native:sql/v20210201preview:JobAgent"), pulumi.Alias(type_="azure-native:sql/v20210501preview:JobAgent")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(JobAgent, __self__).__init__(
            'azure-native:sql/v20200202preview:JobAgent',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'JobAgent':
        """
        Get an existing JobAgent resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobAgentArgs.__new__(JobAgentArgs)

        __props__.__dict__["database_id"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return JobAgent(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> pulumi.Output[str]:
        """
        Resource ID of the database to store job metadata in.
        """
        return pulumi.get(self, "database_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The name and tier of the SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the job agent.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

