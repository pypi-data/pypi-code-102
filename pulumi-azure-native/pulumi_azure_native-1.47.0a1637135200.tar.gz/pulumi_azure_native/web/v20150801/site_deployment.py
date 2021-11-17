# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['SiteDeploymentArgs', 'SiteDeployment']

@pulumi.input_type
class SiteDeploymentArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 active: Optional[pulumi.Input[bool]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 author_email: Optional[pulumi.Input[str]] = None,
                 deployer: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SiteDeployment resource.
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] resource_group_name: Name of resource group
        :param pulumi.Input[bool] active: Active
        :param pulumi.Input[str] author: Author
        :param pulumi.Input[str] author_email: AuthorEmail
        :param pulumi.Input[str] deployer: Deployer
        :param pulumi.Input[str] details: Detail
        :param pulumi.Input[str] end_time: EndTime
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] message: Message
        :param pulumi.Input[str] start_time: StartTime
        :param pulumi.Input[int] status: Status
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if active is not None:
            pulumi.set(__self__, "active", active)
        if author is not None:
            pulumi.set(__self__, "author", author)
        if author_email is not None:
            pulumi.set(__self__, "author_email", author_email)
        if deployer is not None:
            pulumi.set(__self__, "deployer", deployer)
        if details is not None:
            pulumi.set(__self__, "details", details)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of resource group
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def active(self) -> Optional[pulumi.Input[bool]]:
        """
        Active
        """
        return pulumi.get(self, "active")

    @active.setter
    def active(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "active", value)

    @property
    @pulumi.getter
    def author(self) -> Optional[pulumi.Input[str]]:
        """
        Author
        """
        return pulumi.get(self, "author")

    @author.setter
    def author(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author", value)

    @property
    @pulumi.getter(name="authorEmail")
    def author_email(self) -> Optional[pulumi.Input[str]]:
        """
        AuthorEmail
        """
        return pulumi.get(self, "author_email")

    @author_email.setter
    def author_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author_email", value)

    @property
    @pulumi.getter
    def deployer(self) -> Optional[pulumi.Input[str]]:
        """
        Deployer
        """
        return pulumi.get(self, "deployer")

    @deployer.setter
    def deployer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployer", value)

    @property
    @pulumi.getter
    def details(self) -> Optional[pulumi.Input[str]]:
        """
        Detail
        """
        return pulumi.get(self, "details")

    @details.setter
    def details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "details", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        EndTime
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Message
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        StartTime
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[int]]:
        """
        Status
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class SiteDeployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 active: Optional[pulumi.Input[bool]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 author_email: Optional[pulumi.Input[str]] = None,
                 deployer: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents user credentials used for publishing activity

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] active: Active
        :param pulumi.Input[str] author: Author
        :param pulumi.Input[str] author_email: AuthorEmail
        :param pulumi.Input[str] deployer: Deployer
        :param pulumi.Input[str] details: Detail
        :param pulumi.Input[str] end_time: EndTime
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] message: Message
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] resource_group_name: Name of resource group
        :param pulumi.Input[str] start_time: StartTime
        :param pulumi.Input[int] status: Status
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SiteDeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents user credentials used for publishing activity

        :param str resource_name: The name of the resource.
        :param SiteDeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SiteDeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 active: Optional[pulumi.Input[bool]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 author_email: Optional[pulumi.Input[str]] = None,
                 deployer: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
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
            __props__ = SiteDeploymentArgs.__new__(SiteDeploymentArgs)

            __props__.__dict__["active"] = active
            __props__.__dict__["author"] = author
            __props__.__dict__["author_email"] = author_email
            __props__.__dict__["deployer"] = deployer
            __props__.__dict__["details"] = details
            __props__.__dict__["end_time"] = end_time
            __props__.__dict__["id"] = id
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["message"] = message
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["start_time"] = start_time
            __props__.__dict__["status"] = status
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20160801:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20180201:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20181101:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20190801:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20200601:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20200901:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20201001:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20201201:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20210101:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20210115:SiteDeployment"), pulumi.Alias(type_="azure-native:web/v20210201:SiteDeployment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SiteDeployment, __self__).__init__(
            'azure-native:web/v20150801:SiteDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SiteDeployment':
        """
        Get an existing SiteDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SiteDeploymentArgs.__new__(SiteDeploymentArgs)

        __props__.__dict__["active"] = None
        __props__.__dict__["author"] = None
        __props__.__dict__["author_email"] = None
        __props__.__dict__["deployer"] = None
        __props__.__dict__["details"] = None
        __props__.__dict__["end_time"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["message"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["start_time"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return SiteDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def active(self) -> pulumi.Output[Optional[bool]]:
        """
        Active
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter
    def author(self) -> pulumi.Output[Optional[str]]:
        """
        Author
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter(name="authorEmail")
    def author_email(self) -> pulumi.Output[Optional[str]]:
        """
        AuthorEmail
        """
        return pulumi.get(self, "author_email")

    @property
    @pulumi.getter
    def deployer(self) -> pulumi.Output[Optional[str]]:
        """
        Deployer
        """
        return pulumi.get(self, "deployer")

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output[Optional[str]]:
        """
        Detail
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        EndTime
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def message(self) -> pulumi.Output[Optional[str]]:
        """
        Message
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        StartTime
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[int]]:
        """
        Status
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

