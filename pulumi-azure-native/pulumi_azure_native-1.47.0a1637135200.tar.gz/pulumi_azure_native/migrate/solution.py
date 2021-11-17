# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['SolutionArgs', 'Solution']

@pulumi.input_type
class SolutionArgs:
    def __init__(__self__, *,
                 migrate_project_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 etag: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['SolutionPropertiesArgs']] = None,
                 solution_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Solution resource.
        :param pulumi.Input[str] migrate_project_name: Name of the Azure Migrate project.
        :param pulumi.Input[str] resource_group_name: Name of the Azure Resource Group that migrate project is part of.
        :param pulumi.Input[str] etag: Gets or sets the ETAG for optimistic concurrency control.
        :param pulumi.Input['SolutionPropertiesArgs'] properties: Gets or sets the properties of the solution.
        :param pulumi.Input[str] solution_name: Unique name of a migration solution within a migrate project.
        """
        pulumi.set(__self__, "migrate_project_name", migrate_project_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if solution_name is not None:
            pulumi.set(__self__, "solution_name", solution_name)

    @property
    @pulumi.getter(name="migrateProjectName")
    def migrate_project_name(self) -> pulumi.Input[str]:
        """
        Name of the Azure Migrate project.
        """
        return pulumi.get(self, "migrate_project_name")

    @migrate_project_name.setter
    def migrate_project_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "migrate_project_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Azure Resource Group that migrate project is part of.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the ETAG for optimistic concurrency control.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['SolutionPropertiesArgs']]:
        """
        Gets or sets the properties of the solution.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['SolutionPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="solutionName")
    def solution_name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique name of a migration solution within a migrate project.
        """
        return pulumi.get(self, "solution_name")

    @solution_name.setter
    def solution_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "solution_name", value)


class Solution(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 migrate_project_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['SolutionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 solution_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Solution REST Resource.
        API Version: 2018-09-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: Gets or sets the ETAG for optimistic concurrency control.
        :param pulumi.Input[str] migrate_project_name: Name of the Azure Migrate project.
        :param pulumi.Input[pulumi.InputType['SolutionPropertiesArgs']] properties: Gets or sets the properties of the solution.
        :param pulumi.Input[str] resource_group_name: Name of the Azure Resource Group that migrate project is part of.
        :param pulumi.Input[str] solution_name: Unique name of a migration solution within a migrate project.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SolutionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Solution REST Resource.
        API Version: 2018-09-01-preview.

        :param str resource_name: The name of the resource.
        :param SolutionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SolutionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 migrate_project_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['SolutionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 solution_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SolutionArgs.__new__(SolutionArgs)

            __props__.__dict__["etag"] = etag
            if migrate_project_name is None and not opts.urn:
                raise TypeError("Missing required property 'migrate_project_name'")
            __props__.__dict__["migrate_project_name"] = migrate_project_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["solution_name"] = solution_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:migrate/v20180901preview:Solution")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Solution, __self__).__init__(
            'azure-native:migrate:Solution',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Solution':
        """
        Get an existing Solution resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SolutionArgs.__new__(SolutionArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return Solution(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the ETAG for optimistic concurrency control.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets the name of this REST resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.SolutionPropertiesResponse']:
        """
        Gets or sets the properties of the solution.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Gets the type of this REST resource.
        """
        return pulumi.get(self, "type")

