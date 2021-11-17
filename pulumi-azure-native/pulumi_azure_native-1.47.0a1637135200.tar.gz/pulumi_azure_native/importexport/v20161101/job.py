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

__all__ = ['JobArgs', 'Job']

@pulumi.input_type
class JobArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['JobDetailsArgs']] = None,
                 tags: Optional[Any] = None):
        """
        The set of arguments for constructing a Job resource.
        :param pulumi.Input[str] resource_group_name: The resource group name uniquely identifies the resource group within the user subscription.
        :param pulumi.Input[str] job_name: The name of the import/export job.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the job should be created
        :param pulumi.Input['JobDetailsArgs'] properties: Specifies the job properties
        :param Any tags: Specifies the tags that will be assigned to the job.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if job_name is not None:
            pulumi.set(__self__, "job_name", job_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name uniquely identifies the resource group within the user subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="jobName")
    def job_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the import/export job.
        """
        return pulumi.get(self, "job_name")

    @job_name.setter
    def job_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the job should be created
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['JobDetailsArgs']]:
        """
        Specifies the job properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['JobDetailsArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        Specifies the tags that will be assigned to the job.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[Any]):
        pulumi.set(self, "tags", value)


class Job(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['JobDetailsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 __props__=None):
        """
        Contains the job information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] job_name: The name of the import/export job.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the job should be created
        :param pulumi.Input[pulumi.InputType['JobDetailsArgs']] properties: Specifies the job properties
        :param pulumi.Input[str] resource_group_name: The resource group name uniquely identifies the resource group within the user subscription.
        :param Any tags: Specifies the tags that will be assigned to the job.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Contains the job information.

        :param str resource_name: The name of the resource.
        :param JobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['JobDetailsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
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
            __props__ = JobArgs.__new__(JobArgs)

            __props__.__dict__["job_name"] = job_name
            __props__.__dict__["location"] = location
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["identity"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:importexport:Job"), pulumi.Alias(type_="azure-native:importexport/v20200801:Job"), pulumi.Alias(type_="azure-native:importexport/v20210101:Job")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Job, __self__).__init__(
            'azure-native:importexport/v20161101:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobArgs.__new__(JobArgs)

        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityDetailsResponse']]:
        """
        Specifies the job identity details
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the Azure location where the job is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the job.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.JobDetailsResponse']:
        """
        Specifies the job properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        SystemData of ImportExport Jobs.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        """
        Specifies the tags that are assigned to the job.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Specifies the type of the job resource.
        """
        return pulumi.get(self, "type")

