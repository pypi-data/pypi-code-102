# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['JobTargetGroupArgs', 'JobTargetGroup']

@pulumi.input_type
class JobTargetGroupArgs:
    def __init__(__self__, *,
                 job_agent_name: pulumi.Input[str],
                 members: pulumi.Input[Sequence[pulumi.Input['JobTargetArgs']]],
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 target_group_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a JobTargetGroup resource.
        :param pulumi.Input[str] job_agent_name: The name of the job agent.
        :param pulumi.Input[Sequence[pulumi.Input['JobTargetArgs']]] members: Members of the target group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] target_group_name: The name of the target group.
        """
        pulumi.set(__self__, "job_agent_name", job_agent_name)
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if target_group_name is not None:
            pulumi.set(__self__, "target_group_name", target_group_name)

    @property
    @pulumi.getter(name="jobAgentName")
    def job_agent_name(self) -> pulumi.Input[str]:
        """
        The name of the job agent.
        """
        return pulumi.get(self, "job_agent_name")

    @job_agent_name.setter
    def job_agent_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "job_agent_name", value)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Input[Sequence[pulumi.Input['JobTargetArgs']]]:
        """
        Members of the target group.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: pulumi.Input[Sequence[pulumi.Input['JobTargetArgs']]]):
        pulumi.set(self, "members", value)

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
    @pulumi.getter(name="targetGroupName")
    def target_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the target group.
        """
        return pulumi.get(self, "target_group_name")

    @target_group_name.setter
    def target_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_group_name", value)


class JobTargetGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobTargetArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 target_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A group of job targets.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] job_agent_name: The name of the job agent.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobTargetArgs']]]] members: Members of the target group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] target_group_name: The name of the target group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobTargetGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A group of job targets.

        :param str resource_name: The name of the resource.
        :param JobTargetGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobTargetGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobTargetArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 target_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = JobTargetGroupArgs.__new__(JobTargetGroupArgs)

            if job_agent_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_agent_name'")
            __props__.__dict__["job_agent_name"] = job_agent_name
            if members is None and not opts.urn:
                raise TypeError("Missing required property 'members'")
            __props__.__dict__["members"] = members
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["target_group_name"] = target_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:JobTargetGroup"), pulumi.Alias(type_="azure-native:sql/v20200202preview:JobTargetGroup"), pulumi.Alias(type_="azure-native:sql/v20200801preview:JobTargetGroup"), pulumi.Alias(type_="azure-native:sql/v20201101preview:JobTargetGroup"), pulumi.Alias(type_="azure-native:sql/v20210201preview:JobTargetGroup"), pulumi.Alias(type_="azure-native:sql/v20210501preview:JobTargetGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(JobTargetGroup, __self__).__init__(
            'azure-native:sql/v20170301preview:JobTargetGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'JobTargetGroup':
        """
        Get an existing JobTargetGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobTargetGroupArgs.__new__(JobTargetGroupArgs)

        __props__.__dict__["members"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return JobTargetGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Output[Sequence['outputs.JobTargetResponse']]:
        """
        Members of the target group.
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

